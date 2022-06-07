from typing import List, Optional
from pydantic import BaseModel


class InscricaoCreate(BaseModel):
    edicao_semana_id: int
    status: str
    usuario_id: int
    valor: float


class Inscricao(InscricaoCreate):
    id: Optional[int]
    numero_comprovante: Optional[str]


class InscricaoAtividades(Inscricao):
    atividades: List[int]


class InformarPagamento(BaseModel):
    inscricao_id: int
    numero_documento: str


class AtividadeUsuario(BaseModel):
    atividade_id: int
    inscricao_id: int
    status: str
