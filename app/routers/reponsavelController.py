from typing import List
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user
from app.model.comum import OpcaoSelecao

from app.model.responsavel import ComissaoCreate, Responsavel
from app.services.atividadesService import AtividadesService
from app.services.responsavelService import ResponsavelService

router = APIRouter()
prefix = '/responsavel'
tags = ['Responsavel']


@router.get("", response_model=List[OpcaoSelecao])
def obterTodosResponsaveis(
    tipo: str = 'responsavel',
    service: ResponsavelService = Depends()
):
    return service.obterTodosResponsaveis(tipo)


@router.get("/getAll", response_model=List[Responsavel])
def obterResponsaveis(
    service: ResponsavelService = Depends()
):
    return service.obterResponsaveis()


@router.get("/comissao/{edicaoSemanaId}", response_model=List[Responsavel])
def obterResponsaveis(
    edicaoSemanaId: int,
    service: ResponsavelService = Depends()
):
    return service.obterComissao(edicaoSemanaId)


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


@router.post("/comissao", dependencies=[Depends(get_current_active_user)])
def salvarComissaoEdicao(
    comissao: ComissaoCreate,
    service: ResponsavelService = Depends()
):
    service.salvarComissao(comissao)


@router.put("/comissao", dependencies=[Depends(get_current_active_user)])
def salvarComissaoEdicao(
    comissao: Responsavel,
    service: ResponsavelService = Depends()
):
    service.atualizarResponsavel(comissao)


@router.delete("/{responsavel_id}", dependencies=[Depends(get_current_active_user)])
def deletarResponsavel(
    responsavel_id: int,
    service: ResponsavelService = Depends()
):
    service.deleteResponsavel(responsavel_id)
    return True
