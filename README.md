<h1 align="center">Bot Beette - Salas de Sinais</h1>

<p align="center">'Bot Beette - Salas de Sinais' - O Bot Beette é uma ferramenta avançada projetada para gerar e controlar
  múltiplas salas de sinais de forma simultânea. Cada sala pode ser configurada de maneira distinta, proporcionando flexibilidade e 
  personalização para atender às necessidades específicas dos usuários. 
  Este projeto oferece uma solução robusta para o gerenciamento eficiente de sinais relevantes na casa Beette. </p>

<p align="center">
 <a href="#pré-requisitos">Pré-requisitos</a> •
 <a href="#instalação">Instalação</a> • 
 <a href="#tecnologias">Tecnologias</a> • 
 <a href="#contribuicao">Contribuição</a> • 
 <a href="#licenc-a">Licença</a> • 
 <a href="#autor">Autor</a>
</p>

<h4 align="center"> 
	✅  Bot Beette - Salas de Sinais - Finalizado!  ✅
</h4>

### Pré-requisitos
Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com), [Python](https://www.python.org/downloads/). 
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

### Instalação
```bash
# Clone este repositório
$ git clone <https://github.com/Zuriel-Junior-U/bot-beette.git>

# Acesse a pasta do projeto no terminal/cmd
$ cd bot-beette

# Crie seu ambiente virtual
$ python -m venv .venv

# Instale as dependências
$ pip install -r requirements.txt

# Configure o seu .env
# TOKEN = token do seu bot
# ID_TELEGRAM = id do adm

# Gere os dois banco de dados
$ python utils_db.py

# Inicie a extração de dados
$ python extrair_resultado.py

# Inicie o bot
$ python bot.py
```

### Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Python](https://www.python.org/downloads/)
- [Aiogram](https://docs.aiogram.dev/en/latest/)
- [Telebot](https://pypi.org/project/telebot/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [sseclient](https://pypi.org/project/sseclient-py/)

