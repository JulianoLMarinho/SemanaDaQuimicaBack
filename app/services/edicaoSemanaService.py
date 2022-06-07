from typing import List
from fastapi import Depends
from app.model.edicaoSemana import CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaComComissaoIds, EdicaoSemanaCreate

from app.repository.edicaoSemanaRepository import EdicaoSemanaRepository
from app.services.responsavelService import ResponsavelService


class EdicaoSemanaService:
    def __init__(self, repository: EdicaoSemanaRepository = Depends(), responsavelService: ResponsavelService = Depends()):
        self.repo = repository
        self.responsavelService = responsavelService

    async def getEdicaoAtiva(self) -> EdicaoSemanaComComissao:
        edicao = await self.repo.getEdicaoAtiva()
        edicao.comissao_edicao = await self.responsavelService.obterComissaoByEdicao(
            edicao.id)
        return edicao

    async def updateTemaEdicaoAtiva(self, tema: str):
        await self.repo.updateTemaEdicaoAtiva(tema)

    async def getEdicoes(self) -> List[EdicaoSemanaComComissao]:
        edicoes = await self.repo.getEdicoes()
        for edicao in edicoes:
            edicao.comissao_edicao = await self.responsavelService.obterComissaoByEdicao(
                edicao.id)
        return edicoes

    async def adicionarCarrousselImage(self, carrousselImage: CarouselImageCreation):
        return await self.repo.adicionarCarrousselImage(carrousselImage)

    async def getCarouselEdicao(self, edicaoId: int) -> List[CarouselImage]:
        return await self.repo.getCarouselEdicao(edicaoId)

    async def editarCarouselImage(self, carouselImage: CarouselImage):
        await self.repo.editarCarouselImage(carouselImage)

    async def deletarCarouselImage(self, carouselImageId: int):
        await self.repo.deletarCarouselImage(carouselImageId)

    async def adicionarEdicaoSemana(self, edicaoSemana: EdicaoSemanaCreate):
        return await self.repo.adicionarEdicaoSemana(edicaoSemana)

    async def editarCriarEdicaoSemana(self, edicaoSemana: EdicaoSemanaComComissaoIds):
        with self.repo.session.begin():
            try:
                if edicaoSemana.id == None:
                    edicaoInsertId = await self.adicionarEdicaoSemana(edicaoSemana)
                    edicaoSemana.id = edicaoInsertId.id
                else:
                    await self.repo.editarEdicaoSemana(edicaoSemana)
                await self.responsavelService.deletarEdicaoComissaoByEdicao(edicaoSemana.id)
                for res in edicaoSemana.comissao_edicao:
                    await self.responsavelService.salvarEdicaoComissao(
                        edicaoSemana.id, res)
                self.repo.session.commit()
                return True
            except:
                self.repo.session.rollback()
                return False

    async def deletarEdicaoSemana(self, edicaoSemanaId: int):
        await self.repo.deletarEdicaoSemana(edicaoSemanaId)

    async def obterQuemSomos(self, edicaoSemanaId: int) -> List[ComissaoEdicao]:
        return await self.repo.obterQuemSomos(edicaoSemanaId)
