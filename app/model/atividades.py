from datetime import time
from typing import List, Optional
from pydantic import BaseModel, Extra
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from app.model.turno import TurnoComHorarios

Base = declarative_base()


class AtividadeCreate(BaseModel):
    edicao_semana_id: int
    ativa: bool
    tipo_atividade: int
    descricao_atividade: Optional[str]
    vagas: Optional[int]
    titulo: str
    valor: Optional[float]


class DiaHoraAtividade(BaseModel, extra=Extra.ignore):
    hora_inicio: time
    hora_fim: time
    dia: int
    atividade_edicao_id: Optional[int]
    turno_id: Optional[int]


class Atividade(AtividadeCreate):
    id: Optional[int]


class AtividadeCreateComHorarioResponsavel(Atividade):
    horarios: Optional[List[DiaHoraAtividade]]
    turno_atividade: Optional[int]
    responsavel_atividade: List[int]


class ResponsavelAtividade(BaseModel):
    id: int
    id_atividade: int
    nome_responsavel: str
    descricao_responsavel: str
    id_lattes: str
    foto: Optional[str]
    pagina_url: Optional[str]
    twitter: Optional[str]
    instagram: Optional[str]
    facebook: Optional[str]


class AtividadeLista(BaseModel):
    id: int
    titulo: str
    ativa: bool
    descricao_atividade: Optional[str]
    vagas: Optional[int]
    nome_tipo: Optional[str]
    tipo_atividade: Optional[int]
    nome_turno: Optional[str]
    turno_id: Optional[int]
    responsaveis: Optional[List[ResponsavelAtividade]]
    horarios: Optional[List[DiaHoraAtividade]]
    aceita_inscricao: bool
    valor: Optional[float]
    total_inscritos: Optional[int]


class TipoAtividade(BaseModel):
    id: int
    nome_tipo: str
    descricao_tipo: str
    cod_tipo: str


class TurnoAtividade(BaseModel):
    turno_id: int
    turno: TurnoComHorarios
    atividades: List[AtividadeLista]


class AtividadeORM(Base):
    __tablename__ = 'atividade_edicao'

    id = Column(Integer, primary_key=True)
    edicao_semana_id = Column(Integer)
    ativa = Column(Boolean)
    tipo_atividade = Column(Integer)
    dia_hora_atividade_id = Column(Integer)
    descricao_atividade = Column(String)
    responsavel_atividade = Column(Integer)
    vagas = Column(Integer)

    def __repr__(self):
        return f'Atividade {self.descricao_atividade}'
