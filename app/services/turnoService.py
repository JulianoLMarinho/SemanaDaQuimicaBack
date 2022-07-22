from typing import List
from xmlrpc.client import boolean
from fastapi import Depends
from app.model.comum import OpcaoSelecao
from app.model.turno import Turno, TurnoComHorarios, TurnoCriacao, TurnoCriacaoComHorario
from app.repository.diaHorarioRepository import DiaHorarioRepository
from app.repository.turnosRepository import TurnosRepository


class TurnoService:
    def __init__(self, repository: TurnosRepository = Depends(), repositoryDiaHorario: DiaHorarioRepository = Depends()):
        self.repo = repository
        self.diaHorarioRepo = repositoryDiaHorario

    def obterTurnosByEdicao(self, edicaoId: int) -> List[Turno]:
        return self.repo.obterTurnosByEdicao(edicaoId)

    def criarTurno(self, turno: TurnoCriacaoComHorario) -> boolean:
        transaction = self.repo.connection.begin()
        try:
            turnoId = self.repo.criarTurno(turno)
            for hor in turno.horarios:
                hor.turno_id = turnoId.id
            self.repo.salvarHorariosTurnos(turno.horarios)
            transaction.commit()
            return True
        except:
            transaction.rollback()
            return False

    def editarTurno(self, turno: TurnoCriacaoComHorario) -> boolean:
        transaction = self.repo.connection.begin()
        try:
            self.repo.atualizarTurno(turno)
            self.diaHorarioRepo.deletetarHorariosByTurno(turno.id)
            for hor in turno.horarios:
                hor.turno_id = turno.id
            self.repo.salvarHorariosTurnos(turno.horarios)
            transaction.commit()
        except:
            transaction.rollback()
            raise Exception('Não foi possível atualizar o turno')

    def obterTurnosComHorario(self, edicaoId: int) -> List[TurnoComHorarios]:
        returnValue: List[TurnoComHorarios] = []

        turnos = self.obterTurnosByEdicao(edicaoId)
        diaHorario = []
        if len(turnos) > 0:
            diaHorario = self.diaHorarioRepo.obterDiaHorariosByTurnos(
                [t.id for t in turnos])

        for turno in turnos:
            horarios = list(
                filter(lambda x: x.turno_id == turno.id, diaHorario))
            returnValue.append(TurnoComHorarios(id=turno.id, nome_turno=turno.nome_turno,
                               edicao_semana_id=turno.edicao_semana_id, horarios=horarios))
        return returnValue

    def obterTurnosSelecaoByEdicao(self, edicaoId: int) -> List[OpcaoSelecao]:
        return self.repo.obterTurnosSelecaoByEdicao(edicaoId)

    def deletarTurnosByAtividade(self, atividadeId):
        self.repo.deletarTurnosByAtividade(atividadeId)
