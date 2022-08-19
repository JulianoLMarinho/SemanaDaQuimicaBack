from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AvisoCreate(BaseModel):
    titulo: str
    texto: str
    edicao_semana_id: int


class Aviso(AvisoCreate):
    id: Optional[int]


class AvisoNotificacao(Aviso):
    data_criacao: datetime


class FiltroAviso(BaseModel):
    data_criacao: datetime
    edicao_semana_id: int
