from src.model import db # traz a instancia do SQLAlchemy para este arquivo
from sqlalchemy.schema import Column # traz o recurso necessário para o ORM entender que o atributo será uma coluna na tabela
from sqlalchemy.types import String, DECIMAL, Integer # traz os tipos de dados que serão utilizados no banco de dados

class Colaborador(db.Model):
    ### Atributos > vão virar colunas na tabela - é a forma do bolo ###
    id = Column(Integer, primary_key=True, autoincrement=True) # Integer
    nome = Column(String(100)) # Varchar
    email = Column(String(100))
    senha = Column(String(50))
    cargo = Column(String(100))
    salario = Column(DECIMAL(10, 2)) # Float - até 10 dígitos, sendo 2 após a vírgula (ex: 12345678.90)

    ## Construtor > vai criar um objeto baseado no model definido acima - é a o forno do bolo, que vai entregar o forno pronto ##
    # O construtor é o método que vai ser chamado quando instanciamos um objeto
    def __init__(self, nome, email, senha, cargo, salario): # não precisa ser o mesmo nome do atributo, mas é uma boa prática
        # self = this, ou seja, o objeto que está sendo instanciado
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.salario = salario
        # self.id = id # não precisa, pois o banco de dados vai gerar automaticamente o id (autoincremento)


    def to_dict(self) -> dict: # Indica que o retorno do método é um dicionário
        # Método que vai transformar o objeto em um dicionário, para facilitar a conversão em JSON
        return {
            'email': self.email,
            'senha': self.senha
        }
        # vai trabalhar apenas com o que adicionamos no return(), podemos adicionar os demais que não tem problema, mas só vai retornar o que está no return
    
    
    def all_data(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cargo': self.cargo,
            'salario': self.salario
        }