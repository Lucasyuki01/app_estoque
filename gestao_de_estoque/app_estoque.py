import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkinter import simpledialog

# Função que define o menu
def main_menu(frame_principal):
    # Limpa o frame principal
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Menu Principal", font=("Arial", 16)).pack(pady=10)

    # Menu lateral recriado
    tk.Button(frame_principal, text="Estoque", command=lambda: abrir_estoque(frame_principal)).pack(pady=10)
    tk.Button(frame_principal, text="Solicitar Produto", command=lambda: solicitar_produto(frame_principal)).pack(pady=10)
    tk.Button(frame_principal, text="Acompanhar Pedidos", command=lambda: acompanhar_pedidos(frame_principal)).pack(pady=10)
    tk.Button(frame_principal, text="Cadastrar Novo Produto", command=lambda: cadastrar_novo_produto(frame_principal)).pack(pady=10)
    tk.Button(frame_principal, text="Adicionar Produto Existente", command=lambda: adicionar_produto_existente(frame_principal)).pack(pady=10)
    tk.Button(frame_principal, text="Histórico", command=lambda: abrir_historico(frame_principal)).pack(pady=10)

# Função para abrir estoque
def abrir_estoque(frame_principal):
    # Limpa o frame principal antes de adicionar novos widgets
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Estoque", font=("Arial", 16)).pack(pady=10)

    # Campo de pesquisa
    tk.Label(frame_principal, text="Pesquisar produto:").pack()
    entry_pesquisa = tk.Entry(frame_principal)
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
    tree.pack(fill='both', expand=True)

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

    tk.Button(frame_principal, text="Buscar", command=buscar_produtos).pack(pady=10)
    buscar_produtos()

    # Retirada de produtos
    tk.Label(frame_principal, text="Retirar Produto", font=("Arial", 12)).pack(pady=10)

    # Menu suspenso para selecionar ID
    tk.Label(frame_principal, text="ID do Produto:").pack()
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]  # Formato: ID - Nome
    conn.close()
    combo_id = ttk.Combobox(frame_principal, values=produtos)
    combo_id.pack()

    tk.Label(frame_principal, text="Quantidade a Retirar:").pack()
    entry_quantidade = tk.Entry(frame_principal)
    entry_quantidade.pack()

    tk.Label(frame_principal, text="Responsável pela Retirada:").pack()
    entry_responsavel = tk.Entry(frame_principal)
    entry_responsavel.pack()

    def retirar_produto():
        produto_selecionado = combo_id.get()
        quantidade = entry_quantidade.get()
        responsavel = entry_responsavel.get()

        if not (produto_selecionado and quantidade.isdigit() and responsavel):
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return

        try:
            produto_id, nome = produto_selecionado.split(" - ")
            produto_id = int(produto_id)
        except ValueError:
            messagebox.showerror("Erro", "Selecione um produto válido!")
            return

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        estoque_atual = cursor.fetchone()

        if not estoque_atual:
            messagebox.showerror("Erro", "Produto não encontrado!")
            conn.close()
            return

        estoque_atual = estoque_atual[0]
        quantidade = int(quantidade)

        if quantidade > estoque_atual:
            messagebox.showerror("Erro", "Quantidade insuficiente no estoque!")
            conn.close()
            return

        novo_estoque = estoque_atual - quantidade
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, produto_id))
        conn.commit()

        registrar_historico(produto_id, "Retirada", responsavel, nome, -quantidade, novo_estoque)
        conn.close()

        messagebox.showinfo("Sucesso", f"Retirada de {quantidade} unidades de '{nome}' realizada!")
        buscar_produtos()

    tk.Button(frame_principal, text="Retirar", command=retirar_produto).pack(pady=10)

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal)).pack(pady=10)

# Função para cadastrar novo produto
def cadastrar_novo_produto(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Cadastrar Novo Produto", font=("Arial", 16)).pack(pady=10)

    tk.Label(frame_principal, text="Nome").pack()
    entry_nome = tk.Entry(frame_principal)
    entry_nome.pack()

    tk.Label(frame_principal, text="Quantidade").pack()
    entry_quantidade = tk.Entry(frame_principal)
    entry_quantidade.pack()

    tk.Label(frame_principal, text="Quantidade Mínima").pack()
    entry_minimo = tk.Entry(frame_principal)
    entry_minimo.pack()

    tk.Label(frame_principal, text="Localização").pack()
    entry_localizacao = tk.Entry(frame_principal)
    entry_localizacao.pack()

    tk.Label(frame_principal, text="Estado").pack()
    entry_estado = tk.Entry(frame_principal)
    entry_estado.pack()

    tk.Label(frame_principal, text="Responsável pelo Registro").pack()
    entry_responsavel = tk.Entry(frame_principal)
    entry_responsavel.pack()

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
            main_menu(frame_principal)  # Voltar ao menu principal após salvar

    tk.Button(frame_principal, text="Salvar", command=salvar_novo_produto).pack(pady=10)

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal)).pack(pady=10)

