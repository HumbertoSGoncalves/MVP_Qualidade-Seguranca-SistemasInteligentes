from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Radius, Texture, Perimeter, Area, Smoothness, Diagnostic

class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    name= Column("Name", String(50))
    rad = Column("Radius", Float)
    tex = Column("Texture", Float)
    per = Column("Perimeter", Float)
    area = Column("Area", Float)
    smooth = Column("Smoothness", Float)
    diagnosis = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, name:str, rad:float, tex:float, per:float, area:float,
                 smooth:float, diagnosis:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Paciente

        Argumentos:
        name: nome do paciente
            rad: tamanho médio do raio da mama
            tex: textura média da mama
            per: tamanho médio do perímetro da mama
            area: área média da mama
            smooth: nível de suavidade da mama
            diagnosis: diagnóstico sobre possível câncer de mama
            data_insercao: data que o paciente foi adicionado na base
        """
        self.name=name
        self.rad = rad
        self.tex = tex
        self.per = per
        self.area = area
        self.smooth = smooth
        self.diagnosis = diagnosis

        # se a data não for informada, será o data exata da inserção no sistema
        if data_insercao:
            self.data_insercao = data_insercao