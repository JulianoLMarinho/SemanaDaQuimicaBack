from typing import Optional
from pydantic import BaseModel

from app.model.usuario import Usuario


class AuthResponseBody(BaseModel):
    usuario: Optional[Usuario]
    responseType: str
    access_token: Optional[str]
