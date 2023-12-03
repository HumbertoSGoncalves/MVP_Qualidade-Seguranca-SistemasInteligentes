from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente, Model
from logger import logger
from schemas import *
from flask_cors import CORS

import joblib


# Criando a instância do objeto OpenAPI.
info = Info(title="API de Predição", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Estabelecendo tags para a categorização das rotas
home_tag = Tag(name="Documentação", description="Escolha de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Inclusão, visualização, exclusão e previsão de pacientes diagnosticados com câncer de mama")


# Endpoint principal
@app.get('/', tags=[home_tag])
def home():
    """Encaminha para a página /openapi, onde é possível selecionar o formato de documentação desejado.
    """
    return redirect('/openapi')


# Endpoint de listagem de pacientes
@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_pacientes():
    """Recupera todos os pacientes registrados na base de dados.
        Retorna uma lista contendo os pacientes cadastrados.
        Argumento: nome (str): nome do paciente
        Retorna: lista de pacientes cadastrados
    """
    session = Session()
    
    # Retorna todos os pacientes existentes na base
    pacientes = session.query(Paciente).all()
    
    if not pacientes:
        logger.warning("A base de dados não possui pacientes cadastrados no momento")
        return {"message": "A base de dados não possui pacientes cadastrados no momento"}, 404
    else:
        logger.debug(f"%d pacientes encontrados" % len(pacientes))
        return apresenta_pacientes(pacientes), 200


# Rota para adicionar pacientes e obter diagnósticos
@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PacienteSchema):
    """Inclui um novo paciente na base de dados.
    Retorna uma representação dos pacientes e seus diagnósticos associados.
    
    Argumentos:
        name (str): nome do paciente
        rad (float): tamanho médio do raio da mama
        tex (float): textura média da mama
        per (float): tamanho médio do perímetro da mama
        area (float): área média da mama
        smooth (float): nível de suavidade da mama
        
    Retorna:
        Descrição ou representação do paciente juntamente com o diagnóstico associado.
    """
    
    # Carregando o modelo treinado
    ml_path = 'ml_model/breast_model.pkl'
    modelo = Model.carrega_modelo(ml_path)
    
    # Carregando scaler para ajustar os valores a serem inseridos no modelo treinado
    scaler_path = 'ml_model/scaler.pkl'
    scaler = joblib.load(scaler_path)
    
    # Padronizando os dados de entrada para o modelo SVM-padronizado
    dados_paciente = [[form.rad, form.tex, form.per, form.area, form.smooth]]
    dados_paciente_padronizados = scaler.transform(dados_paciente)
    
    # Predição de classes dos dados de entrada
    diagnostico = modelo.predict(dados_paciente_padronizados)
    
    paciente = Paciente(
        name=form.name.strip(),
        rad=form.rad,
        tex=form.tex,
        per=form.per,
        area=form.area,
        smooth=form.smooth,
        diagnosis=diagnostico[0]
    )
    logger.debug(f"Incluindo: '{paciente.name}'")
    
    try:
        # Estabelecendo conexão com a base de dados.
        session = Session()
        
        # Verificando se paciente é existente na base
        if session.query(Paciente).filter(Paciente.name == form.name).first():
            error_msg = "Paciente já contido na base"
            logger.warning(f"Falha ao incluir '{paciente.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Incluindo paciente
        session.add(paciente)
        # Efetivando a inclusão
        session.commit()
        # Finalizando inclusão
        logger.debug(f"Incluído paciente: '{paciente.name}'")
        return apresenta_paciente(paciente), 200
    
    # Em caso de erro durante a inclusão
    except Exception as e:
        error_msg = "Não foi possível concluir a operação"
        logger.warning(f"Erro ao adicionar '{paciente.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Operações fundamentadas no nome.
# Endpoint de busca de paciente por nome.
@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):    
    """Realiza a pesquisa de um paciente cadastrado na base usando o nome fornecido.

    Argumentos:
        nome (str): nome do paciente.
        
    Retorna:
        Descrição ou representação do paciente e do diagnóstico associado obtidos através da busca.
    """
    
    paciente_nome = query.name
    logger.debug(f"Buscando dados #{paciente_nome}")
    # Estabelecendo conexão com a base de dados
    session = Session()
    # realizando a busca
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
    if not paciente:
        # caso paciente não foi encontrado
        error_msg = f"Paciente {paciente_nome} inexistente."
        logger.warning(f"Erro ao buscar '{paciente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paciente encontrado: '{paciente.name}'")
        # retorna dados existentes
        return apresenta_paciente(paciente), 200
    
# Endpoint para deletar pacientes por nome
@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteViewSchema, "404": ErrorSchema})
def delete_paciente(query: PacienteBuscaSchema):
    """Deleta paciente já existente utilizando do nome deste

    Argumentos:
        nome (str): nome do paciente
        
    Retorna:
        Mensagem de sucesso ou erro
    """
    
    paciente_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre paciente #{paciente_nome}")
    
    # Estabelecendo conexão com a base de dados
    session = Session()
    
    # Buscando paciente
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
    if not paciente:
        error_msg = "Paciente inexistente."
        logger.warning(f"Erro ao performar a operação de deleção de '{paciente_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(paciente)
        session.commit()
        logger.debug(f"Deletado #{paciente_nome}")
        return {"message": f"Sucesso! Paciente {paciente_nome} deletado!"}, 200