from pydantic import BaseModel


class CoresEdicaoCreate(BaseModel):
    edicao_semana_id: int
    cor1: str
    cor2: str
    cor3: str
    cor4: str
    cor5: str
    cor6: str


class CoresEdicao(CoresEdicaoCreate):
    id: int
