from typing import Optional
from pydantic import BaseModel


class ResponsavelCreate(BaseModel):
    nome_responsavel: str
    descricao_responsavel: Optional[str]
    id_lattes: Optional[str]
    foto: Optional[str]
    pagina_url: Optional[str]
    twitter: Optional[str]
    instagram: Optional[str]
    facebook: Optional[str]
    tipo: str
    funcao_semana: Optional[str]


class ComissaoCreate(ResponsavelCreate):
    edicao_semana_id: int


class Responsavel(ResponsavelCreate):
    id: Optional[int]
