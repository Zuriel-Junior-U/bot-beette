import json

import utils_db


def sala(dados: dict):
    resultados = {'lista_cores': []}
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
        print(resultados)
    
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

    
    while True:
        giro()
        gatilhos = verificar_gatilhos()
        if gatilhos[0]:
            print('bateu o gatilho')
            wins = 0
            while wins <= dados['configuracoes']['limite_wins']:
                padroes = verificar_padroes()
                if padroes[0]:
                    print(f'Entrar no {padroes[2]}')
                giro()



if __name__ == '__main__':
    dados = {}
    sala(dados)
