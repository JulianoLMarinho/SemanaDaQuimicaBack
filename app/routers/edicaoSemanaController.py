from typing import Any, List
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user

from app.model.edicaoSemana import CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoLogo, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaComComissaoIds
from app.services.edicaoSemanaService import EdicaoSemanaService


router = APIRouter()
prefix = '/edicaoSemana'
tags = ['Edição Semana']


@router.get("", response_model=EdicaoSemanaComComissao)
def getEdicaoSemana(
    service: EdicaoSemanaService = Depends()
):
    return service.getEdicaoAtiva()


@router.put("", dependencies=[Depends(get_current_active_user)])
def editarEdicaoSemana(
    edicaoSemana: EdicaoSemanaComComissaoIds,
    service: EdicaoSemanaService = Depends()
):
    return service.editarCriarEdicaoSemana(edicaoSemana)


@router.put("/tema", dependencies=[Depends(get_current_active_user)])
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


@router.post("/carousel-image", dependencies=[Depends(get_current_active_user)])
def adicionarCarrousselImage(
    carrousselImage: CarouselImageCreation,
    service: EdicaoSemanaService = Depends()
):
    service.adicionarCarrousselImage(carrousselImage)


@router.get("/carousel-edicao/{edicaoId}", response_model=List[CarouselImage])
def getCarouselEdicao(
    edicaoId: int,
    service: EdicaoSemanaService = Depends()
):
    return service.getCarouselEdicao(edicaoId)


@router.put("/carousel-image", dependencies=[Depends(get_current_active_user)])
def editarCarouselImage(
    carouselImage: CarouselImage,
    service: EdicaoSemanaService = Depends()
):
    service.editarCarouselImage(carouselImage)


@router.delete("/carousel-image/{carouselImageId}", dependencies=[Depends(get_current_active_user)])
def deletarCarouselImage(
    carouselImageId: int,
    service: EdicaoSemanaService = Depends()
):
    service.deletarCarouselImage(carouselImageId)


@router.get("/quem-somos/{edicaoSemanaId}", response_model=List[ComissaoEdicao], dependencies=[Depends(get_current_active_user)])
def obterQuemSomos(
    edicaoSemanaId: int,
    service: EdicaoSemanaService = Depends()
):
    return service.obterQuemSomos(edicaoSemanaId)


@router.put("/liberar-certificado/{edicaoSemanaId}/{liberar}", dependencies=[Depends(get_current_active_user)])
def liberarCertificados(
    edicaoSemanaId: int,
    liberar: bool,
    service: EdicaoSemanaService = Depends()
):
    service.liberarCertificados(edicaoSemanaId, liberar)


@router.put("/aceitar-inscricao-atividade/{edicaoSemanaId}/{aceitarInscricao}", dependencies=[Depends(get_current_active_user)])
def aceitarInscricoesAtividades(
    edicaoSemanaId: int,
    aceitarInscricao: bool,
    service: EdicaoSemanaService = Depends()
):
    service.aceitarInscricoesAtividades(edicaoSemanaId, aceitarInscricao)


@router.post("/salvar-logo", dependencies=[Depends(get_current_active_user)])
def salvarLogo(
    edicaoLogo: EdicaoLogo,
    service: EdicaoSemanaService = Depends()
):
    service.salvarLogo(edicaoLogo)


@router.put("/site-em-construcao/{edicaoSemanaId}/{siteEmContrucao}", dependencies=[Depends(get_current_active_user)])
def aceitarInscricoesAtividades(
    edicaoSemanaId: int,
    siteEmContrucao: bool,
    service: EdicaoSemanaService = Depends()
):
    service.ativarSiteEmConstrucao(edicaoSemanaId, siteEmContrucao)
