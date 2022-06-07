from pydantic import BaseModel


class OpcaoSelecao(BaseModel):
    value: int
    name: str
