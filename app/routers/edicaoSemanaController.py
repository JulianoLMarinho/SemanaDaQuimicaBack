import asyncio
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Request
from sse_starlette import EventSourceResponse
from app.dependencies import current_user_is_admin, get_current_active_user
from ..model.aviso import Aviso, AvisoCreate, AvisoNotificacao, FiltroAviso

from app.model.edicaoSemana import Assinatura, CarouselImage, CarouselImageCreation, ComissaoEdicao, ComoChegar, EdicaoLogo, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaComComissaoIds, FaleConosco, QuemSomos
from app.services.edicaoSemanaService import EdicaoSemanaService


router = APIRouter()
prefix = '/edicaosemana'
tags = ['Edição Semana']


@router.get("", response_model=EdicaoSemanaComComissao)
def getEdicaoSemana(
    id: Optional[int] = None,
    service: EdicaoSemanaService = Depends()
):
    return service.getEdicaoAtiva() if id is None else service.getEdicaoById(id)


@router.put("", dependencies=[Depends(current_user_is_admin)])
def editarEdicaoSemana(
    edicaoSemana: EdicaoSemana,
    service: EdicaoSemanaService = Depends()
):
    return service.editarCriarEdicaoSemana(edicaoSemana)


@router.put("/tema", dependencies=[Depends(current_user_is_admin)])
def updateEdicaoSemana(
    tema: dict,
    service: EdicaoSemanaService = Depends()
):
    service.updateTemaEdicaoAtiva(tema['tema'])


@router.get("/edicoes", dependencies=[Depends(get_current_active_user)], response_model=List[EdicaoSemanaComComissao])
def getEdicoes(
    service: EdicaoSemanaService = Depends()
):
    return service.getEdicoes()


@router.post("/carousel-image", dependencies=[Depends(current_user_is_admin)])
def adicionarCarrousselImage(
    carrousselImage: CarouselImageCreation,
    service: EdicaoSemanaService = Depends()
):
    service.adicionarCarrousselImage(carrousselImage)


@router.post("/aviso", dependencies=[Depends(current_user_is_admin)])
def criarAviso(
    aviso: Aviso,
    service: EdicaoSemanaService = Depends()
):
    service.criarAviso(aviso)
    return True


@router.put("/aviso")
def atualizarAviso(
    aviso: Aviso,
    service: EdicaoSemanaService = Depends()
):
    service.updateAvisoEdicao(aviso)
    return True


@router.get("/stream-results")
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'

    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                yield {
                    "event": "new_message",
                    "id": "message_id",
                    "retry": 15000,
                    "data": "message_content"
                }

            await asyncio.sleep(5)

    return EventSourceResponse(event_generator())


@router.get("/carousel-edicao/{edicaoId}", response_model=List[CarouselImage])
def getCarouselEdicao(
    edicaoId: int,
    service: EdicaoSemanaService = Depends()
):
    return service.getCarouselEdicao(edicaoId)


@router.put("/carousel-image", dependencies=[Depends(current_user_is_admin)])
def editarCarouselImage(
    carouselImage: CarouselImage,
    service: EdicaoSemanaService = Depends()
):
    service.editarCarouselImage(carouselImage)


@router.delete("/carousel-image/{carouselImageId}", dependencies=[Depends(current_user_is_admin)])
def deletarCarouselImage(
    carouselImageId: int,
    service: EdicaoSemanaService = Depends()
):
    service.deletarCarouselImage(carouselImageId)


@router.put("/quem-somos", dependencies=[Depends(current_user_is_admin)])
def salvarQuemSomos(
    quemSomos: QuemSomos,
    service: EdicaoSemanaService = Depends()
):
    service.salvarQuemSomos(quemSomos.quem_somos, quemSomos.edicao_semana_id)


@router.get("/quem-somos/{edicaoSemanaId}", response_model=List[ComissaoEdicao], dependencies=[Depends(get_current_active_user)])
def obterQuemSomos(
    edicaoSemanaId: int,
    service: EdicaoSemanaService = Depends()
):
    return service.obterQuemSomos(edicaoSemanaId)


@router.put("/como-chegar", dependencies=[Depends(current_user_is_admin)])
def salvarComoChegar(
    comoChegar: ComoChegar,
    service: EdicaoSemanaService = Depends()
):
    service.salvarComoChegar(comoChegar.como_chegar,
                             comoChegar.edicao_semana_id)


@router.put("/fale-conosco", dependencies=[Depends(current_user_is_admin)])
def salvarFaleConosco(
    faleConosco: FaleConosco,
    service: EdicaoSemanaService = Depends()
):
    service.salvarFaleConosco(faleConosco.fale_conosco,
                              faleConosco.edicao_semana_id)


@router.put("/liberar-certificado/{edicaoSemanaId}/{liberar}", dependencies=[Depends(current_user_is_admin)])
def liberarCertificados(
    edicaoSemanaId: int,
    liberar: bool,
    service: EdicaoSemanaService = Depends()
):
    service.liberarCertificados(edicaoSemanaId, liberar)


@router.put("/aceitar-inscricao-atividade/{edicaoSemanaId}/{aceitarInscricao}", dependencies=[Depends(current_user_is_admin)])
def aceitarInscricoesAtividades(
    edicaoSemanaId: int,
    aceitarInscricao: bool,
    service: EdicaoSemanaService = Depends()
):
    service.aceitarInscricoesAtividades(edicaoSemanaId, aceitarInscricao)


@router.post("/salvar-logo", dependencies=[Depends(current_user_is_admin)])
def salvarLogo(
    edicaoLogo: EdicaoLogo,
    service: EdicaoSemanaService = Depends()
):
    service.salvarLogo(edicaoLogo)


@router.post("/salvar-assinatura", dependencies=[Depends(current_user_is_admin)])
def salvarLogo(
    assinatura: Assinatura,
    service: EdicaoSemanaService = Depends()
):
    service.salvarAssinaturaPresidente(assinatura)


@router.post("/avisos/obter-data")
def obterAvisosPorData(
    filtro: FiltroAviso,
    service: EdicaoSemanaService = Depends()
):
    return service.obterAvisosPorData(filtro)


@router.put("/site-em-construcao/{edicaoSemanaId}/{siteEmContrucao}", dependencies=[Depends(current_user_is_admin)])
def aceitarInscricoesAtividades(
    edicaoSemanaId: int,
    siteEmContrucao: bool,
    service: EdicaoSemanaService = Depends()
):
    service.ativarSiteEmConstrucao(edicaoSemanaId, siteEmContrucao)


@router.get("/avisos/{edicaoId}", response_model=List[AvisoNotificacao])
def obterAvisosEdicao(
    edicaoId: int,
    service: EdicaoSemanaService = Depends()
):
    return service.obterAvisosEdicao(edicaoId)


@router.delete("/avisos/{avisoId}", dependencies=[Depends(current_user_is_admin)])
def deletarAviso(
    avisoId: int,
    service: EdicaoSemanaService = Depends()
):
    service.deletarAviso(avisoId)
    return True
