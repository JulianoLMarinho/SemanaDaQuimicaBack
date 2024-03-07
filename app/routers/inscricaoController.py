import asyncio
from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends

from app.dependencies import current_user_is_admin, get_current_active_user
from app.model.atividades import Atividade
from app.model.inscricao import AlunoAtividade, AtividadeUsuario, InformarPagamento, Inscricao, InscricaoAtividades
from app.model.tabelas import InscricoesEdicao
from app.model.usuario import NomeEmail
from app.repository.atividadesRepository import AtividadesRepository
from app.repository.coresEdicaoRepository import CoresEdicaoRepository
from app.repository.edicaoSemanaRepository import EdicaoSemanaRepository
from app.repository.inscricaoRepository import InscricaoRepository
from app.repository.responsavelRepository import ResponsavelRepository
from app.services.coresEdicaoService import CoresEdicaoService
from app.services.edicaoSemanaService import EdicaoSemanaService
from app.services.emailService import EmailService
from app.services.inscricaoService import InscricaoService
from fastapi_utils.tasks import repeat_every
from app.services.responsavelService import ResponsavelService
from app.sql.connections import MainConnection

from app.sql.database import dbEngine


router = APIRouter()
prefix = '/inscricao'
tags = ['Inscrição']

lock = asyncio.Lock()


@router.post("")
async def adicionarInscricao(
    inscricao: InscricaoAtividades,
    background_task: BackgroundTasks,
    service: InscricaoService = Depends(),
    usuario=Depends(get_current_active_user),
):
    inscricaoId = await service.criarInscricao(inscricao, lock)
    if (isinstance(inscricaoId, list)):
        return inscricaoId
    background_task.add_task(
        service.enviarEmailConfirmacaoInscricao, usuario['email'], inscricaoId)


@router.put("/pagamento", dependencies=[Depends(get_current_active_user)])
def informarPagamento(
    documento: InformarPagamento,
    service: InscricaoService = Depends()
):
    service.informarPagamento(documento.inscricao_id,
                              documento.numero_documento,
                              documento.titular_comprovante,
                              documento.id_comprovante)


@router.delete("/{inscricaoId}", dependencies=[Depends(get_current_active_user)])
def cancelarInscricao(
    inscricaoId: int,
    background_task: BackgroundTasks,
    service: InscricaoService = Depends()
):
    service.cancelarInscricao(inscricaoId)
    background_task.add_task(
        service.enviarEmailCancelamentoInscricao, inscricaoId)


@router.get("/confirmacao", dependencies=[Depends(current_user_is_admin)], response_model=List[Inscricao])
def obterInscricoes(
    service: InscricaoService = Depends()
):
    return service.obterInscricoesConfirmacao()


@router.put("/confirmacao/{inscricao_id}", dependencies=[Depends(current_user_is_admin)])
def confirmarInscricao(
    inscricao_id: int,
    background_task: BackgroundTasks,
    service: InscricaoService = Depends()
):
    service.confirmarInscricao(inscricao_id)
    background_task.add_task(
        service.enviarEmailConfirmacaoPagamentoInscricao, inscricao_id)


@router.get("/total-pagamento-informado", dependencies=[Depends(current_user_is_admin)])
def totalInscricoesPagamentoInformado(
    service: InscricaoService = Depends()
):
    return service.totalInscricoesPagamentoInformado()


@router.get("/usuarios/{atividadeId}", dependencies=[Depends(current_user_is_admin)], response_model=List[NomeEmail])
def obterInscricoesPorAtividade(
    atividadeId: int,
    service: InscricaoService = Depends()
):
    return service.obterInscricoesPorAtividade(atividadeId)


@router.get("/{usuarioId}", dependencies=[Depends(get_current_active_user)], response_model=List[AtividadeUsuario])
def obterAtividadesUsuario(
    usuarioId: int,
    edicaoSemana: Optional[int] = None,
    service: InscricaoService = Depends()
):
    return service.obterAtividadesUsuario(usuarioId, edicaoSemana)


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


@router.get("/inscritos/edicao/{edicaoId}", dependencies=[Depends(current_user_is_admin)], response_model=List[InscricoesEdicao])
def obterInscricoesPorEdicao(
    edicaoId: int,
    service: InscricaoService = Depends()
):
    return service.obterInscricoesPorEdicao(edicaoId)


@router.get("/primeiro-curso/{EdicaoId}", dependencies=[Depends(current_user_is_admin)])
def obterAlunosPrimeiroCurso(
    EdicaoId: int,
    service: InscricaoService = Depends()
):
    return service.obterAlunosPrimeiroCurso(EdicaoId)


@router.get("/tamanho-camisas/{EdicaoId}", dependencies=[Depends(current_user_is_admin)])
def tamanhoCamisaUsuarioInscrito(
    EdicaoId: int,
    service: InscricaoService = Depends()
):
    return service.tamanhoCamisaUsuarioInscrito(EdicaoId)


@router.get("/inscritos-atividades-edicao/{edicao_id}", dependencies=[Depends(current_user_is_admin)], response_model=List[AlunoAtividade])
def obterAtividadesAlunos(
    edicao_id: int,
    atividade_id: Optional[int] = None,
    service: InscricaoService = Depends()
):
    return service.obterAtividadesAlunos(edicao_id, atividade_id)


@router.on_event("startup")
@repeat_every(seconds=60 * 60)
async def cancelarInscricoesPendentesPagamento():
    conn = dbEngine._db_engine.connect()
    service = InscricaoService(
        repo=InscricaoRepository(conn),
        atividadeRepo=AtividadesRepository(conn),
        emailService=EmailService(edicaoSemanaService=EdicaoSemanaService(repository=EdicaoSemanaRepository(
            conn), responsavelService=ResponsavelService(ResponsavelRepository(conn))), coresEdicaoService=CoresEdicaoService(CoresEdicaoRepository(conn)))
    )
    inscricoes = service.obterInscricoesAguardandoPagamento3Dias()
    for inscricao in inscricoes:
        service.cancelarInscricao(inscricao.id)
        service.enviarEmailCancelamentoInscricao3Dias(inscricao.id)
    conn.close()
