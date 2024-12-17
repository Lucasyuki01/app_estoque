import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkinter import simpledialog

# Função que define o menu
def main_menu(frame_principal):
    """
    Função para renderizar o menu principal no frame_principal.
    Garante que o layout fique centralizado e alinhado após qualquer ação.
    """
    # Define a cor de fundo
    frame_principal.configure(bg="light gray")  # Cor de fundo cinza claro

    # Limpa todos os widgets existentes no frame principal
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Redefine a configuração do grid para garantir centralização
    frame_principal.grid_rowconfigure(0, weight=1)  # Espaço superior
    frame_principal.grid_rowconfigure(8, weight=1)  # Espaço inferior
    frame_principal.grid_columnconfigure(0, weight=1)  # Espaço lateral esquerda
    frame_principal.grid_columnconfigure(2, weight=1)  # Espaço lateral direita

    # Título do menu principal
    tk.Label(
        frame_principal,
        text="Gestão de Estoque e Solicitações",
        font=("Arial", 24, "bold"),
        bg="light gray"  # Adiciona a cor de fundo ao título
    ).grid(row=0, column=1, pady=20)

    # Botões do menu principal, centralizados
    menu_buttons = [
        ("Estoque", lambda: abrir_estoque(frame_principal)),
        ("Solicitar Produto", lambda: solicitar_produto(frame_principal)),
        ("Acompanhar Pedidos", lambda: acompanhar_pedidos(frame_principal)),
        ("Cadastrar Novo Produto", lambda: cadastrar_novo_produto(frame_principal)),
        ("Adicionar Produto Existente", lambda: adicionar_produto_existente(frame_principal)),
        ("Histórico", lambda: abrir_historico(frame_principal)),
    ]

    for idx, (text, command) in enumerate(menu_buttons, start=1):
        tk.Button(
            frame_principal,
            text=text,
            command=command,
            font=("Arial", 14),  # Tamanho da fonte dos botões
            width=25,  # Botões de largura consistente
            height=2   # Altura consistente
        ).grid(row=idx, column=1, pady=10)  # Alinhado na coluna central

    # Mensagem de rodapé
    tk.Label(
        frame_principal,
        text="Gestão de Estoque - Desenvolvido por Lucas Yuki",
        font=("Arial", 10, "italic"),
        bg="light gray"  # Adiciona a cor de fundo ao rodapé
    ).grid(row=8, column=1, pady=20)

def inicializar_banco_de_dados():
    """
    Verifica se o banco de dados e as tabelas necessárias existem.
    Se não existirem, cria-as.
    """
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Criação da tabela produtos, se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            minimo INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            estado TEXT NOT NULL,
            unidade_medida TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Função para abrir estoque
