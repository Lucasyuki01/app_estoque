import sqlite3

def criar_banco_solicitacoes():
    conn = sqlite3.connect('solicitacoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            importancia TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            observacao TEXT,
            data_solicitacao TEXT NOT NULL,
            status TEXT NOT NULL,
            numero_solicitacao TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados de solicitações criado ou já existente.")

if __name__ == '__main__':
    criar_banco_solicitacoes()
