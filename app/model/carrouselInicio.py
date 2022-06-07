import base64
from pydantic import BaseModel


class CarrouselInicio(BaseModel):
    id: int
    edicao_semana_id: int
    imagem: str
