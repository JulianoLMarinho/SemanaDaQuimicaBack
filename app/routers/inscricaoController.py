from typing import List
from fastapi import APIRouter, Depends

from app.dependencies import get_current_active_user
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, InformarPagamento, Inscricao, InscricaoAtividades
from app.services.inscricaoService import InscricaoService


router = APIRouter()
prefix = '/inscricao'
tags = ['Inscrição']


@router.post("", dependencies=[Depends(get_current_active_user)])
async def adicionarInscricao(
    inscricao: InscricaoAtividades,
    service: InscricaoService = Depends()
):
    await service.criarInscricao(inscricao)


@router.put("/pagamento", dependencies=[Depends(get_current_active_user)])
async def informarPagamento(
    documento: InformarPagamento,
    service: InscricaoService = Depends()
):
    await service.informarPagamento(documento.inscricao_id, documento.numero_documento)


@router.delete("/{inscricaoId}", dependencies=[Depends(get_current_active_user)])
async def cancelarInscricao(
    inscricaoId: int,
    service: InscricaoService = Depends()
):
    await service.cancelarInscricao(inscricaoId)


@router.get("/confirmacao", dependencies=[Depends(get_current_active_user)], response_model=List[Inscricao])
async def obterInscricoes(
    service: InscricaoService = Depends()
):
    return await service.obterInscricoesConfirmacao()


@router.put("/confirmacao/{inscricao_id}", dependencies=[Depends(get_current_active_user)])
async def confirmarInscricao(
    inscricao_id: int,
    service: InscricaoService = Depends()
):
    await service.confirmarInscricao(inscricao_id)


@router.get("/total-pagamento-informado", dependencies=[Depends(get_current_active_user)])
async def totalInscricoesPagamentoInformado(
    service: InscricaoService = Depends()
):
    return await service.totalInscricoesPagamentoInformado()


@router.get("/{usuarioId}", dependencies=[Depends(get_current_active_user)], response_model=List[AtividadeUsuario])
async def obterAtividadesUsuario(
    usuarioId: int,
    service: InscricaoService = Depends()
):
    return await service.obterAtividadesUsuario(usuarioId)


@router.get("/{usuarioId}/resumo", dependencies=[Depends(get_current_active_user)], response_model=List[Inscricao])
async def obterInscricoes(
    usuarioId: int,
    service: InscricaoService = Depends()
):
    return await service.obterInscricoes(usuarioId)


@router.get("/atividade/usuario/{inscricaoId}", dependencies=[Depends(get_current_active_user)], response_model=List[Atividade])
async def obterAtividade(
    inscricaoId: int,
    service: InscricaoService = Depends()
):
    return await service.obterAtividade(inscricaoId)
