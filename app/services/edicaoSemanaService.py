from typing import List
from fastapi import Depends
from app.model.edicaoSemana import Assinatura, CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoLogo, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaComComissaoIds, EdicaoSemanaCreate

from app.repository.edicaoSemanaRepository import EdicaoSemanaRepository
from app.services.responsavelService import ResponsavelService


class EdicaoSemanaService:
    def __init__(self, repository: EdicaoSemanaRepository = Depends(), responsavelService: ResponsavelService = Depends()):
        self.repo = repository
        self.responsavelService = responsavelService

    def getEdicaoAtiva(self) -> EdicaoSemanaComComissao:
        edicao = self.repo.getEdicaoAtiva()
        if edicao is None:
            return edicao
        edicao.comissao_edicao = self.responsavelService.obterComissaoByEdicao(
            edicao.id)
        return edicao

    def updateTemaEdicaoAtiva(self, tema: str):
        self.repo.updateTemaEdicaoAtiva(tema)

    def getEdicoes(self) -> List[EdicaoSemanaComComissao]:
        edicoes = self.repo.getEdicoes()
        for edicao in edicoes:
            edicao.comissao_edicao = self.responsavelService.obterComissaoByEdicao(
                edicao.id)
        return edicoes

    def adicionarCarrousselImage(self, carrousselImage: CarouselImageCreation):
        return self.repo.adicionarCarrousselImage(carrousselImage)

    def getCarouselEdicao(self, edicaoId: int) -> List[CarouselImage]:
        return self.repo.getCarouselEdicao(edicaoId)

    def editarCarouselImage(self, carouselImage: CarouselImage):
        self.repo.editarCarouselImage(carouselImage)

    def deletarCarouselImage(self, carouselImageId: int):
        self.repo.deletarCarouselImage(carouselImageId)

    def adicionarEdicaoSemana(self, edicaoSemana: EdicaoSemanaCreate):
        return self.repo.adicionarEdicaoSemana(edicaoSemana)

    def editarCriarEdicaoSemana(self, edicaoSemana: EdicaoSemana):
        transaction = self.repo.connection.begin()
        try:
            if edicaoSemana.id == None:
                edicaoInsertId = self.adicionarEdicaoSemana(edicaoSemana)
                edicaoSemana.id = edicaoInsertId.id
            else:
                self.repo.editarEdicaoSemana(edicaoSemana)
            transaction.commit()
            return True
        except:
            transaction.rollback()
            return False

    def deletarEdicaoSemana(self, edicaoSemanaId: int):
        self.repo.deletarEdicaoSemana(edicaoSemanaId)

    def obterQuemSomos(self, edicaoSemanaId: int) -> List[ComissaoEdicao]:
        return self.repo.obterQuemSomos(edicaoSemanaId)

    def liberarCertificados(self, edicaoSemanaId: int, liberar: bool):
        self.repo.liberarCertificados(edicaoSemanaId, liberar)

    def aceitarInscricoesAtividades(self, edicaoSemanaId: int, aceitarInscricao: bool):
        self.repo.aceitarInscricoesAtividades(edicaoSemanaId, aceitarInscricao)

    def salvarLogo(self, edicaoLogo: EdicaoLogo):
        self.repo.salvarLogo(edicaoLogo)

    def ativarSiteEmConstrucao(self, edicaoSemanaId: int, siteEmConstrucao: bool):
        self.repo.ativarSiteEmConstrucao(edicaoSemanaId, siteEmConstrucao)

    def salvarAssinaturaPresidente(self, assinatura: Assinatura):
        self.repo.salvarAssinaturaPresidente(assinatura)

    def salvarQuemSomos(self, quemSomosTexto: str, edicaoSemanaId: int):
        self.repo.salvarQuemSomos(quemSomosTexto, edicaoSemanaId)
