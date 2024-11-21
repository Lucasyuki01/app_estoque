import sqlite3

def criar_historico_banco():
    conn = sqlite3.connect('historico.db')
    cursor = conn.cursor()

    # Criar ou recriar a tabela de histórico com a nova estrutura
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acao TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            novo_total INTEGER NOT NULL,
            data TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados de histórico criado ou atualizado com sucesso.")

if __name__ == '__main__':
    criar_historico_banco()
