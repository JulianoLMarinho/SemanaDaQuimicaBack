from typing import List
from fastapi import Depends
from app.model.comum import OpcaoSelecao
from app.model.responsavel import ComissaoCreate, Responsavel, ResponsavelCreate
from app.repository.responsavelRepository import ResponsavelRepository


class ResponsavelService:
    def __init__(self, repo: ResponsavelRepository = Depends()):
        self.repo = repo

    def obterTodosResponsaveis(self, tipo: str = 'responsavel') -> List[OpcaoSelecao]:
        return self.repo.obterTodosResponsaveis(tipo)

    def obterResponsaveis(self) -> List[Responsavel]:
        return self.repo.obterResponsaveis()

    def obterComissao(self, edicaoSemanaId: int) -> List[Responsavel]:
        return self.repo.obterComissao(edicaoSemanaId)

    def salvarNovoResponsavel(self, responsavel: ResponsavelCreate):
        return self.repo.salvarNovoResponsavel(responsavel)

    def atualizarResponsavel(self, responsavel: Responsavel):
        return self.repo.atualizarResponsavel(responsavel)

    def deletarEdicaoComissaoByEdicao(self, edicaoSemanaId: int):
        self.repo.deletarEdicaoComissaoByEdicao(edicaoSemanaId)

    def salvarEdicaoComissao(self, edicaoSemanaId: int, integranteComissaoId: int):
        self.repo.salvarEdicaoComissaoC(edicaoSemanaId, integranteComissaoId)

    def obterComissaoByEdicao(self, edicaoSemanaId: int) -> List[Responsavel]:
        return self.repo.obterComissaoByEdicao(edicaoSemanaId)

    def salvarComissao(self, responsavel: ComissaoCreate):
        transaction = self.repo.connection.begin()
        try:
            comissao = self.salvarNovoResponsavel(responsavel)
            self.salvarEdicaoComissao(
                responsavel.edicao_semana_id, comissao.id)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e

    def deleteResponsavel(self, responsavel_id: int):
        self.repo.deleteResponsavel(responsavel_id)
