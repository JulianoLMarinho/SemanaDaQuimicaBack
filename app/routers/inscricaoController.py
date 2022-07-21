from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends

from app.dependencies import get_current_active_user
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, InformarPagamento, Inscricao, InscricaoAtividades
from app.services.inscricaoService import InscricaoService


router = APIRouter()
prefix = '/inscricao'
tags = ['Inscrição']


@router.post("")
def adicionarInscricao(
    inscricao: InscricaoAtividades,
    background_task: BackgroundTasks,
    service: InscricaoService = Depends(),
    usuario=Depends(get_current_active_user),
):
    inscricaoId = service.criarInscricao(inscricao)
    background_task.add_task(
        service.enviarEmailConfirmacaoInscricao, usuario['email'], inscricaoId)


@router.put("/pagamento", dependencies=[Depends(get_current_active_user)])
def informarPagamento(
    documento: InformarPagamento,
    service: InscricaoService = Depends()
):
    service.informarPagamento(documento.inscricao_id,
                              documento.numero_documento)


@router.delete("/{inscricaoId}", dependencies=[Depends(get_current_active_user)])
def cancelarInscricao(
    inscricaoId: int,
    background_task: BackgroundTasks,
    service: InscricaoService = Depends()
):
    service.cancelarInscricao(inscricaoId)
    background_task.add_task(
        service.enviarEmailCancelamentoInscricao, inscricaoId)


@router.get("/confirmacao", dependencies=[Depends(get_current_active_user)], response_model=List[Inscricao])
def obterInscricoes(
    service: InscricaoService = Depends()
):
    return service.obterInscricoesConfirmacao()


@router.put("/confirmacao/{inscricao_id}", dependencies=[Depends(get_current_active_user)])
def confirmarInscricao(
    inscricao_id: int,
    background_task: BackgroundTasks,
    service: InscricaoService = Depends()
):
    service.confirmarInscricao(inscricao_id)
    background_task.add_task(
        service.enviarEmailConfirmacaoPagamentoInscricao, inscricao_id)


@router.get("/total-pagamento-informado", dependencies=[Depends(get_current_active_user)])
def totalInscricoesPagamentoInformado(
    service: InscricaoService = Depends()
):
    return service.totalInscricoesPagamentoInformado()


@router.get("/{usuarioId}", dependencies=[Depends(get_current_active_user)], response_model=List[AtividadeUsuario])
def obterAtividadesUsuario(
    usuarioId: int,
    service: InscricaoService = Depends()
):
    return service.obterAtividadesUsuario(usuarioId)


@router.get("/{usuarioId}/resumo", dependencies=[Depends(get_current_active_user)], response_model=List[Inscricao])
def obterInscricoes(
    usuarioId: int,
    service: InscricaoService = Depends()
):
    return service.obterInscricoes(usuarioId)


@router.get("/atividade/usuario/{inscricaoId}", dependencies=[Depends(get_current_active_user)], response_model=List[Atividade])
def obterAtividade(
    inscricaoId: int,
    service: InscricaoService = Depends()
):
    return service.obterAtividade(inscricaoId)
