from typing import List
from fastapi import Depends
from sqlalchemy import null
from app.model.presenca import AlunoPresenca, Presenca
from app.repository.presencaRepository import PresencaRepository


class PresencaService():
    def __init__(self, repo: PresencaRepository = Depends()):
        self.repo = repo

    def getAlunosPresenca(self, atividade_id):
        presencas = self.repo.getAlunosPresenca(atividade_id)
        returnListObject = {}
        for presenca in presencas:
            if presenca.id not in returnListObject.keys():

                returnListObject[presenca.id] = AlunoPresenca(id=presenca.id,
                                                              nome=presenca.nome, atividade_id=presenca.atividade_id, presencas=[])
            if presenca.inscricao_atividade_id is not None:
                obj = returnListObject.get(presenca.inscricao_atividade_id)
                obj.presencas.append(Presenca(inscricao_atividade_id=presenca.inscricao_atividade_id,
                                     dia=presenca.dia, inteira=presenca.inteira, meia=presenca.meia))
        return list(returnListObject.values())

    def salvarPresenca(self, presenca: Presenca):
        self.repo.salvarPresenca(presenca)
