import sqlite3
import json
import os

import dotenv


dotenv.load_dotenv()
dados_usurio = {
    'tipo_usuario': '',
    'sala_selecionada': None,
    'salas': {}
}

def criar_banco_dados():
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    ID_TELEGRAM = os.getenv('ID_TELEGRAM')
    dados_usurio['tipo_usuario'] = 'adm'
    cursor.execute('''CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    id_telegram TEXT,
    dados_usuario TEXT
    )    
    ''')
    cursor.execute("INSERT INTO usuarios (id_telegram, dados_usuario) VALUES (?, ?)", 
                   (ID_TELEGRAM, json.dumps(dados_usurio)))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    #criar_banco_dados()
    pass
