import json
import os

import telebot
import dotenv

import utils_db


dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(token=TOKEN)

def mandar_mensagem(sala_id, mensagem):
    try:
        bot.send_message(chat_id=sala_id, text=mensagem)
    except Exception as error:
        print(error)

def sala(dados: dict, sala_id):
    resultados = {'lista_cores': []}
    cores = {'black': '⚫️', 'yellow': '🟡', 'white': '⚪️'}
    def traduzir_numer(numero):
        if numero >= 1 and numero <= 7:
            return 'yellow'
        elif numero == 0:
            return 'white'
        else:
            return 'black'
    
    def giro():
        ultima_pedra = json.loads(utils_db.obter_resultado('beette')[0])
        pedra_atual = json.loads(utils_db.obter_resultado('beette')[0])
        while ultima_pedra == pedra_atual:
            pedra_atual = json.loads(utils_db.obter_resultado('beette')[0])
        cor = traduzir_numer(pedra_atual['result'])
        resultados['lista_cores'].append(cor)
    
    def verificar_gatilhos():
        gatilhos = dados['estrategias']['gatilhos'] 
        for gatilho in gatilhos:
            if resultados['lista_cores'][-len(gatilhos[gatilho]): ] == gatilhos[gatilho]:
                return True, gatilhos[gatilho]
        return False, False, False
    
    def verificar_padroes():
        padroes = dados['estrategias']['padroes']
        buscadores = dados['estrategias']['buscadores']
        for padrao in padroes:
            if resultados['lista_cores'][-len(padroes[padrao]): ] == padroes[padrao]:
                return True, padroes[padrao], buscadores[padrao]
        return False, False, False

    def verificar_win(cor_win):
        ultima_pedra = resultados['lista_cores'][-1]
        if ultima_pedra == cor_win or ultima_pedra == 'white':
            return True
        return False
    
    while True:
        giro()
        gatilhos = verificar_gatilhos()
        if gatilhos[0]:
            wins = 0
            gales = int(dados['configuracoes']['gales']) + 1
            while wins < dados['configuracoes']['limite_wins']:
                padroes = verificar_padroes()
                if padroes[0]:
                    for gale in range(gales):
                        if gale == 0:
                            gale = 'SG'
                        mensagem = f'⚠️ Entrar no: {cores[padroes[2]]} | ⚪️\n🔄 Status: {gale}'
                        mandar_mensagem(sala_id, f'{mensagem}')
                        giro()
                        if verificar_win(padroes[2]):
                            wins += 1
                            mandar_mensagem(sala_id, f'✅ Winnn ✅ - 🔄 Status: {gale}')
                            break
                    else:
                        wins += int(dados['configuracoes']['limite_wins']) + 5
                        mandar_mensagem(sala_id, f'❌ Loss ...❌')
                else:
                    giro()
