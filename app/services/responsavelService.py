from typing import List
from fastapi import Depends
from app.model.comum import OpcaoSelecao
from app.model.responsavel import Responsavel, ResponsavelCreate
from app.repository.responsavelRepository import ResponsavelRepository


class ResponsavelService:
    def __init__(self, repo: ResponsavelRepository = Depends()):
        self.repo = repo

    def obterTodosResponsaveis(self) -> List[OpcaoSelecao]:
        return self.repo.obterTodosResponsaveis()

    def obterResponsaveis(self) -> List[Responsavel]:
        return self.repo.obterResponsaveis()

    def salvarNovoResponsavel(self, responsavel: ResponsavelCreate):
        return self.repo.salvarNovoResponsavel(responsavel)

    def atualizarResponsavel(self, responsavel: Responsavel):
        return self.repo.atualizarResponsavel(responsavel)

    def deletarEdicaoComissaoByEdicao(self, edicaoSemanaId: int):
        self.repo.deletarEdicaoComissaoByEdicao(edicaoSemanaId)

    def salvarEdicaoComissao(self, edicaoSemanaId: int, integranteComissaoId: int):
        self.repo.salvarEdicaoComissao(edicaoSemanaId, integranteComissaoId)

    def obterComissaoByEdicao(self, edicaoSemanaId: int) -> List[Responsavel]:
        return self.repo.obterComissaoByEdicao(edicaoSemanaId)
