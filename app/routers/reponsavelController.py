from typing import List
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user
from app.model.comum import OpcaoSelecao

from app.model.responsavel import Responsavel
from app.services.atividadesService import AtividadesService
from app.services.responsavelService import ResponsavelService

router = APIRouter()
prefix = '/responsavel'
tags = ['Responsavel']


@router.get("", response_model=List[OpcaoSelecao])
def obterTodosResponsaveis(
    service: ResponsavelService = Depends()
):
    return service.obterTodosResponsaveis()


@router.get("/getAll", response_model=List[Responsavel])
def obterResponsaveis(
    service: ResponsavelService = Depends()
):
    return service.obterResponsaveis()


@router.get("/atividade/{atividadeId}", dependencies=[Depends(get_current_active_user)])
def getResponsaveisByAtividade(
    atividadeId: int,
    service: AtividadesService = Depends()
):
    return service.getResponsaveisByAtividade(atividadeId)


@router.post("", dependencies=[Depends(get_current_active_user)])
def salvarEditarResponsavel(
    responsavel: Responsavel,
    service: ResponsavelService = Depends()
):
    if responsavel.id != None:
        service.atualizarResponsavel(responsavel)
    else:
        service.salvarNovoResponsavel(responsavel)
