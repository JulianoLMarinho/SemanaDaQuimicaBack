from typing import List
from xmlrpc.client import boolean
from pydantic import BaseModel


class Presenca(BaseModel):
    inscricao_atividade_id: int
    dia: int
    inteira: boolean
    meia: boolean


class AlunoPresenca(BaseModel):
    id: int
    nome: str
    atividade_id: int
    presencas: List[Presenca]
