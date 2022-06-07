from pydantic import BaseModel


class PatrocinadorCreate(BaseModel):
    imagem: str
    nome: str
    link: str
    edicao_semana_id: int
    ordem: int


class Patrocinador(PatrocinadorCreate):
    id: int
