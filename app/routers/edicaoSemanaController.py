import asyncio
from typing import Any, List
from fastapi import APIRouter, Depends, Request
from sse_starlette import EventSourceResponse
from app.dependencies import current_user_is_admin, get_current_active_user

from app.model.edicaoSemana import Assinatura, CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoLogo, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaComComissaoIds, QuemSomos
from app.services.edicaoSemanaService import EdicaoSemanaService


router = APIRouter()
prefix = '/edicaosemana'
tags = ['Edição Semana']


@router.get("", response_model=EdicaoSemanaComComissao)
def getEdicaoSemana(
    service: EdicaoSemanaService = Depends()
):
    return service.getEdicaoAtiva()


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


@router.put("/site-em-construcao/{edicaoSemanaId}/{siteEmContrucao}", dependencies=[Depends(current_user_is_admin)])
def aceitarInscricoesAtividades(
    edicaoSemanaId: int,
    siteEmContrucao: bool,
    service: EdicaoSemanaService = Depends()
):
    service.ativarSiteEmConstrucao(edicaoSemanaId, siteEmContrucao)
