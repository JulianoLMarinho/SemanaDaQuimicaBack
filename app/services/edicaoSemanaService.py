from typing import List
from fastapi import Depends
from app.model.aviso import Aviso, AvisoCreate, AvisoNotificacao, FiltroAviso
from app.model.edicaoSemana import Assinatura, CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoLogo, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaComComissaoIds, EdicaoSemanaCreate

from app.repository.edicaoSemanaRepository import EdicaoSemanaRepository
from app.services.responsavelService import ResponsavelService


class EdicaoSemanaService:
    def __init__(self, repository: EdicaoSemanaRepository = Depends(), responsavelService: ResponsavelService = Depends()):
        self.repo = repository
        self.responsavelService = responsavelService

    def getEdicaoAtiva(self, ) -> EdicaoSemanaComComissao:
        edicao = self.repo.getEdicaoAtiva()
        if edicao is None:
            return edicao
        edicao.comissao_edicao = self.responsavelService.obterComissaoByEdicao(
            edicao.id)
        return edicao
    
    def getEdicaoById(self, id: int) -> EdicaoSemanaComComissao:
        edicao = self.repo.getEdicaoByID(id)
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
            if edicaoSemana.ativa:
                semanaAtiva = self.getEdicaoAtiva()
                if edicaoSemana.id != semanaAtiva.id:
                    semanaAtiva.ativa = False
                    self.repo.editarEdicaoSemana(semanaAtiva)
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

    def salvarComoChegar(self, comoChegarTexto: str, edicaoSemanaId: int):
        self.repo.salvarComoChegar(comoChegarTexto, edicaoSemanaId)

    def salvarFaleConosco(self, faleConosco: str, edicaoSemanaId: int):
        self.repo.salvarFaleConosco(faleConosco, edicaoSemanaId)

    def criarAviso(self, aviso: AvisoCreate):
        self.repo.criarAviso(aviso)

    def obterAvisosEdicao(self, semanaId: int) -> List[AvisoNotificacao]:
        return self.repo.obterAvisosEdicao(semanaId)

    def updateAvisoEdicao(self, aviso: Aviso):
        self.repo.updateAvisoEdicao(aviso)

    def obterAvisosPorData(self, filtro: FiltroAviso) -> List[AvisoNotificacao]:
        return self.repo.obterAvisosPorData(filtro)

    def deletarAviso(self, avisoId: int):
        self.repo.deletarAviso(avisoId)
