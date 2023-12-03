from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente
import json
import numpy as np

class PacienteSchema(BaseModel):
    """ Define a representação para a inclusão de um novo paciente
    """
    name: str = "Corey"
    rad: float = 6.2
    tex: float = 148.3
    per: float = 72.5
    area: float = 35.6
    smooth: float = 2.8
    
class PacienteViewSchema(BaseModel):
    """Define o retorno dos dados do paciente
    """
    id: int = 1
    name: str = "Corey"
    rad: float = 6.2
    tex: float = 148.3
    per: float = 72.5
    area: float = 35.6
    smooth: float = 2.8
    diagnosis: int = None
    
class PacienteBuscaSchema(BaseModel):
    """Define a estrutura que representa o resultado da busca.
    Realizada através do nome do paciente.
    """
    name: str = "Corey"

class ListaPacientesSchema(BaseModel):
    """Representação de uma lista de pacientes
    """
    pacientes: List[PacienteSchema]

    
class PacienteDelSchema(BaseModel):
    """Representação de um paciente a ser removido
    """
    name: str = "Corey"
    
# Retorna somente os dados de um paciente.  
def apresenta_paciente(paciente: Paciente):
    """ Representação do paciente de acordo com o schema definido em
        PacienteViewSchema.
    """
    return {
        "id": paciente.id,
        "name": paciente.name,
        "rad": paciente.rad,
        "tex": paciente.tex,
        "per": paciente.per,
        "area": paciente.area,
        "smooth": paciente.smooth,
        "diagnosis": paciente.diagnosis
    }
    
# Exibe a lista de pacientes
def apresenta_pacientes(pacientes: List[Paciente]):
    """ Representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    result = []
    for paciente in pacientes:
        result.append({
        "id": paciente.id,
        "name": paciente.name,
        "rad": paciente.rad,
        "tex": paciente.tex,
        "per": paciente.per,
        "area": paciente.area,
        "smooth": paciente.smooth,
        "diagnosis": paciente.diagnosis
        })

    return {"pacientes": result}

