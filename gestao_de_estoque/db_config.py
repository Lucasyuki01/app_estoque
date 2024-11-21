import sqlite3

def criar_banco():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Criar a tabela com as colunas atualizadas
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
    conn.commit()
    conn.close()
    print("Banco de dados criado ou atualizado com sucesso!")

if __name__ == '__main__':
    criar_banco()
