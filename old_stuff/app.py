import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def show_frame(frame):
    frame.tkraise()

def search_stock():
    query = search_var.get()
    for row in tree.get_children():
        tree.delete(row)
    for row in cursor.execute("SELECT * FROM estoque WHERE nome LIKE ?", ('%' + query + '%',)):
        tree.insert("", "end", values=row)

def load_products():
    cursor.execute("SELECT nome FROM estoque")
    return [row[0] for row in cursor.fetchall()]

def register_retirada():
    responsavel = responsavel_var.get().strip()
    produto = produto_var.get().strip()
    quantidade_str = quantidade_var.get()
    
    print(responsavel_var)
    print(quantidade_var, 'oi')
    print(responsavel)
    print(quantidade_str)
    if not responsavel:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos! Resp")
    if not produto:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos! prod")
    if not quantidade_str:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos! quant")
        return

    try:
        quantidade = int(quantidade_str)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro válido!")
        return

    cursor.execute("SELECT quantidade FROM estoque WHERE nome = ?", (produto,))
    result = cursor.fetchone()

    if result and result[0] >= quantidade:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO historico_retiradas (responsavel, produto, quantidade, data) VALUES (?, ?, ?, ?)",
                       (responsavel, produto, quantidade, data))
        cursor.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE nome = ?", (quantidade, produto))
        conn.commit()
        messagebox.showinfo("Sucesso", "Retirada registrada com sucesso!")
        show_frame(estoque_frame)
    else:
        messagebox.showerror("Erro", "Quantidade indisponível em estoque!")

def cadastrar_produto():
    nome = nome_var.get().strip()
    quantidade_str = quantidade_var.get().strip()
    min_str = min_var.get().strip()
    estado = estado_var.get().strip()
    local = local_var.get().strip()

    if not nome or not quantidade_str or not min_str or not estado or not local:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    try:
        quantidade = int(quantidade_str)
        min_valor = int(min_str)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e Min devem ser números inteiros válidos!")
        return

    cursor.execute("INSERT INTO estoque (nome, quantidade, min, estado, local) VALUES (?, ?, ?, ?, ?)",
                   (nome, quantidade, min_valor, estado, local))
    conn.commit()
    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
    show_frame(estoque_frame)

def populate_treeview():
    for row in tree.get_children():
        tree.delete(row)
    for row in cursor.execute("SELECT * FROM estoque"):
        tree.insert("", "end", values=row)

def show_historico_retiradas():
    for row in historico_tree.get_children():
        historico_tree.delete(row)
    for row in cursor.execute("SELECT * FROM historico_retiradas"):
        historico_tree.insert("", "end", values=row)
    show_frame(historico_retirada_frame)

root = tk.Tk()
root.title("Aplicativo de Gestão")

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Configuração das frames
main_frame = ttk.Frame(root, padding=10)
estoque_frame = ttk.Frame(root, padding=10)
cantina_frame = ttk.Frame(root, padding=10)
consultar_estoque_frame = ttk.Frame(root, padding=10)
registrar_retirada_frame = ttk.Frame(root, padding=10)
cadastro_produto_frame = ttk.Frame(root, padding=10)
historico_retirada_frame = ttk.Frame(root, padding=10)

