import sqlite3

def criar_historico_banco():
    # Conecta ao banco de dados separado para o histórico
    conn = sqlite3.connect('historico.db')
    cursor = conn.cursor()

    # Criação da tabela de histórico
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acao TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados de histórico criado ou já existente.")

if __name__ == '__main__':
    criar_historico_banco()
