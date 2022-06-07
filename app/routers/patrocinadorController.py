from fastapi import APIRouter, Depends

from app.dependencies import get_current_active_user
from app.model.patrocinador import Patrocinador, PatrocinadorCreate
from app.services.patrocinadorService import PatrocinadorService


router = APIRouter()
prefix = '/patrocinador'
tags = ['Patrocinador']


@router.post("", dependencies=[Depends(get_current_active_user)])
async def salvarPatrocinador(
    patrocinador: PatrocinadorCreate,
    service: PatrocinadorService = Depends()
):
    await service.salvarNovoPatrocinador(patrocinador)


@router.get("/{edicaoId}")
async def obterPatrocindorEdicao(
    edicaoId: int,
    service: PatrocinadorService = Depends()
):
    return await service.obterPatrocindorEdicao(edicaoId)


@router.put("", dependencies=[Depends(get_current_active_user)])
async def atualizarPatrocinador(
    patrocinador: Patrocinador,
    service: PatrocinadorService = Depends()
):
    await service.atualizarPatrocinador(patrocinador)


@router.delete("/{patrocinadorId}", dependencies=[Depends(get_current_active_user)])
async def deletarPatrocinador(
    patrocinadorId: int,
    service: PatrocinadorService = Depends()
):
    await service.deletarPatrocinador(patrocinadorId)