def abrir_estoque(frame_principal):
    """
    Página para gerenciar o estoque, com pesquisa, retirada e exibição de produtos.
    """
    # Limpa o frame principal antes de adicionar novos widgets
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Estoque", font=("Arial", 16)).pack(pady=10)

    # Campo de pesquisa
    tk.Label(frame_principal, text="Pesquisar produto:").pack()
    entry_pesquisa = tk.Entry(frame_principal, width=30)
    entry_pesquisa.pack()

    # Tabela de resultados
    tree = ttk.Treeview(
        frame_principal,
        columns=('ID', 'Nome', 'Quantidade', 'Mínimo', 'Localização', 'Estado', 'Unidade de Medida'),
        show='headings'
    )
    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Quantidade', text='Quantidade')
    tree.heading('Mínimo', text='Mínimo')
    tree.heading('Localização', text='Localização')
    tree.heading('Estado', text='Estado')
    tree.heading('Unidade de Medida', text='Unidade de Medida')
    tree.pack(fill='both', expand=True, pady=10)

    def buscar_produtos():
        tree.delete(*tree.get_children())
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        pesquisa = entry_pesquisa.get()
        if pesquisa:
            cursor.execute("SELECT id, nome, quantidade, minimo, localizacao, estado, unidade_medida FROM produtos WHERE nome LIKE ?", ('%' + pesquisa + '%',))
        else:
            cursor.execute("SELECT id, nome, quantidade, minimo, localizacao, estado, unidade_medida FROM produtos")
        for row in cursor.fetchall():
            tree.insert('', tk.END, values=row)
        conn.close()

    tk.Button(frame_principal, text="Buscar", command=buscar_produtos, width=30).pack(pady=10)
    buscar_produtos()

    # Retirada de produtos
    tk.Label(frame_principal, text="Retirar Produto", font=("Arial", 12)).pack(pady=10)

    tk.Label(frame_principal, text="ID do Produto:").pack()
    entry_id = tk.Entry(frame_principal, width=30)
    entry_id.pack()

    tk.Label(frame_principal, text="Quantidade a Retirar:").pack()
    entry_quantidade = tk.Entry(frame_principal, width=30)
    entry_quantidade.pack()

    tk.Label(frame_principal, text="Responsável pela Retirada:").pack()
    entry_responsavel = tk.Entry(frame_principal, width=30)
    entry_responsavel.pack()

    def retirar_produto():
        produto_id = entry_id.get()
        quantidade = entry_quantidade.get()
        responsavel = entry_responsavel.get()

        if not (produto_id.isdigit() and quantidade.isdigit() and responsavel):
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (int(produto_id),))
        produto = cursor.fetchone()

        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado!")
            conn.close()
            return

        nome, estoque_atual = produto
        quantidade = int(quantidade)

        if quantidade > estoque_atual:
            messagebox.showerror("Erro", "Quantidade insuficiente no estoque!")
            conn.close()
            return

        novo_estoque = estoque_atual - quantidade
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, int(produto_id)))
        conn.commit()

        registrar_historico(int(produto_id), "Retirada", responsavel, nome, -quantidade, novo_estoque)
        conn.close()

        messagebox.showinfo("Sucesso", f"Retirada de {quantidade} unidades de '{nome}' realizada!")
        buscar_produtos()

    tk.Button(frame_principal, text="Retirar", command=retirar_produto, width=30, height=2).pack(pady=10)

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal), width=30, height=2).pack(pady=10)

