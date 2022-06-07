from typing import List
from fastapi import Depends
from app.model.patrocinador import Patrocinador, PatrocinadorCreate

from app.repository.patrocinadorRepository import PatrocinadorRepository


class PatrocinadorService:
    def __init__(self, repository: PatrocinadorRepository = Depends()):
        self.repo = repository

    async def salvarNovoPatrocinador(self, patrocinador: PatrocinadorCreate):
        await self.repo.salvarNovoPatrocinador(patrocinador)

    async def obterPatrocindorEdicao(self, edicaoId: int) -> List[Patrocinador]:
        return await self.repo.obterPatrocindorEdicao(edicaoId)

    async def atualizarPatrocinador(self, patrocinador: Patrocinador):
        await self.repo.atualizarPatrocinador(patrocinador)

    async def deletarPatrocinador(self, patrocinadorId: int):
        await self.repo.deletarPatrocinador(patrocinadorId)
