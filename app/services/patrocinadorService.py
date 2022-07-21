from typing import List
from fastapi import Depends
from app.model.patrocinador import Patrocinador, PatrocinadorCreate

from app.repository.patrocinadorRepository import PatrocinadorRepository


class PatrocinadorService:
    def __init__(self, repository: PatrocinadorRepository = Depends()):
        self.repo = repository

    def salvarNovoPatrocinador(self, patrocinador: PatrocinadorCreate):
        self.repo.salvarNovoPatrocinador(patrocinador)

    def obterPatrocindorEdicao(self, edicaoId: int) -> List[Patrocinador]:
        return self.repo.obterPatrocindorEdicao(edicaoId)

    def atualizarPatrocinador(self, patrocinador: Patrocinador):
        self.repo.atualizarPatrocinador(patrocinador)

    def deletarPatrocinador(self, patrocinadorId: int):
        self.repo.deletarPatrocinador(patrocinadorId)
