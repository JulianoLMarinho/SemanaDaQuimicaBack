from fastapi import APIRouter, Depends

from app.model.coresEdicao import CoresEdicaoCreate
from app.services.coresEdicaoService import CoresEdicaoService


router = APIRouter()
prefix = '/cores-edicao'
tags = ['Cores Edição']


@router.post("")
def salvarCoresEdicao(
    coresEdicao: CoresEdicaoCreate,
    service: CoresEdicaoService = Depends()
):
    service.salvarCoresEdicao(coresEdicao)


@router.get("/{edicaoId}", response_model=CoresEdicaoCreate)
def obterCoresEdicao(
    edicaoId: int,
    service: CoresEdicaoService = Depends()
):
    return service.obterCoresEdicao(edicaoId)
