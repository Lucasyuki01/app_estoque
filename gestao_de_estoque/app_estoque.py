import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Função para registrar ações no histórico
def registrar_historico(acao, responsavel, produto, quantidade):
    # Conecta ao banco de dados do histórico
    conn = sqlite3.connect('historico.db')
    cursor = conn.cursor()

    # Insere o registro no histórico
    data_acao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO historico (acao, responsavel, produto, quantidade, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (acao, responsavel, produto, quantidade, data_acao))

    conn.commit()
    conn.close()

# Função para abrir a tela de Estoque
def abrir_estoque():
    janela_estoque = tk.Toplevel()
    janela_estoque.title("Estoque")

    # Campo de pesquisa
    tk.Label(janela_estoque, text="Pesquisar produto:").pack()
    entry_pesquisa = tk.Entry(janela_estoque)
    entry_pesquisa.pack()

    # Tabela de resultados
    tree = ttk.Treeview(
        janela_estoque,
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
    tree.pack()

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

    tk.Button(janela_estoque, text="Buscar", command=buscar_produtos).pack()
    buscar_produtos()

    # Retirada de produtos
    tk.Label(janela_estoque, text="Retirar Produto").pack()

    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM produtos")
    produtos = [row[0] for row in cursor.fetchall()]
    conn.close()

    produto_var = tk.StringVar()
    menu_produtos = ttk.Combobox(janela_estoque, textvariable=produto_var, values=produtos)
    menu_produtos.pack()

    tk.Label(janela_estoque, text="Quantidade a Retirar:").pack()
    entry_quantidade = tk.Entry(janela_estoque)
    entry_quantidade.pack()

    tk.Label(janela_estoque, text="Responsável pela Retirada:").pack()
    entry_responsavel = tk.Entry(janela_estoque)
    entry_responsavel.pack()

    def retirar_produto():
        nome = produto_var.get()
        quantidade = entry_quantidade.get()
        responsavel = entry_responsavel.get()

        if not (nome and quantidade and responsavel):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos antes de continuar.")
            return
        if not quantidade.isdigit() or int(quantidade) <= 0:
            messagebox.showerror("Erro", "A quantidade deve ser um número maior que zero.")
            return

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade FROM produtos WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showerror("Erro", f"O produto '{nome}' não existe no estoque.")
        else:
            estoque_atual = resultado[0]
            if int(quantidade) > estoque_atual:
                messagebox.showerror("Erro", "A quantidade solicitada excede o estoque disponível.")
            else:
                novo_estoque = estoque_atual - int(quantidade)
                cursor.execute("UPDATE produtos SET quantidade = ? WHERE nome = ?", (novo_estoque, nome))
                conn.commit()
                registrar_historico("Retirada", responsavel, nome, int(quantidade))
                messagebox.showinfo("Sucesso", f"{quantidade} unidades de '{nome}' retiradas do estoque por {responsavel}.")
                buscar_produtos()
        conn.close()

    tk.Button(janela_estoque, text="Retirar", command=retirar_produto).pack()

# Função para cadastrar novo produto
def cadastrar_novo_produto():
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

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, quantidade, minimo, localizacao, estado, unidade_medida)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, int(quantidade), int(minimo), localizacao, estado, "Unidade"))
        conn.commit()
        registrar_historico("Cadastro", responsavel, nome, int(quantidade))
        conn.close()
        messagebox.showinfo("Sucesso", f"Produto cadastrado com sucesso pelo responsável {responsavel}!")
        janela_cadastrar.destroy()

    janela_cadastrar = tk.Toplevel()
    janela_cadastrar.title("Cadastrar Novo Produto")

    tk.Label(janela_cadastrar, text="Nome").grid(row=0, column=0)
    entry_nome = tk.Entry(janela_cadastrar)
    entry_nome.grid(row=0, column=1)

    tk.Label(janela_cadastrar, text="Quantidade").grid(row=1, column=0)
    entry_quantidade = tk.Entry(janela_cadastrar)
    entry_quantidade.grid(row=1, column=1)

    tk.Label(janela_cadastrar, text="Quantidade Mínima").grid(row=2, column=0)
    entry_minimo = tk.Entry(janela_cadastrar)
    entry_minimo.grid(row=2, column=1)

    tk.Label(janela_cadastrar, text="Localização").grid(row=3, column=0)
    entry_localizacao = tk.Entry(janela_cadastrar)
    entry_localizacao.grid(row=3, column=1)

    tk.Label(janela_cadastrar, text="Estado").grid(row=4, column=0)
    entry_estado = tk.Entry(janela_cadastrar)
    entry_estado.grid(row=4, column=1)

    tk.Label(janela_cadastrar, text="Responsável pelo Registro").grid(row=5, column=0)
    entry_responsavel = tk.Entry(janela_cadastrar)
    entry_responsavel.grid(row=5, column=1)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar_novo_produto).grid(row=6, column=0, columnspan=2, pady=10)