for frame in (main_frame, estoque_frame, cantina_frame, consultar_estoque_frame, registrar_retirada_frame, cadastro_produto_frame, historico_retirada_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Frame principal (Menu inicial)
ttk.Label(main_frame, text="Menu Inicial").grid(column=0, row=0, columnspan=2)
ttk.Button(main_frame, text="Estoque", command=lambda: show_frame(estoque_frame)).grid(column=0, row=1)
ttk.Button(main_frame, text="Cantina", command=lambda: show_frame(cantina_frame)).grid(column=1, row=1)

# Frame de estoque
ttk.Label(estoque_frame, text="Estoque").grid(column=0, row=0, columnspan=2)
ttk.Button(estoque_frame, text="Consultar estoque", command=lambda: [show_frame(consultar_estoque_frame), populate_treeview()]).grid(column=0, row=1)
ttk.Button(estoque_frame, text="Registrar retirada", command=lambda: show_frame(registrar_retirada_frame)).grid(column=0, row=2)
ttk.Button(estoque_frame, text="Solicitar produto").grid(column=0, row=3)
ttk.Button(estoque_frame, text="Acompanhar solicitação").grid(column=0, row=4)
ttk.Button(estoque_frame, text="Cadastrar produto", command=lambda: show_frame(cadastro_produto_frame)).grid(column=0, row=5)
ttk.Button(estoque_frame, text="Histórico de retiradas", command=show_historico_retiradas).grid(column=0, row=6)
ttk.Button(estoque_frame, text="Voltar", command=lambda: show_frame(main_frame)).grid(column=0, row=7)

# Frame de cantina
ttk.Label(cantina_frame, text="Cantina").grid(column=0, row=0, columnspan=2)
ttk.Button(cantina_frame, text="Consultar cardápio").grid(column=0, row=1)
ttk.Button(cantina_frame, text="Registrar compra").grid(column=1, row=1)
ttk.Button(cantina_frame, text="Voltar", command=lambda: show_frame(main_frame)).grid(column=0, row=2, columnspan=2)

# Frame de consultar estoque
ttk.Label(consultar_estoque_frame, text="Consultar Estoque").grid(column=0, row=0, columnspan=2)
search_var = tk.StringVar()
ttk.Entry(consultar_estoque_frame, textvariable=search_var).grid(column=0, row=1)
ttk.Button(consultar_estoque_frame, text="Buscar", command=search_stock).grid(column=1, row=1)
ttk.Button(consultar_estoque_frame, text="Voltar", command=lambda: show_frame(estoque_frame)).grid(column=0, row=2, columnspan=2)

tree = ttk.Treeview(consultar_estoque_frame, columns=("id", "nome", "quantidade", "min", "estado", "local"), show='headings')
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("quantidade", text="Quantidade")
tree.heading("min", text="Min")
tree.heading("estado", text="Estado")
tree.heading("local", text="Local")
tree.grid(column=0, row=3, columnspan=2)

# Frame de registrar retirada
ttk.Label(registrar_retirada_frame, text="Registrar Retirada").grid(column=0, row=0, columnspan=2)

#Responsavel
ttk.Label(registrar_retirada_frame, text="Responsável").grid(column=0, row=1)
responsavel_var = tk.StringVar()
ttk.Entry(registrar_retirada_frame, textvariable=responsavel_var).grid(column=1, row=1)
#Quantidade
ttk.Label(registrar_retirada_frame, text="Quantidade").grid(column=0, row=2)
quantidade_var = tk.StringVar()
ttk.Entry(registrar_retirada_frame, textvariable=quantidade_var).grid(column=1, row=2)
#Produto
ttk.Label(registrar_retirada_frame, text="Produto").grid(column=0, row=3)
produto_var = tk.StringVar()
produto_menu = ttk.Combobox(registrar_retirada_frame, textvariable=produto_var)
produto_menu['values'] = load_products()
produto_menu.grid(column=1, row=3)

ttk.Button(registrar_retirada_frame, text="Registrar", command=register_retirada).grid(column=0, row=4, columnspan=2)

ttk.Button(registrar_retirada_frame, text="Voltar", command=lambda: show_frame(estoque_frame)).grid(column=0, row=5, columnspan=2)

# Frame de cadastro de produto
ttk.Label(cadastro_produto_frame, text="Cadastro de Produto").grid(column=0, row=0, columnspan=2)
ttk.Label(cadastro_produto_frame, text="Nome").grid(column=0, row=1, padx=5, pady=5)
nome_var = tk.StringVar()
ttk.Entry(cadastro_produto_frame, textvariable=nome_var).grid(column=1, row=1, padx=5, pady=5)
ttk.Label(cadastro_produto_frame, text="Quantidade").grid(column=0, row=2, padx=5, pady=5)
quantidade_var = tk.StringVar()
ttk.Entry(cadastro_produto_frame, textvariable=quantidade_var).grid(column=1, row=2, padx=5, pady=5)
ttk.Label(cadastro_produto_frame, text="Min").grid(column=0, row=3, padx=5, pady=5)
min_var = tk.StringVar()
ttk.Entry(cadastro_produto_frame, textvariable=min_var).grid(column=1, row=3, padx=5, pady=5)
ttk.Label(cadastro_produto_frame, text="Estado").grid(column=0, row=4, padx=5, pady=5)
estado_var = tk.StringVar()
ttk.Entry(cadastro_produto_frame, textvariable=estado_var).grid(column=1, row=4, padx=5, pady=5)
ttk.Label(cadastro_produto_frame, text="Local").grid(column=0, row=5, padx=5, pady=5)
local_var = tk.StringVar()
ttk.Entry(cadastro_produto_frame, textvariable=local_var).grid(column=1, row=5, padx=5, pady=5)
ttk.Button(cadastro_produto_frame, text="Cadastrar", command=cadastrar_produto).grid(column=0, row=6, columnspan=2)
ttk.Button(cadastro_produto_frame, text="Voltar", command=lambda: show_frame(estoque_frame)).grid(column=0, row=7, columnspan=2)

# Frame de histórico de retiradas
ttk.Label(historico_retirada_frame, text="Histórico de Retiradas").grid(column=0, row=0, columnspan=2)
historico_tree = ttk.Treeview(historico_retirada_frame, columns=("id", "responsavel", "produto", "quantidade", "data"), show='headings')
historico_tree.heading("id", text="ID")
historico_tree.heading("responsavel", text="Responsável")
historico_tree.heading("produto", text="Produto")
historico_tree.heading("quantidade", text="Quantidade")
historico_tree.heading("data", text="Data")
historico_tree.grid(column=0, row=1, columnspan=2)
ttk.Button(historico_retirada_frame, text="Voltar", command=lambda: show_frame(estoque_frame)).grid(column=0, row=2, columnspan=2)

# Mostrar a frame principal inicialmente
show_frame(main_frame)

root.mainloop()