# Função para cadastrar novo produto
def cadastrar_novo_produto(frame_principal):
    """
    Página para cadastrar um novo produto, com layout ajustado e deslocado verticalmente.
    """
    # Limpa o frame principal antes de adicionar novos widgets
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Centralização e padronização do layout com deslocamento vertical
    container = tk.Frame(frame_principal)
    container.pack(expand=True, fill='both', padx=20, pady=(100, 20))  # Aumenta o deslocamento vertical com `pady=(100, 20)`

    # Título com menor espaçamento vertical
    tk.Label(container, text="Cadastrar Novo Produto", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Nome do Produto
    tk.Label(container, text="Nome do Produto:", font=("Arial", 12), anchor="e").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_nome = tk.Entry(container, width=40, font=("Arial", 12))
    entry_nome.grid(row=1, column=1, padx=5, pady=5)

    # Quantidade Inicial
    tk.Label(container, text="Quantidade Inicial:", font=("Arial", 12), anchor="e").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_quantidade = tk.Entry(container, width=40, font=("Arial", 12))
    entry_quantidade.grid(row=2, column=1, padx=5, pady=5)

    # Quantidade Mínima
    tk.Label(container, text="Quantidade Mínima:", font=("Arial", 12), anchor="e").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_minimo = tk.Entry(container, width=40, font=("Arial", 12))
    entry_minimo.grid(row=3, column=1, padx=5, pady=5)

    # Localização
    tk.Label(container, text="Localização:", font=("Arial", 12), anchor="e").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_localizacao = tk.Entry(container, width=40, font=("Arial", 12))
    entry_localizacao.grid(row=4, column=1, padx=5, pady=5)

    # Estado
    tk.Label(container, text="Estado:", font=("Arial", 12), anchor="e").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_estado = tk.Entry(container, width=40, font=("Arial", 12))
    entry_estado.grid(row=5, column=1, padx=5, pady=5)

    # Responsável
    tk.Label(container, text="Responsável pelo Registro:", font=("Arial", 12), anchor="e").grid(row=6, column=0, sticky="e", padx=5, pady=5)
    entry_responsavel = tk.Entry(container, width=40, font=("Arial", 12))
    entry_responsavel.grid(row=6, column=1, padx=5, pady=5)

    # Função para salvar o novo produto
    def salvar_novo_produto():
        nome = entry_nome.get()
        quantidade = entry_quantidade.get()
        minimo = entry_minimo.get()
        localizacao = entry_localizacao.get()
        estado = entry_estado.get()
        responsavel = entry_responsavel.get()

        if not (nome and quantidade.isdigit() and minimo.isdigit() and localizacao and estado and responsavel):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios e devem ser preenchidos corretamente.")
            return

        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (nome, quantidade, minimo, localizacao, estado, unidade_medida)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, int(quantidade), int(minimo), localizacao, estado, "Unidade"))
            conn.commit()

            # Obter o ID do produto recém-criado
            produto_id = cursor.lastrowid

            # O novo total é igual à quantidade inicial
            novo_total = int(quantidade)
            registrar_historico(produto_id, "Cadastro", responsavel, nome, novo_total, novo_total)

            messagebox.showinfo("Sucesso", f"Produto cadastrado com sucesso pelo responsável {responsavel}!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
        finally:
            conn.close()
            main_menu(frame_principal)

    # Botões
    tk.Button(container, text="Salvar Produto", command=salvar_novo_produto, width=20, font=("Arial", 12)).grid(row=7, column=0, columnspan=2, pady=(20, 10))
    tk.Button(container, text="Voltar", command=lambda: main_menu(frame_principal), width=20, font=("Arial", 12)).grid(row=8, column=0, columnspan=2, pady=10)

    # Centraliza o grid no frame
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

# Função para adicionar quantidade a produto existente
def adicionar_produto_existente(frame_principal):
    """
    Página para adicionar quantidade a um produto existente.
    """
    # Limpa o frame principal antes de adicionar novos widgets
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Centralização e padronização do layout
    container = tk.Frame(frame_principal)
    container.pack(expand=True, fill='both', padx=20, pady=40)

    # Título
    tk.Label(container, text="Adicionar Produto Existente", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Menu suspenso para IDs e nomes dos produtos
    tk.Label(container, text="ID - Nome do Produto:", font=("Arial", 14), anchor="e").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    conn.close()
    combo_produto = ttk.Combobox(container, values=produtos, width=38, font=("Arial", 14))
    combo_produto.grid(row=1, column=1, padx=5, pady=5)

    # Quantidade a adicionar
    tk.Label(container, text="Quantidade a Adicionar:", font=("Arial", 14), anchor="e").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_quantidade = tk.Entry(container, width=40, font=("Arial", 14))
    entry_quantidade.grid(row=2, column=1, padx=5, pady=5)

    # Responsável pela adição
    tk.Label(container, text="Responsável:", font=("Arial", 14), anchor="e").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_responsavel = tk.Entry(container, width=40, font=("Arial", 14))
    entry_responsavel.grid(row=3, column=1, padx=5, pady=5)

    # Função para salvar a adição
    def salvar_quantidade():
        produto_selecionado = combo_produto.get()
        quantidade = entry_quantidade.get()
        responsavel = entry_responsavel.get()

        # Validações iniciais
        if not (produto_selecionado and quantidade.isdigit() and responsavel):
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return

        try:
            produto_id, nome_produto = produto_selecionado.split(" - ")
            produto_id = int(produto_id)
        except ValueError:
            messagebox.showerror("Erro", "Selecione um produto válido!")
            return

        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Verifica se o produto existe
            cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
            resultado = cursor.fetchone()

            if not resultado:
                messagebox.showerror("Erro", "Produto não encontrado!")
                conn.close()
                return

            estoque_atual = resultado[0]
            quantidade = int(quantidade)

            # Atualiza o estoque
            novo_estoque = estoque_atual + quantidade
            cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, produto_id))

            # Registra no histórico
            registrar_historico(produto_id, "Adição", responsavel, nome_produto, quantidade, novo_estoque)
            conn.commit()

            messagebox.showinfo("Sucesso", f"Quantidade adicionada ao produto '{nome_produto}' com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
        finally:
            conn.close()
            main_menu(frame_principal)

    # Botões
    tk.Button(container, text="Salvar", command=salvar_quantidade, width=20, font=("Arial", 14)).grid(row=4, column=0, columnspan=2, pady=(20, 10))
    tk.Button(container, text="Voltar", command=lambda: main_menu(frame_principal), width=20, font=("Arial", 14)).grid(row=5, column=0, columnspan=2, pady=10)

    # Centraliza o grid no frame
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

# Página para solicitar um produto
def solicitar_produto(frame_principal):
    """
    Página para solicitar um produto, com fontes ajustadas.
    """
    # Limpa o frame principal antes de adicionar novos widgets
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Centralização e padronização do layout
    container = tk.Frame(frame_principal)
    container.pack(expand=True, fill='both', padx=20, pady=40)

    # Título
    tk.Label(container, text="Solicitar Produto", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Nome do Produto
    tk.Label(container, text="Nome do Produto:", font=("Arial", 14), anchor="e").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_nome = tk.Entry(container, width=40, font=("Arial", 14))
    entry_nome.grid(row=1, column=1, padx=5, pady=5)

    # Quantidade
    tk.Label(container, text="Quantidade:", font=("Arial", 14), anchor="e").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_quantidade = tk.Entry(container, width=40, font=("Arial", 14))
    entry_quantidade.grid(row=2, column=1, padx=5, pady=5)

    # Importância
    tk.Label(container, text="Importância:", font=("Arial", 14), anchor="e").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    combo_importancia = ttk.Combobox(container, values=["Alta", "Média", "Baixa"], width=38, font=("Arial", 14))
    combo_importancia.grid(row=3, column=1, padx=5, pady=5)

    # Responsável
    tk.Label(container, text="Responsável:", font=("Arial", 14), anchor="e").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_responsavel = tk.Entry(container, width=40, font=("Arial", 14))
    entry_responsavel.grid(row=4, column=1, padx=5, pady=5)

    # Observação (Opcional)
    tk.Label(container, text="Observação (Opcional):", font=("Arial", 14), anchor="e").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_observacao = tk.Entry(container, width=40, font=("Arial", 14))
    entry_observacao.grid(row=5, column=1, padx=5, pady=5)

    # Função para salvar a solicitação
    def salvar_solicitacao():
        nome_produto = entry_nome.get()
        quantidade = entry_quantidade.get()
        importancia = combo_importancia.get()
        responsavel = entry_responsavel.get()
        observacao = entry_observacao.get()
        data_solicitacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        numero_solicitacao = gerar_numero_solicitacao()

        if not (nome_produto and quantidade.isdigit() and importancia and responsavel):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios corretamente!")
            return

        conn = sqlite3.connect('solicitacoes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO solicitacoes (nome_produto, quantidade, importancia, responsavel, observacao, data_solicitacao, status, numero_solicitacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome_produto, int(quantidade), importancia, responsavel, observacao, data_solicitacao, "Solicitado", numero_solicitacao))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"Solicitação registrada com sucesso!\nNúmero da solicitação: {numero_solicitacao}")

    # Botões
    tk.Button(container, text="Salvar Solicitação", command=salvar_solicitacao, width=20, font=("Arial", 14)).grid(row=6, column=0, columnspan=2, pady=(20, 10))
    tk.Button(container, text="Voltar", command=lambda: main_menu(frame_principal), width=20, font=("Arial", 14)).grid(row=7, column=0, columnspan=2, pady=10)

    # Centraliza o grid no frame
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

# Página para acompanhar pedidos
def acompanhar_pedidos(frame_principal):
    """
    Página para acompanhar pedidos.
    """
    # Limpa o frame principal antes de adicionar novos widgets
    for widget in frame_principal.winfo_children():
        widget.destroy()

    # Centralização e padronização do layout
    container = tk.Frame(frame_principal)
    container.pack(expand=True, fill='both', padx=20, pady=20)

    tk.Label(container, text="Acompanhar Pedidos", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=20)

    # Campo de filtro
    filtro_frame = tk.Frame(container)
    filtro_frame.grid(row=1, column=0, columnspan=3, pady=10)
    tk.Label(filtro_frame, text="Filtrar por:").grid(row=0, column=0, padx=5)
    filtro_opcao = ttk.Combobox(filtro_frame, values=["Responsável", "Número da Solicitação"], width=27)
    filtro_opcao.grid(row=0, column=1, padx=5)

    tk.Label(filtro_frame, text="Valor do Filtro:").grid(row=0, column=2, padx=5)
    entry_filtro = tk.Entry(filtro_frame, width=30)
    entry_filtro.grid(row=0, column=3, padx=5)

    # Botão de carregar pedidos
    tk.Button(container, text="Carregar Pedidos", command=lambda: carregar_pedidos(), width=20).grid(row=2, column=0, columnspan=3, pady=10)

    # Tabela de pedidos
    tree = ttk.Treeview(
        container,
        columns=('ID', 'Produto', 'Quantidade', 'Importância', 'Responsável', 'Observação', 'Data', 'Status', 'Número'),
        show='headings'
    )
    tree.heading('ID', text='ID')
    tree.heading('Produto', text='Produto')
    tree.heading('Quantidade', text='Quantidade')
    tree.heading('Importância', text='Importância')
    tree.heading('Responsável', text='Responsável')
    tree.heading('Observação', text='Observação')
    tree.heading('Data', text='Data')
    tree.heading('Status', text='Status')
    tree.heading('Número', text='Número')
    tree.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=10)

    # Configuração do grid para tabela e container
    container.grid_rowconfigure(3, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # Botão de atualizar status
    tk.Button(container, text="Atualizar Status", command=lambda: atualizar_status(), width=20).grid(row=4, column=0, columnspan=3, pady=10)

    # Botão de voltar
    tk.Button(container, text="Voltar", command=lambda: main_menu(frame_principal), width=20).grid(row=5, column=0, columnspan=3, pady=10)

    # Função para carregar pedidos
    def carregar_pedidos():
        tree.delete(*tree.get_children())  # Limpa a tabela antes de carregar novos dados
        conn = sqlite3.connect('solicitacoes.db')
        cursor = conn.cursor()

        query = "SELECT * FROM solicitacoes"
        parametros = []

        # Aplica os filtros, se houver
        if filtro_opcao.get() == "Responsável" and entry_filtro.get():
            query += " WHERE responsavel LIKE ?"
            parametros.append('%' + entry_filtro.get() + '%')
        elif filtro_opcao.get() == "Número da Solicitação" and entry_filtro.get():
            query += " WHERE numero_solicitacao LIKE ?"
            parametros.append('%' + entry_filtro.get() + '%')

        query += " ORDER BY data_solicitacao"
        cursor.execute(query, parametros)

        # Preenche a tabela com os resultados
        for row in cursor.fetchall():
            tree.insert('', tk.END, values=row)
        conn.close()

    def atualizar_status():
        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Nenhum pedido selecionado!")
            return

        pedido = tree.item(item_selecionado, 'values')

        janela_status = tk.Toplevel()
        janela_status.title("Atualizar Status")
        janela_status.geometry("300x150")

        tk.Label(janela_status, text="Selecione o novo status:").pack(pady=10)

        status_var = tk.StringVar()
        combo_status = ttk.Combobox(
            janela_status,
            textvariable=status_var,
            values=["Solicitado", "Recusado", "Em análise", "Comprado", "Recebido"],
            width=27
        )
        combo_status.pack(pady=10)

        def salvar_status():
            novo_status = combo_status.get()
            if novo_status not in ["Solicitado", "Recusado", "Em análise", "Comprado", "Recebido"]:
                messagebox.showerror("Erro", "Status inválido! Por favor, selecione um status válido.")
                return

            try:
                conn = sqlite3.connect('solicitacoes.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE solicitacoes SET status = ? WHERE numero_solicitacao = ?", (novo_status, pedido[8]))
                conn.commit()
                messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
                carregar_pedidos()
                janela_status.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
            finally:
                conn.close()

        tk.Button(janela_status, text="Salvar", command=salvar_status).pack(pady=10)

# Função para histórico
def abrir_historico(frame_principal):
    # Limpa o frame principal antes de adicionar novos widgets
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Histórico de Ações", font=("Arial", 16)).pack(pady=10)

    # Tabela para exibir o histórico
    tree = ttk.Treeview(
        frame_principal,
        columns=('Produto ID', 'Produto', 'Ação', 'Responsável', 'Quantidade', 'Novo Total', 'Data'),
        show='headings',
        height=15
    )
    tree.heading('Produto ID', text='ID')
    tree.heading('Produto', text='Nome do Produto')
    tree.heading('Ação', text='Ação')
    tree.heading('Responsável', text='Responsável')
    tree.heading('Quantidade', text='Quantidade')
    tree.heading('Novo Total', text='Novo Total')
    tree.heading('Data', text='Data')
    tree.pack(fill='both', expand=True, padx=20, pady=10)

    # Configura largura das colunas para melhor visualização
    tree.column('Produto ID', width=100, anchor='center')
    tree.column('Produto', width=150, anchor='center')
    tree.column('Ação', width=100, anchor='center')
    tree.column('Responsável', width=150, anchor='center')
    tree.column('Quantidade', width=100, anchor='center')
    tree.column('Novo Total', width=100, anchor='center')
    tree.column('Data', width=200, anchor='center')

    # Filtros
    tk.Label(frame_principal, text="Filtrar por:", font=("Arial", 12)).pack(pady=5)
    filtro_opcao = ttk.Combobox(frame_principal, values=["ID - Nome", "Responsável"], font=("Arial", 12))
    filtro_opcao.pack(pady=5)

    entry_filtro = tk.StringVar()
    combo_filtro = ttk.Combobox(frame_principal, textvariable=entry_filtro, font=("Arial", 12), state="disabled")
    combo_filtro.pack(pady=5)

    # Função para carregar os valores no menu suspenso de acordo com o filtro selecionado
    def carregar_opcoes_filtro(event):
        conn = sqlite3.connect('historico.db')
        cursor = conn.cursor()
        filtro_selecionado = filtro_opcao.get()

        if filtro_selecionado == "ID - Nome":
            cursor.execute("SELECT DISTINCT produto_id, produto FROM historico")
            valores = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        elif filtro_selecionado == "Responsável":
            cursor.execute("SELECT DISTINCT responsavel FROM historico")
            valores = [row[0] for row in cursor.fetchall()]
        else:
            valores = []

        combo_filtro['values'] = valores
        combo_filtro['state'] = "readonly" if valores else "disabled"
        conn.close()

    filtro_opcao.bind("<<ComboboxSelected>>", carregar_opcoes_filtro)

    # Função para carregar o histórico do banco de dados com filtro
    def carregar_historico():
        tree.delete(*tree.get_children())  # Limpa a tabela antes de carregar novos dados
        conn = sqlite3.connect('historico.db')
        cursor = conn.cursor()

        query = "SELECT produto_id, produto, acao, responsavel, quantidade, novo_total, data FROM historico"
        parametros = []

        # Aplica o filtro com base na escolha do usuário
        if filtro_opcao.get() == "ID - Nome" and entry_filtro.get():
            produto_id = entry_filtro.get().split(" - ")[0]  # Extrai apenas o ID
            query += " WHERE produto_id = ?"
            parametros.append(produto_id)
        elif filtro_opcao.get() == "Responsável" and entry_filtro.get():
            query += " WHERE responsavel LIKE ?"
            parametros.append(entry_filtro.get())

        cursor.execute(query, parametros)
        for row in cursor.fetchall():
            tree.insert('', tk.END, values=row)
        conn.close()

    # Botão para carregar o histórico com filtros aplicados
    tk.Button(frame_principal, text="Carregar Histórico", command=carregar_historico, font=("Arial", 12), width=20).pack(pady=5)

    # Botão para limpar os filtros
    def limpar_filtros():
        filtro_opcao.set("")
        combo_filtro.set("")
        combo_filtro['state'] = "disabled"
        carregar_historico()

    tk.Button(frame_principal, text="Limpar Filtros", command=limpar_filtros, font=("Arial", 12), width=20).pack(pady=5)

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal), font=("Arial", 12), width=20).pack(pady=10)

    # Carrega o histórico inicialmente
    carregar_historico()

# Função para registrar ações no histórico
def registrar_historico(produto_id, acao, responsavel, produto, quantidade, novo_total):
    # Conecta ao banco de dados do histórico
    conn = sqlite3.connect('historico.db')
    cursor = conn.cursor()

    # Insere o registro no histórico
    data_acao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO historico (produto_id, acao, responsavel, produto, quantidade, novo_total, data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (produto_id, acao, responsavel, produto, quantidade, novo_total, data_acao))

    conn.commit()
    conn.close()

# Função para gerar um número único de solicitação
def gerar_numero_solicitacao():
    return datetime.now().strftime('%Y%m%d%H%M%S')

# Função que verifica o estoque
def verificar_estoque_minimo():
    """
    Verifica se algum produto está com quantidade menor ou igual ao mínimo
    e gera uma solicitação automática se ainda não houver uma.
    """
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Seleciona todos os produtos cujo estoque está menor ou igual ao mínimo
    cursor.execute("SELECT id, nome, quantidade, minimo FROM produtos WHERE quantidade <= minimo")
    produtos_baixo_estoque = cursor.fetchall()
    conn.close()

    if not produtos_baixo_estoque:
        return  # Nenhuma ação necessária se todos os produtos estão acima do mínimo

    # Conecta ao banco de solicitações para verificar e registrar as solicitações
    conn_solicitacoes = sqlite3.connect('solicitacoes.db')
    cursor_solicitacoes = conn_solicitacoes.cursor()

    for produto in produtos_baixo_estoque:
        produto_id, nome, quantidade_atual, minimo = produto

        # Verifica se já existe uma solicitação pendente para este produto
        cursor_solicitacoes.execute('''
            SELECT COUNT(*) FROM solicitacoes
            WHERE nome_produto = ? AND status IN ("Solicitado", "Em análise")
        ''', (nome,))
        resultado = cursor_solicitacoes.fetchone()

        if resultado[0] > 0:
            continue  # Já existe uma solicitação pendente para este produto

        # Calcula a quantidade sugerida para a compra (3x o mínimo)
        quantidade_sugerida = 3 * minimo

        # Preenche os campos da solicitação automática
        nome_produto = nome
        quantidade = quantidade_sugerida
        importancia = "Baixa"
        responsavel = "Sistema"
        observacao = "Gerado automaticamente devido ao baixo estoque."
        data_solicitacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        numero_solicitacao = gerar_numero_solicitacao()

        # Insere a solicitação no banco de dados de solicitações
        cursor_solicitacoes.execute('''
            INSERT INTO solicitacoes (nome_produto, quantidade, importancia, responsavel, observacao, data_solicitacao, status, numero_solicitacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome_produto, quantidade, importancia, responsavel, observacao, data_solicitacao, "Solicitado", numero_solicitacao))

    conn_solicitacoes.commit()
    conn_solicitacoes.close()

# Função principal
def main():
    inicializar_banco_de_dados()  # Garante que o banco de dados está configurado
    root = tk.Tk()
    root.title("Gestão de Estoque e Solicitações")
    root.geometry("1200x800")

    # Criação do frame principal
    frame_principal = tk.Frame(root)
    frame_principal.pack(fill='both', expand=True)

    # Menu lateral
    menu_lateral = tk.Frame(root, width=200, bg="#f0f0f0")
    menu_lateral.pack(side="left", fill="y")

    # Chamada inicial do menu principal
    main_menu(frame_principal)

    root.mainloop()


if __name__ == '__main__':
    main()