# Responsável por configurar o Flask/criar a aplicação

from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.model import db
from config import Config # traz a classe Config
from flask_cors import CORS
from flasgger import Swagger

swagger_config = {
    "headers": [], # Caso tenha um componente de autorização, adicionar na lista
    "specs": [ # Especificações da documentação
        {
            "endpoint": 'apispec',
            "route": '/apispec.json/', 
            # rota do arquivo JSON para a construção da documentação
            "rule_filter": lambda rule: True,
            # regras de filtragem dos endpoints
            # todas as rotas serão documentadas
            "model_filter": lambda tag: True,
            # especifica quais modelos serão documentados
        }
    ],
    "static_url_path": "/flasgger_static", # URL para acessar a documentação
    "swagger_ui": True, # Habilita a interface do Swagger UI
    "specs_route": "/apidocs/"
}

# Inicialização do Flask
def create_app():
    app = Flask(__name__) # Instancia do Flask
    CORS(app, origins="*") # Habilita o CORS para todas as rotas da aplicação
    app.register_blueprint(bp_colaborador)  
    # Registrando o blueprint do colaborador
    # se criar outra rota nesse mesmo arquivo, como já registramos a blueprint, não precisa mais add no app.py
    # Mas se criasse outra rota em outro arquivo, precisaria registrar a blueprint aqui também
    
    app.config.from_object(Config) # Carrega as configurações do banco de dados
    
    db.init_app(app) # Inicia a conexão com o banco de dados
    
    Swagger(app, config=swagger_config) # Inicializa o Swagger com as configurações definidas acima e documentar os endpoints
    
    with app.app_context(): 
        # Se as tabelas não existem, crie-as
        db.create_all()

    return app
