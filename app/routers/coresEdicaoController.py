from fastapi import APIRouter, Depends

from app.model.coresEdicao import CoresEdicaoCreate
from app.services.coresEdicaoService import CoresEdicaoService


router = APIRouter()
prefix = '/cores-edicao'
tags = ['Cores Edição']


@router.post("")
async def salvarCoresEdicao(
    coresEdicao: CoresEdicaoCreate,
    service: CoresEdicaoService = Depends()
):
    await service.salvarCoresEdicao(coresEdicao)


@router.get("/{edicaoId}", response_model=CoresEdicaoCreate)
async def obterCoresEdicao(
    edicaoId: int,
    service: CoresEdicaoService = Depends()
):
    return await service.obterCoresEdicao(edicaoId)