# Função para adicionar quantidade a produto existente
def adicionar_produto_existente(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Adicionar Produto Existente", font=("Arial", 16)).pack(pady=10)

    # Menu suspenso para IDs dos produtos
    tk.Label(frame_principal, text="ID do Produto").pack()
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM produtos")
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    combo_id = ttk.Combobox(frame_principal, values=ids)
    combo_id.pack()

    # Campos restantes
    tk.Label(frame_principal, text="Quantidade a Adicionar").pack()
    entry_quantidade = tk.Entry(frame_principal)
    entry_quantidade.pack()

    tk.Label(frame_principal, text="Responsável pela Adição").pack()
    entry_responsavel = tk.Entry(frame_principal)
    entry_responsavel.pack()

    def salvar_quantidade():
        produto_id = combo_id.get()
        quantidade = entry_quantidade.get()
        responsavel = entry_responsavel.get()

        # Validações iniciais
        if not (produto_id and quantidade.isdigit() and responsavel):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios e devem ser preenchidos corretamente.")
            return

        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Verifica se o produto existe
            cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (int(produto_id),))
            produto = cursor.fetchone()

            if not produto:
                messagebox.showerror("Erro", f"Produto com ID {produto_id} não encontrado.")
                return

            nome, estoque_atual = produto
            quantidade = int(quantidade)

            # Calcula o novo total no estoque
            novo_estoque = estoque_atual + quantidade

            # Atualiza o estoque no banco de dados
            cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, int(produto_id)))

            # Registra no histórico
            registrar_historico(int(produto_id), "Adição", responsavel, nome, quantidade, novo_estoque)

            conn.commit()
            messagebox.showinfo("Sucesso", f"Quantidade atualizada para o produto '{nome}' por {responsavel}. Novo estoque: {novo_estoque}.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
        finally:
            conn.close()
            main_menu(frame_principal)  # Voltar ao menu principal após salvar

    tk.Button(frame_principal, text="Salvar", command=salvar_quantidade).pack(pady=10)

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal)).pack(pady=10)

# Página para solicitar um produto
def solicitar_produto(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Solicitar Produto", font=("Arial", 16)).pack(pady=10)

    tk.Label(frame_principal, text="Nome do Produto").pack()
    entry_nome = tk.Entry(frame_principal)
    entry_nome.pack()

    tk.Label(frame_principal, text="Quantidade").pack()
    entry_quantidade = tk.Entry(frame_principal)
    entry_quantidade.pack()

    tk.Label(frame_principal, text="Importância").pack()
    combo_importancia = ttk.Combobox(frame_principal, values=["Alta", "Média", "Baixa"])
    combo_importancia.pack()

    tk.Label(frame_principal, text="Responsável").pack()
    entry_responsavel = tk.Entry(frame_principal)
    entry_responsavel.pack()

    tk.Label(frame_principal, text="Observação (Opcional)").pack()
    entry_observacao = tk.Entry(frame_principal)
    entry_observacao.pack()

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

    tk.Button(frame_principal, text="Salvar Solicitação", command=salvar_solicitacao).pack(pady=10)

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal)).pack(pady=10)

