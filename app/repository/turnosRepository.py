from typing import List
from app.model.comum import OpcaoSelecao
from app.model.turno import DiaHoraAtividade, Turno, TurnoCriacao
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_session_sql, insert_command_from_models, query_db, query_db_session, update_command_from_model
from app.schemas.db import Turno as TurnoORM


class TurnosRepository(BaseRepository):

    def obterTurnosByEdicao(self, edicaoId: int) -> List[Turno]:
        query = """SELECT * FROM turno WHERE edicao_semana_id = :EdicaoSemanaId"""
        return query_db(self.connection, query, {'EdicaoSemanaId': edicaoId}, model=Turno)

    def criarTurno(self, turno: TurnoCriacao):
        columnsTable = TurnoCriacao.construct().__fields__
        query = insert_command_from_models(
            'turno', columnsTable, [turno])
        return query_db_session(self.connection, query[0] + " RETURNING id", query[1], single=True)

    def salvarHorariosTurnos(self, horarios: List[DiaHoraAtividade]):
        columnsTable = DiaHoraAtividade.construct().__fields__
        query = insert_command_from_models(
            'dia_hora_atividade', columnsTable, horarios)
        exec_session_sql(self.session, query[0], query[1])

    def obterTurnosSelecaoByEdicao(self, edicaoId: int) -> List[OpcaoSelecao]:
        query = """SELECT id as value, nome_turno as name FROM turno WHERE edicao_semana_id = :EdicaoSemanaId"""
        return query_db(self.connection, query, {'EdicaoSemanaId': edicaoId}, model=OpcaoSelecao)

    def deletarTurnosByAtividade(self, atividadeId):
        query = f"""DELETE FROM atividade_turno WHERE atividade_id = {atividadeId}"""
        exec_session_sql(self.session, query)

    def atualizarTurno(self, turno: Turno):
        g = update_command_from_model(
            'turno', Turno.construct().__fields__)
        g += " WHERE id = :id"

        exec_session_sql(self.session, g, turno.dict())
