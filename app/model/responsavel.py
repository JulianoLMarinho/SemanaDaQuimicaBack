from typing import Optional
from pydantic import BaseModel


class ResponsavelCreate(BaseModel):
    nome_responsavel: str
    descricao_responsavel: str
    id_lattes: str
    foto: Optional[str]
    pagina_url: Optional[str]
    twitter: Optional[str]
    instagram: Optional[str]
    facebook: Optional[str]


class Responsavel(ResponsavelCreate):
    id: Optional[int]
