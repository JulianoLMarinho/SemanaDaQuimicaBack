
from typing import Any, List
from xmlrpc.client import Boolean
from fastapi import APIRouter, Depends
from app.dependencies import current_user_is_admin, get_current_active_user
from app.model.atividades import AtividadeCreate, AtividadeCreateComHorarioResponsavel, AtividadeLista, TipoAtividade, TurnoAtividade
from app.model.certificadoUsuario import CertificadoUsuario
from app.model.comum import OpcaoSelecao
from app.model.usuario import Usuario
from app.services.atividadesService import AtividadesService


router = APIRouter()
prefix = '/atividades'
tags = ['Atividades']


@router.get('/tipoAtividade', response_model=List[OpcaoSelecao])
def getTipoAtividade(
    service: AtividadesService = Depends()
):
    return service.tipoAtividades()


@router.get("/inscricao", response_model=List[AtividadeLista])
def getAtividadesByEdicaoInscricao(
    idEdicao: int,
    service: AtividadesService = Depends()
):
    return service.getAtividadesDetalhesByEdicaoAndTipo(idEdicao, ['CURSO', 'WORKSHOP', 'VISITA_TECNICA'])


@router.get("/atividades-certificado", response_model=List[AtividadeLista])
def getAtividadesCertificadosByEdicaoInscricao(
    idEdicao: int,
    service: AtividadesService = Depends()
):
    return service.getAtividadesDetalhesByEdicaoAndTipo(idEdicao, ['CURSO', 'WORKSHOP', 'VISITA_TECNICA', 'PALESTRA'])


@router.get("/lista-certificados", response_model=List[CertificadoUsuario])
def obterListaCertificadosUsuario(
    service: AtividadesService = Depends(),
    usuario: Usuario = Depends(get_current_active_user)
):
    return service.obterListaCertificadosUsuario(usuario['id'])


@router.get("/{idEdicao}", response_model=List[AtividadeLista])
def getAtividadesByEdicao(
    idEdicao: int,
    service: AtividadesService = Depends()
):
    return service.getAtividadesDetalhesByEdicao(idEdicao)


@router.get("/{idEdicao}/{tipoAtividade}", response_model=List[AtividadeLista])
def getAtividadesByEdicaoAndTipo(
    idEdicao: int,
    tipoAtividade: str,
    service: AtividadesService = Depends()
):
    return service.getAtividadesDetalhesByEdicaoAndTipo(idEdicao, [tipoAtividade])


@router.get("/turno/{idEdicao}/{tipoAtividade}", response_model=List[TurnoAtividade])
def getAtividadesByEdicaoAndTipo(
    idEdicao: int,
    tipoAtividade: str,
    service: AtividadesService = Depends()
):
    return service.getAtividadesDetalhesByEdicaoTurnoAndTipo(idEdicao, tipoAtividade)


@router.put("", response_model=Boolean, dependencies=[Depends(current_user_is_admin)])
def criarAtividade(
    atividade: AtividadeCreateComHorarioResponsavel,
    service: AtividadesService = Depends()
):
    if (atividade.id):
        service.atualizarAtividade(atividade)
    else:
        return service.criarAtividade(atividade)


@router.post("", dependencies=[Depends(current_user_is_admin)])
def atualizarAtividade(
    atividade: AtividadeCreateComHorarioResponsavel,
    service: AtividadesService = Depends()
):
    service.atualizarAtividade(atividade)
