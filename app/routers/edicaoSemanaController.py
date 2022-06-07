from typing import Any, List
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user

from app.model.edicaoSemana import CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaComComissaoIds
from app.services.edicaoSemanaService import EdicaoSemanaService


router = APIRouter()
prefix = '/edicaoSemana'
tags = ['Edição Semana']


@router.get("", response_model=EdicaoSemanaComComissao)
async def getEdicaoSemana(
    service: EdicaoSemanaService = Depends()
):
    return await service.getEdicaoAtiva()


@router.put("", dependencies=[Depends(get_current_active_user)])
async def editarEdicaoSemana(
    edicaoSemana: EdicaoSemanaComComissaoIds,
    service: EdicaoSemanaService = Depends()
):
    return await service.editarCriarEdicaoSemana(edicaoSemana)


@router.put("/tema", dependencies=[Depends(get_current_active_user)])
async def updateEdicaoSemana(
    tema: dict,
    service: EdicaoSemanaService = Depends()
):
    await service.updateTemaEdicaoAtiva(tema['tema'])


@router.get("/edicoes", dependencies=[Depends(get_current_active_user)], response_model=List[EdicaoSemanaComComissao])
async def getEdicoes(
    service: EdicaoSemanaService = Depends()
):
    return await service.getEdicoes()


@router.post("/carousel-image", dependencies=[Depends(get_current_active_user)])
async def adicionarCarrousselImage(
    carrousselImage: CarouselImageCreation,
    service: EdicaoSemanaService = Depends()
):
    await service.adicionarCarrousselImage(carrousselImage)


@router.get("/carousel-edicao/{edicaoId}", response_model=List[CarouselImage])
async def getCarouselEdicao(
    edicaoId: int,
    service: EdicaoSemanaService = Depends()
):
    return await service.getCarouselEdicao(edicaoId)


@router.put("/carousel-image", dependencies=[Depends(get_current_active_user)])
async def editarCarouselImage(
    carouselImage: CarouselImage,
    service: EdicaoSemanaService = Depends()
):
    await service.editarCarouselImage(carouselImage)


@router.delete("/carousel-image/{carouselImageId}", dependencies=[Depends(get_current_active_user)])
async def deletarCarouselImage(
    carouselImageId: int,
    service: EdicaoSemanaService = Depends()
):
    await service.deletarCarouselImage(carouselImageId)


@router.get("/quem-somos/{edicaoSemanaId}", response_model=List[ComissaoEdicao])
async def obterQuemSomos(
    edicaoSemanaId: int,
    service: EdicaoSemanaService = Depends()
):
    return await service.obterQuemSomos(edicaoSemanaId)
