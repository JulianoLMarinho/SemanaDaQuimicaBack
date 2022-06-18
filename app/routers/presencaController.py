from fastapi import APIRouter, Depends

from app.dependencies import get_current_active_user
from app.model.presenca import Presenca
from app.services.presencaService import PresencaService


router = APIRouter()
prefix = '/presenca'
tags = ['Presença']


@router.get("/{atividadeId}", dependencies=[Depends(get_current_active_user)])
def getAlunosPresenca(
    atividadeId: int,
    service: PresencaService = Depends()
):
    return service.getAlunosPresenca(atividadeId)


@router.put("", dependencies=[Depends(get_current_active_user)])
def salvarPresenca(
    presenca: Presenca,
    service: PresencaService = Depends()
):
    service.salvarPresenca(presenca)
