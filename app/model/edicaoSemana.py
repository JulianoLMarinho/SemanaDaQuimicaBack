from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

from app.model.responsavel import Responsavel


class ComissaoEdicao(BaseModel):
    id: int
    edicao_semana_id: int
    nome_responsavel: str
    descricao_responsavel: str
    id_lattes: str


class EdicaoSemanaCreate(BaseModel):
    tema: str
    data_inicio: date
    data_fim: date
    ativa: bool
    quem_somos: Optional[str]
    numero_edicao: int


class EdicaoSemana(EdicaoSemanaCreate):
    id: Optional[int]
    certificado_liberado: bool


class EdicaoSemanaComComissaoIds(EdicaoSemana):
    comissao_edicao: Optional[List[int]]


class EdicaoSemanaComComissao(EdicaoSemana):
    comissao_edicao: Optional[List[Responsavel]]


class CarouselImageCreation(BaseModel):
    edicao_semana_id: int
    imagem: str
    titulo: Optional[str]
    subtitulo: Optional[str]
    ordem: Optional[int]
    link: Optional[str]


class CarouselImage(CarouselImageCreation):
    id: int


class ComissaoEdicao(BaseModel):
    id: int
    edicao_semana_id: int
    nome_responsavel: str
    descricao_responsavel: str
    id_lattes: str
    foto: Optional[str]
    pagina_url: Optional[str]
    twitter: Optional[str]
    instagram: Optional[str]
    facebook: Optional[str]
