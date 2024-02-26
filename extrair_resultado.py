import json

import requests
from sseclient import SSEClient

import utils_db as utils


#extrai os ultimos resultados do modo double
def puxar_resultado(casa, id_casa):
    url = f"https://www.tipminer.com/api/rounds/DOUBLE/{id_casa}/live"
    headers = {
        "authority": "www.tipminer.com",
        "accept": "text/event-stream",
        "accept-language": "pt-BR,pt;q=0.9",
        "cache-control": "no-cache",
        "cookie": "cf_clearance=ltfC3Q2qRJVFHtH9gI9TFkYsQs6.L4ONRGxQHBdofVw-1708544824-1.0-AWBFunmWRRfW3Mduw7dRhmTo9GgKIazBZI90+qOkgV+waI9pAXw6WkAOyUmznba3+CFOLvUhDcRoVJWZo4mKf9U=",
        "referer": f"https://www.tipminer.com/historico/{casa}/double",
    }

    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        client = SSEClient(response.iter_content())
        for event in client.events():
            if 'id' in str(event.data):
                resultado = json.loads(event.data)[0]
                utils.atualizar_resultados(casa, json.dumps(resultado))
    else:
        print("Erro na solicitação:", response.status_code)


if __name__ == '__main__':
    while True:
        puxar_resultado('beette', '647f2d0230696c7329011c01')
