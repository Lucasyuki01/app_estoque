import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Produtos para inserir
produtos = [
    ("Produto A", 50, 10, "Novo", "Depósito 1"),
    ("Produto B", 30, 5, "Usado", "Depósito 2"),
    ("Produto C", 20, 3, "Novo", "Depósito 3"),
    ("Produto D", 100, 20, "Novo", "Depósito 4"),
    ("Produto E", 70, 7, "Usado", "Depósito 5")
]

# Inserir produtos
for produto in produtos:
    cursor.execute("INSERT INTO estoque (nome, quantidade, min, estado, local) VALUES (?, ?, ?, ?, ?)", produto)

# Commit e fechar a conexão
conn.commit()
conn.close()

print("Produtos cadastrados com sucesso!")