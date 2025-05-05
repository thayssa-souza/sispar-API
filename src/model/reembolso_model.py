from src.model import db
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DECIMAL, Integer, DATE
from sqlalchemy.orm import func

class Reembolso(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador = Column(String(150), nullable=False)
    empresa = Column(String(50), nullable=False)
    num_prestacao = Column(Integer, nullable=False)
    descricao = Column(String(200)) # no site, a descrição é uma imagem da NF, mas aqui vamos considerar que será uma URL
    data = Column(DATE, server_default=func.current_date(), nullable=False) # constraint server_default: caso não passe a data, o padrão será a data atual
    tipo_reembolso = Column(String(35))
    centro_custo = Column(String(50), nullable=False)
    ordem_interna = Column(String(50))
    divisao = Column(String(50))
    pep = Column(String(50)) # regra de negócio: caso preencha ordem_interna e divisão, pep não pode ser preenchido e vice-versa
    moeda = Column(String(20), nullable=False)
    distancia_km = Column(String(50)) # pode fazer uma funcionalidade ou uma trigger para calcular o valor_faturado = distancia_km * valor_km isso se distancia_km e valor_km nao forem null; se for trigger, tem que apresentar no dia da entrega
    valor_km = Column(String(50))
    valor_faturado = Column(DECIMAL(10, 2), nullable=False)
    despesa = Column(DECIMAL(10, 2))
    id_colaborador = Column(Integer, ForeignKey(column='colaborador.id'), nullable=False) # quem criou o reembolso e não necessariamente é a mesma pessoa que será reembolsada, já que o reembolso pode ser para outra pessoa
    status = Column(String(25))
    
    def __init__(self, colaborador, empresa, num_prestacao, descricao, data, tipo_reembolso, centro_custo, ordem_interna, divisao, pep, moeda, distancia_km, valor_km, valor_faturado, despesa, id_colaborador, status='Em análise'):
        self.colaborador = colaborador
        self.empresa = empresa
        self.num_prestacao = num_prestacao
        self.descricao = descricao
        self.data = data
        self.tipo_reembolso = tipo_reembolso
        self.centro_custo = centro_custo
        self.ordem_interna = ordem_interna
        self.divisao = divisao
        self.pep = pep
        self.moeda = moeda
        self.distancia_km = distancia_km
        self.valor_km = valor_km
        self.valor_faturado = valor_faturado
        self.despesa = despesa
        self.id_colaborador = id_colaborador
        self.status = status