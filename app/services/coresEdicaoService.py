from fastapi import Depends
from app.model.coresEdicao import CoresEdicaoCreate
from app.repository.coresEdicaoRepository import CoresEdicaoRepository


class CoresEdicaoService:

    def __init__(self, repository: CoresEdicaoRepository = Depends()):
        self.repo = repository

    async def salvarCoresEdicao(self, coresEdicao: CoresEdicaoCreate):
        await self.repo.salvarCoresEdicao(coresEdicao)

    async def obterCoresEdicao(self, edicaoId: int) -> CoresEdicaoCreate:
        return await self.repo.obterCoresEdicao(edicaoId)
