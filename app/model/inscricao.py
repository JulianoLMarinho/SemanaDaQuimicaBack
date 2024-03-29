from typing import List, Optional
from pydantic import BaseModel


class InscricaoCreate(BaseModel):
    edicao_semana_id: int
    status: str
    usuario_id: int
    valor: float
    camisa_kit: bool
    cotista_sbq: bool


class Inscricao(InscricaoCreate):
    id: Optional[int]
    numero_comprovante: Optional[str]
    titular_comprovante: Optional[str]
    id_comprovante: Optional[str]
    nome: Optional[str]
    email: Optional[str]
    numero_edicao: Optional[str]


class InscricaoAtividades(Inscricao):
    atividades: List[int]


class InformarPagamento(BaseModel):
    inscricao_id: int
    numero_documento: str
    titular_comprovante: str
    id_comprovante: str


class AtividadeUsuario(BaseModel):
    atividade_id: int
    inscricao_id: int
    status: str
    camisa_kit: bool
    cotista_sbq: bool


class AlunoAtividade(BaseModel):
    inscricao_id: int
    edicao_semana_id: int
    aluno_nome: str
    aluno_email: str
    atividade_titulo: str
