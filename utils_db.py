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

# CREAT (C)
def cadastrar_usuario(id_telegram, tipo_cliente):
    dados_usurio['tipo_usuario'] = tipo_cliente
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (id_telegram, dados_usuario) VALUES (?, ?)",
                   (id_telegram,  json.dumps(dados_usurio)))
    conn.commit()
    conn.close()

# READ (R)
def dados_usuario(id_telegram):
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT dados_usuario FROM usuarios WHERE id_telegram = ?", (id_telegram,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return json.loads(resultado[0])
    else:
        return None

# UPDATE (U)
def atualizar_usuario(id_telegram, campo, novo_valor):
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE usuarios SET {campo} = ? WHERE id_telegram = ?", (novo_valor, id_telegram))
    conn.commit()
    conn.close()

# DELETE (D)
def deletar_usuario(id_telegram):
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_telegram = ?", (id_telegram,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    #criar_banco_dados()
    #cadastrar_usuario('12323', 'user')
    #print(dados_usuario('12323'))
    #atualizar_usuario('12323', 'dados_usuario', 'dado atualizado')
    #deletar_usuario('12323')
    pass
