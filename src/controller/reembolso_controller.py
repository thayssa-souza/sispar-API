from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db

bp_colaborador = Blueprint('reembolso', __name__, url_prefix='/reembolso')

@bp_colaborador.route('/todos-reembolsos', methods=['GET'])
def get_todos_reembolsos():
    reembolsos = db.session.execute(
        db.select(Reembolso) 
    ).scalar_all()
    
    reembolsos = [reembolso.all_data() for reembolso in reembolsos] 
    
    return jsonify(reembolsos), 200


@bp_colaborador.route('/adicionar-reembolso', methods=['POST'])
def adicionar_reembolso():
    dados_requisicao = request.get_json()
    
    campos_obrigatorios = ['colaborador', 'empresa', 'num_prestacao', 'data', 'centro_custo', 'moeda', 'valor_faturado', 'id_colaborador']

    for campo in campos_obrigatorios:
        if campo not in dados_requisicao:
            return jsonify({'erro': f'Campo obrigatório ausente: {campo}'}), 400
    
    novo_reembolso = Reembolso(
        colaborador = dados_requisicao['colaborador'],
        empresa = dados_requisicao['empresa'],
        num_prestacao = dados_requisicao['num_prestacao'],
        descricao = dados_requisicao.get('descricao'),
        data = dados_requisicao['data'],
        tipo_reembolso = dados_requisicao.get('tipo_reembolso'),
        centro_custo = dados_requisicao['centro_custo'],
        ordem_interna = dados_requisicao.get('ordem_interna'),
        divisao = dados_requisicao.get('divisao'),
        pep = dados_requisicao.get('pep'),
        moeda = dados_requisicao['moeda'],
        distancia_km = dados_requisicao.get('distancia_km'),
        valor_km = dados_requisicao.get('valor_km'),
        valor_faturado = dados_requisicao['valor_faturado'],
        despesa = dados_requisicao.get('despesa'),
        id_colaborador = dados_requisicao['id_colaborador'],
        status = dados_requisicao.get('status', 'Em análise')
    )
    
    db.session.add(novo_reembolso)
    db.session.commit()
    
    return jsonify({'mensagem': 'Reembolso adicionado com sucesso'}), 201


@bp_colaborador.route('/atualizar-reembolso/<int:id_reembolso>', methods=['PUT'])
def atualizar_dados_reembolso(id_reembolso):     
    dados_requisicao = request.get_json()
    
    reembolso_encontrado = db.session.execute(
        db.select(Reembolso).where(Reembolso.id == id_reembolso)
    ).scalar_one_or_none()

    if reembolso_encontrado is None:
        return jsonify({'erro': 'Reembolso não encontrado'}), 404
    
    for key, value in dados_requisicao.items():
        if hasattr(reembolso_encontrado, key):
            setattr(reembolso_encontrado, key, value)

    db.session.commit()

    return jsonify({'mensagem': 'Dados do reembolso atualizados com sucesso'}), 200