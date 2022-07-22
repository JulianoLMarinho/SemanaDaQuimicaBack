
from typing import List
from fastapi import APIRouter, Depends
from app.dependencies import current_user_is_admin
from app.model.comum import OpcaoSelecao

from app.model.turno import Turno, TurnoComHorarios, TurnoCriacao, TurnoCriacaoComHorario
from app.services.turnoService import TurnoService


router = APIRouter()
prefix = '/turnos'
tags = ['Turnos']


@router.get('/{EdicaoId}', response_model=List[TurnoComHorarios])
def getByEdicao(
    EdicaoId: int,
    service: TurnoService = Depends()
):
    return service.obterTurnosComHorario(EdicaoId)


@router.post('', response_model=bool, dependencies=[Depends(current_user_is_admin)])
def criarEditarTurno(
    turno: TurnoCriacaoComHorario,
    service: TurnoService = Depends()
):
    if turno.id != None:
        return service.editarTurno(turno)
    else:
        return service.criarTurno(turno)


@router.get('/turnos-selecao/{edicaoId}', response_model=List[OpcaoSelecao])
def obterTurnosSelecaoByEdicao(
    edicaoId: int,
    service: TurnoService = Depends()
):
    return service.obterTurnosSelecaoByEdicao(edicaoId)
