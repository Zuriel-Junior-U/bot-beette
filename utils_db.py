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

# DB DE USUARIOS:
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

# EXTRA (READ)
def obter_usuarios():
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_telegram FROM usuarios")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# DB DE RESULTADOS
def criar_db_resultados(casas):
    conn = sqlite3.connect('resultados.db')
    cursor = conn.cursor()

    query = f'''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {', '.join(f'{casa} TEXT' for casa in casas)}
        )
    '''
    cursor.execute(query)

    conn.commit()
    conn.close()

# (U) ATUALIZANDO RESULTADO NO DB: resultados
def atualizar_resultados(campo, novo_valor):
    conn = sqlite3.connect('resultados.db')
    cursor = conn.cursor()
    query = f"UPDATE resultados SET {campo} = ?"
    cursor.execute(query, (novo_valor,))
    conn.commit()
    conn.close()

# (R) LENDO RESULTADO DO DB: resultados
def obter_resultado(campo):
    conn = sqlite3.connect('resultados.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT {campo} FROM resultados")
    valor_atual = cursor.fetchone()
    conn.close()
    return valor_atual

if __name__ == '__main__':
    #cadastrar_usuario('12323', 'user')
    #print(dados_usuario('12323'))
    #atualizar_usuario('12323', 'dados_usuario', 'dado atualizado')
    #deletar_usuario('12323')
    #print(obter_usuarios())
    criar_banco_dados()
    criar_db_resultados(['beette'])
    pass
