# Vamos tratar as rotas da entidade

from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador # Importando o model para usar o ORM (Object Relational Mapping)
from src.model import db # Importando o db para usar o SQLAlchemy
from src.security.security import hash_senha, checar_senha # Importando o módulo de segurança para criptografar a senha e verificar a senha
from flasgger import swag_from # Importando o módulo para gerar a documentação da API

# request: trabalha com as requisições, capturando o corpo/conteúdo da requisição (JSON, por exemplo)
# jsonify: trabalha com as respostas da requisição, convertendo um dado Python em JSON

# Instanciando o Blueprint
bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')


# TODA ROTA TEM UMA FUNÇÃO ASSOCIADA
# e toda função tem o return
@bp_colaborador.route('/todos-colaboradores', methods=['GET'])
def get_todos_colaboradores():
    colaboradores = db.session.execute(
        db.select(Colaborador) 
    ).scalar_all() # Retorna todos os resultados da consulta (scalar_all)
    
    colaboradores = [colaborador.all_data() for colaborador in colaboradores] # Transforma cada colaborador em um dicionário, já que estamos usando o método all_data() para cada linha da tabela Colaborador
    
    return jsonify(colaboradores), 200


# Rota para cadastrar um colaborador
# Só vai aceitar método POST (é uma boa prática colocar em maiúsculo)
@bp_colaborador.route('/cadastrar', methods=['POST'])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml') # Importando o arquivo de documentação da API
def cadastrar_novo_colaborador():
    # Primeiro: capturar o corpo da requisição (JSON)
    dados_requisicao = request.get_json()
    
    # Python lê o JSON e trata como um dicionário
    # novo_colaborador = {
    #    'id': len(dados) + 1, # atuando como um AUTO_INCREMENT
    #    'nome': dados_requisicao['nome'], # pegando a chave nome
    #    'cargo': dados_requisicao['cargo'],
    #    'cracha': dados_requisicao['cracha']
    #}  
    #dados.append(novo_colaborador) # adicionando o novo colaborador no final da lista de dados (já que estamos usando append)
    
    # Como estamos usando ORM, não precisamos fazer isso manualmente como estava sendo feito aí acima
    
    novo_colaborador = Colaborador( # instancia ORM
        nome = dados_requisicao['nome'],
        email = dados_requisicao['email'],
        senha = hash_senha(dados_requisicao['senha']),
        cargo = dados_requisicao['cargo'],
        salario = dados_requisicao['salario']
    )
    
    db.session.add(novo_colaborador) # monta o insert no banco de dados
    db.session.commit() # executa a query de insert montada acima
    
    return jsonify({'mensagem': 'Dado cadastrado com sucesso'}), 201
# O jsonify transforma a mensagem em JSON, para retornar na resposta da requisição.
# Status Code 201 indica que deu certo a requisição e foi criado


# endereco/colaborador/atualizar/id
@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
def atualizar_dados_colaborador(id_colaborador): 
    # funções com put tem parametro para armazenar o que veio na URL
    
    dados_requisicao = request.get_json()
    
    # Primeiro precisamos verificar se o id_colaborador enviado existe na lista
    for colaborador in dados_requisicao:
        if colaborador['id'] == id_colaborador:
            colaborador_encontrado = colaborador
            break # sai do if e sai do loop
    
    # se houver a chave nome no JSON do conteúdo da requisição,
    # então vamos atualizar o nome do colaborador encontrado
    if 'nome' in dados_requisicao:
        colaborador_encontrado['nome'] = dados_requisicao['nome']
    
    if 'cargo' in dados_requisicao:
        colaborador_encontrado['cargo'] = dados_requisicao['cargo']
    
    if 'cracha' in dados_requisicao:
        colaborador_encontrado['cracha'] = dados_requisicao['cracha']
    
    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200


@bp_colaborador.route('/login', methods=['POST'])
def login():
    # Captura o body da requisição
    dados_requisicao = request.get_json()
    
    email = dados_requisicao['email']
    senha = dados_requisicao['senha']
    
    if not email or not senha:
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
    
    # Verifica se o colaborador existe no banco de dados através do ORM, usando a classe que representa a entidade do BD
    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar() # Executa a query e retorna apenas o primeiro resultado (scalar) ou None se não encontrar nada
    
    if not colaborador:
        return jsonify({'mensagem': 'Usuario não encontrado'}), 404
    
    
    colaborador = colaborador.to_dict() # transforma o objeto colaborador em um dicionário
    if email == colaborador.get('email') and checar_senha(senha, colaborador.get('senha')):
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas'}), 401
    

# Com o Blueprint criado, precisamos registrá-lo na aplicação Flask
# Depois, rodamos o caminho da rota, por exemplo: http://localhost:5000/colaborador/pegar-dados