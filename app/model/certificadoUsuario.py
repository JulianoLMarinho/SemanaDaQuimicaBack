from datetime import date, datetime, time, timedelta
from pydantic import BaseModel
from sqlalchemy import Interval


class CertificadoUsuario(BaseModel):
    id: int
    numero_edicao: int
    cod_tipo: str
    data_inicio: date
    data_fim: date
    tema: str
    titulo: str
    percentual_presenca: float
    duracao_atividade: timedelta
