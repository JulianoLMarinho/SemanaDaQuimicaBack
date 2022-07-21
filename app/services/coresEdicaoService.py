from fastapi import Depends
from app.model.coresEdicao import CoresEdicaoCreate
from app.repository.coresEdicaoRepository import CoresEdicaoRepository


class CoresEdicaoService:

    def __init__(self, repository: CoresEdicaoRepository = Depends()):
        self.repo = repository

    def salvarCoresEdicao(self, coresEdicao: CoresEdicaoCreate):
        self.repo.salvarCoresEdicao(coresEdicao)

    def obterCoresEdicao(self, edicaoId: int) -> CoresEdicaoCreate:
        return self.repo.obterCoresEdicao(edicaoId)
