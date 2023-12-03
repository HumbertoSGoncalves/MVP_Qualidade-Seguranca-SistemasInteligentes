from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.paciente import Paciente
from model.modelo import Model

db_path = "database/"
# Verifica se o diretorio é existente
if not os.path.exists(db_path):
    # cria o diretorio se necessário
   os.makedirs(db_path)

# url de acesso ao banco de dados local
db_url = 'sqlite:///%s/pacientes.sqlite3' % db_path

# realiza a conexão com o banco
engine = create_engine(db_url, echo=False)

# Instanciamento para criação de seção com o banco de dados local
Session = sessionmaker(bind=engine)

# criação do banco caso ele não exista
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)