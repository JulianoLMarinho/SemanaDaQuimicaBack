from datetime import time
from typing import List, Optional
from pydantic import BaseModel, Extra
from uvicorn import Config


class TurnoCriacao(BaseModel):
    nome_turno: str
    edicao_semana_id: int


class DiaHoraTurno(BaseModel, extra=Extra.ignore):
    id: int
    hora_inicio: time
    hora_fim: time
    turno_id: Optional[int]
    dia: int


class Turno(TurnoCriacao):
    id: Optional[int]


class DiaHoraAtividade(BaseModel):
    hora_inicio: str
    hora_fim: str
    dia: int
    turno_id: Optional[int]


class TurnoCriacaoComHorario(Turno):
    horarios: List[DiaHoraAtividade]


class TurnoComHorarios(Turno):
    horarios: List[DiaHoraTurno]