# Função para adicionar quantidade a produto existente
def adicionar_produto_existente():
    def salvar_quantidade():
        produto_id = entry_id.get()
        quantidade = entry_quantidade.get()
        responsavel = entry_responsavel.get()

        if not (produto_id.isdigit() and quantidade.isdigit() and responsavel):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios e devem ser preenchidos corretamente.")
            return

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (int(produto_id),))
        produto = cursor.fetchone()

        if not produto:
            messagebox.showerror("Erro", f"Produto com ID {produto_id} não encontrado.")
        else:
            nome, estoque_atual = produto
            novo_estoque = estoque_atual + int(quantidade)
            cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, int(produto_id)))
            conn.commit()
            registrar_historico("Adição", responsavel, nome, int(quantidade))
            messagebox.showinfo("Sucesso", f"Quantidade atualizada para o produto '{nome}' por {responsavel}. Novo estoque: {novo_estoque}.")
        conn.close()
        janela_adicionar.destroy()

    janela_adicionar = tk.Toplevel()
    janela_adicionar.title("Adicionar Produto")

    tk.Label(janela_adicionar, text="ID do Produto").grid(row=0, column=0)
    entry_id = tk.Entry(janela_adicionar)
    entry_id.grid(row=0, column=1)

    tk.Label(janela_adicionar, text="Quantidade a Adicionar").grid(row=1, column=0)
    entry_quantidade = tk.Entry(janela_adicionar)
    entry_quantidade.grid(row=1, column=1)

    tk.Label(janela_adicionar, text="Responsável pela Adição").grid(row=2, column=0)
    entry_responsavel = tk.Entry(janela_adicionar)
    entry_responsavel.grid(row=2, column=1)

    tk.Button(janela_adicionar, text="Salvar", command=salvar_quantidade).grid(row=3, column=0, columnspan=2, pady=10)

def abrir_historico():
    janela_historico = tk.Toplevel()
    janela_historico.title("Histórico de Ações")

    # Tabela para exibir o histórico
    tree = ttk.Treeview(
        janela_historico,
        columns=('ID', 'Ação', 'Responsável', 'Produto', 'Quantidade', 'Data'),
        show='headings'
    )
    tree.heading('ID', text='ID')
    tree.heading('Ação', text='Ação')
    tree.heading('Responsável', text='Responsável')
    tree.heading('Produto', text='Produto')
    tree.heading('Quantidade', text='Quantidade')
    tree.heading('Data', text='Data')
    tree.pack(fill='both', expand=True)

    # Função para carregar o histórico do banco de dados
    def carregar_historico():
        tree.delete(*tree.get_children())  # Limpa a tabela antes de carregar novos dados
        conn = sqlite3.connect('historico.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historico")
        for row in cursor.fetchall():
            tree.insert('', tk.END, values=row)
        conn.close()

    carregar_historico()

    # Botão para recarregar o histórico
    tk.Button(janela_historico, text="Recarregar", command=carregar_historico).pack(pady=10)

# Função para gerar um número único de solicitação
def gerar_numero_solicitacao():
    return datetime.now().strftime('%Y%m%d%H%M%S')

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
        tree.delete(*tree.get_children())
        conn = sqlite3.connect('solicitacoes.db')
        cursor = conn.cursor()

        query = "SELECT * FROM solicitacoes"
        parametros = []

        if filtro_opcao.get() == "Responsável" and entry_filtro.get():
            query += " WHERE responsavel LIKE ?"
            parametros.append('%' + entry_filtro.get() + '%')
        elif filtro_opcao.get() == "Número da Solicitação" and entry_filtro.get():
            query += " WHERE numero_solicitacao LIKE ?"
            parametros.append('%' + entry_filtro.get() + '%')

        query += " ORDER BY data_solicitacao"
        cursor.execute(query, parametros)

        for row in cursor.fetchall():
            tree.insert('', tk.END, values=row)
        conn.close()

    tk.Button(frame_principal, text="Carregar Pedidos", command=carregar_pedidos).pack(pady=10)

    # Atualizar status
    def atualizar_status():
        senha = tk.simpledialog.askstring("Senha", "Digite a senha para alterar o status:")
        if senha != "admin123":
            messagebox.showerror("Erro", "Senha incorreta!")
            return

        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Nenhum pedido selecionado!")
            return

        pedido = tree.item(item_selecionado, 'values')
        novo_status = tk.simpledialog.askstring("Novo Status", "Digite o novo status (Solicitado, Recusado, Em análise, Comprado, Recebido):")

        if novo_status not in ["Solicitado", "Recusado", "Em análise", "Comprado", "Recebido"]:
            messagebox.showerror("Erro", "Status inválido!")
            return

        conn = sqlite3.connect('solicitacoes.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE solicitacoes SET status = ? WHERE id = ?", (novo_status, pedido[0]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
        carregar_pedidos()

    tk.Button(frame_principal, text="Atualizar Status", command=atualizar_status).pack(pady=10)


# Menu Principal
def main():
    root = tk.Tk()
    root.title("Gestão de Estoque e Solicitações")
    root.geometry("900x600")

    frame_principal = tk.Frame(root)
    frame_principal.pack(fill='both', expand=True)

    menu_lateral = tk.Frame(root, width=200, bg="#f0f0f0")
    menu_lateral.pack(side="left", fill="y")

    tk.Button(root, text="Estoque", command=abrir_estoque).pack()
    tk.Button(menu_lateral, text="Solicitar Produto", command=lambda: solicitar_produto(frame_principal)).pack(pady=10)
    tk.Button(menu_lateral, text="Acompanhar Pedidos", command=lambda: acompanhar_pedidos(frame_principal)).pack(pady=10)
    tk.Button(root, text="Cadastrar Novo Produto", command=cadastrar_novo_produto).pack()
    tk.Button(root, text="Adicionar Produto Existente", command=adicionar_produto_existente).pack()
    tk.Button(root, text="Histórico", command=abrir_historico).pack()

    root.mainloop()

if __name__ == '__main__':
    main()
