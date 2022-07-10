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
    aceita_inscricao_atividade: bool
    site_em_construcao: bool
    logo: Optional[str]
    logo_completa: Optional[str]
    presidente_edicao: Optional[str]
    assinatura_presidente_edicao: Optional[str]
    direcao_instituto: Optional[str]
    assinatura_direcao_instituto: Optional[str]


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


class EdicaoLogo(BaseModel):
    edicao_semana_id: int
    logo: str
    tipo_logo: str


class Assinatura(BaseModel):
    edicao_semana_id: int
    tipo_assinatura: str
    assinatura: str
    nome: str
