# Armazena as configurações do ambiente de desenvolvimento

from os import environ # importa a lib os para acessar as variáveis de ambiente
from dotenv import load_dotenv # importa a lib dotenv para carregar as variáveis de ambiente do arquivo .env

load_dotenv() # carrega as variáveis de ambiente nesse arquivo, acessando a URL definida no .env

# Criar a classe config que vai definir uma caixa isolando as configurações
class Config():
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_DEV') # acessa a variável de ambiente URL do .env e utiliza para a conexão
    SQLALCHEMY_TRACK_MODIFICATIONS = False # define que será utilizado apenas o que estamos setando, assim, carregamentos adicionais não precisam ser feitos --> otimizando as querys no BD