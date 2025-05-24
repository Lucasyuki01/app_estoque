import sqlite3

# Conexão com o banco de dados de produtos
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criação da tabela de produtos (caso não exista)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        minimo INTEGER NOT NULL,
        localizacao TEXT,
        estado TEXT,
        unidade_medida TEXT
    )
''')

# Dados fictícios para 20 produtos
produtos = [
    ("Cabo HDMI", 50, 10, "Corredor A1", "Novo", "Unidade"),
    ("Mouse USB", 100, 20, "Corredor B2", "Novo", "Unidade"),
    ("Teclado Mecânico", 30, 5, "Corredor B3", "Novo", "Unidade"),
    ("Monitor 24 polegadas", 15, 2, "Corredor C1", "Novo", "Unidade"),
    ("Placa Mãe ATX", 20, 3, "Corredor C2", "Novo", "Unidade"),
    ("Fonte de Alimentação", 40, 10, "Corredor D1", "Novo", "Unidade"),
    ("Gabinete Gamer", 25, 5, "Corredor D2", "Novo", "Unidade"),
    ("SSD 1TB", 60, 10, "Corredor E1", "Novo", "Unidade"),
    ("HD 2TB", 35, 5, "Corredor E2", "Novo", "Unidade"),
    ("Memória RAM 16GB", 45, 10, "Corredor F1", "Novo", "Unidade"),
    ("Notebook 15 polegadas", 10, 2, "Corredor G1", "Novo", "Unidade"),
    ("Smartphone", 50, 10, "Corredor H1", "Novo", "Unidade"),
    ("Mousepad XXL", 70, 20, "Corredor I1", "Novo", "Unidade"),
    ("Cooler para CPU", 25, 5, "Corredor J1", "Novo", "Unidade"),
    ("Cabo Ethernet 10m", 80, 10, "Corredor K1", "Novo", "Unidade"),
    ("Adaptador USB-C", 90, 15, "Corredor L1", "Novo", "Unidade"),
    ("Hub USB", 35, 5, "Corredor M1", "Novo", "Unidade"),
    ("Controle Xbox", 20, 5, "Corredor N1", "Novo", "Unidade"),
    ("Fone de Ouvido Bluetooth", 60, 10, "Corredor O1", "Novo", "Unidade"),
    ("Impressora Multifuncional", 10, 2, "Corredor P1", "Novo", "Unidade"),
]

# Inserção dos registros no banco de dados
for produto in produtos:
    cursor.execute('''
        INSERT INTO produtos (nome, quantidade, minimo, localizacao, estado, unidade_medida)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', produto)

# Commit e fechamento da conexão
conn.commit()
conn.close()

print("20 produtos foram adicionados ao banco de dados com sucesso.")