# Página para acompanhar pedidos
def acompanhar_pedidos(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Acompanhar Pedidos", font=("Arial", 16)).pack(pady=10)

    # Campo de filtro
    tk.Label(frame_principal, text="Filtrar por:").pack()
    filtro_opcao = ttk.Combobox(frame_principal, values=["Responsável", "Número da Solicitação"])
    filtro_opcao.pack()

    tk.Label(frame_principal, text="Valor do Filtro").pack()
    entry_filtro = tk.Entry(frame_principal)
    entry_filtro.pack()

    # Tabela de pedidos
    tree = ttk.Treeview(
        frame_principal,
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
    tree.pack(fill='both', expand=True)

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

    tk.Button(frame_principal, text="Carregar Pedidos", command=carregar_pedidos).pack(pady=10)
    carregar_pedidos()

    # Atualizar status
    def atualizar_status():
        senha = simpledialog.askstring("Senha", "Digite a senha para alterar o status:")
        if senha != "admin123":  # Substitua pela senha desejada
            messagebox.showerror("Erro", "Senha incorreta!")
            return

        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Nenhum pedido selecionado!")
            return

        pedido = tree.item(item_selecionado, 'values')

        # Janela para atualizar o status
        janela_status = tk.Toplevel()
        janela_status.title("Atualizar Status")
        janela_status.geometry("300x150")

        tk.Label(janela_status, text="Selecione o novo status:").pack(pady=10)

        # Opções de status
        status_var = tk.StringVar()
        combo_status = ttk.Combobox(
            janela_status,
            textvariable=status_var,
            values=["Solicitado", "Recusado", "Em análise", "Comprado", "Recebido"]
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

                # Atualiza o banco de dados
                cursor.execute("UPDATE solicitacoes SET status = ? WHERE numero_solicitacao = ?", (novo_status, pedido[8]))
                conn.commit()

                # Atualiza a tabela exibida
                carregar_pedidos()  # Recarrega todos os pedidos para refletir a alteração
                messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
                janela_status.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
            finally:
                conn.close()

        tk.Button(janela_status, text="Salvar", command=salvar_status).pack(pady=10)

    tk.Button(frame_principal, text="Atualizar Status", command=atualizar_status).pack(pady=10)

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal)).pack(pady=10)

# Função para histórico
def abrir_historico(frame_principal):
    for widget in frame_principal.winfo_children():
        widget.destroy()

    tk.Label(frame_principal, text="Histórico de Ações", font=("Arial", 16)).pack(pady=10)

    # Tabela para exibir o histórico
    tree = ttk.Treeview(
        frame_principal,
        columns=('Produto ID', 'Ação', 'Responsável', 'Produto', 'Quantidade', 'Novo Total', 'Data'),
        show='headings'
    )
    tree.heading('Produto ID', text='ID do Produto')
    tree.heading('Ação', text='Ação')
    tree.heading('Responsável', text='Responsável')
    tree.heading('Produto', text='Produto')
    tree.heading('Quantidade', text='Quantidade')
    tree.heading('Novo Total', text='Novo Total')
    tree.heading('Data', text='Data')
    tree.pack(fill='both', expand=True)

    # Filtros
    tk.Label(frame_principal, text="Filtrar por:").pack(pady=5)
    filtro_opcao = ttk.Combobox(frame_principal, values=["Nome do Produto", "Produto ID", "Responsável"])
    filtro_opcao.pack()

    tk.Label(frame_principal, text="Valor do Filtro").pack(pady=5)
    entry_filtro = tk.Entry(frame_principal)
    entry_filtro.pack()

    # Função para carregar o histórico do banco de dados com filtro
    def carregar_historico():
        tree.delete(*tree.get_children())  # Limpa a tabela antes de carregar novos dados
        conn = sqlite3.connect('historico.db')
        cursor = conn.cursor()

        query = "SELECT * FROM historico"
        parametros = []

        # Aplica o filtro com base na escolha do usuário
        if filtro_opcao.get() == "Nome do Produto" and entry_filtro.get():
            query += " WHERE produto LIKE ?"
            parametros.append('%' + entry_filtro.get() + '%')
        elif filtro_opcao.get() == "Produto ID" and entry_filtro.get():
            query += " WHERE produto_id = ?"
            parametros.append(entry_filtro.get())
        elif filtro_opcao.get() == "Responsável" and entry_filtro.get():
            query += " WHERE responsavel LIKE ?"
            parametros.append('%' + entry_filtro.get() + '%')

        cursor.execute(query, parametros)
        for row in cursor.fetchall():
            tree.insert('', tk.END, values=row)
        conn.close()

    # Botões para carregar e limpar o filtro
    tk.Button(frame_principal, text="Carregar Histórico", command=carregar_historico).pack(pady=10)
    tk.Button(frame_principal, text="Limpar Filtro", command=lambda: [entry_filtro.delete(0, tk.END), carregar_historico()]).pack(pady=10)

    # Carrega o histórico inicialmente
    carregar_historico()

    # Botão de Voltar
    tk.Button(frame_principal, text="Voltar", command=lambda: main_menu(frame_principal)).pack(pady=10)

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

def main():
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