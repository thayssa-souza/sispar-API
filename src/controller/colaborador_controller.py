from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flasgger import swag_from 

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@bp_colaborador.route('/todos-colaboradores', methods=['GET'])
def get_todos_colaboradores():
    colaboradores = db.session.execute(
        db.select(Colaborador) 
    ).scalar_all()
    
    colaboradores = [colaborador.all_data() for colaborador in colaboradores] 
    
    return jsonify(colaboradores), 200


@bp_colaborador.route('/cadastrar', methods=['POST'])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def cadastrar_novo_colaborador():
    dados_requisicao = request.get_json()
    
    novo_colaborador = Colaborador(
        nome = dados_requisicao['nome'],
        email = dados_requisicao['email'],
        senha = hash_senha(dados_requisicao['senha']),
        cargo = dados_requisicao['cargo'],
        salario = dados_requisicao['salario']
    )
    
    db.session.add(novo_colaborador)
    db.session.commit()
    
    return jsonify({'mensagem': 'Dado cadastrado com sucesso'}), 201


@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
def atualizar_dados_colaborador(id_colaborador):     
    dados_requisicao = request.get_json()
    
    for colaborador in dados_requisicao:
        if colaborador['id'] == id_colaborador:
            colaborador_encontrado = colaborador
            break
    
    if 'nome' in dados_requisicao:
        colaborador_encontrado['nome'] = dados_requisicao['nome']
    
    if 'cargo' in dados_requisicao:
        colaborador_encontrado['cargo'] = dados_requisicao['cargo']
    
    if 'cracha' in dados_requisicao:
        colaborador_encontrado['cracha'] = dados_requisicao['cracha']
    
    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200


@bp_colaborador.route('/login', methods=['POST'])
def login():
    dados_requisicao = request.get_json()
    
    email = dados_requisicao['email']
    senha = dados_requisicao['senha']
    
    if not email or not senha:
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
    
    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar()
    
    if not colaborador:
        return jsonify({'mensagem': 'Usuario não encontrado'}), 404
    
    
    colaborador = colaborador.to_dict()
    if email == colaborador.get('email') and checar_senha(senha, colaborador.get('senha')):
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas'}), 401