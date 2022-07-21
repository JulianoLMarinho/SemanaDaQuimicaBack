from typing import List
from app.model.atividades import DiaHoraAtividade
from app.model.turno import DiaHoraTurno
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_session_sql, query_db


class DiaHorarioRepository(BaseRepository):
    def obterDiaHorariosByTurnos(self, turnosIds: List[int]) -> List[DiaHoraTurno]:
        query = """SELECT * FROM dia_hora_atividade
                    WHERE turno_id IN :TurnosIds"""
        return query_db(self.connection, query, {
            'TurnosIds': turnosIds}, model=DiaHoraTurno)

    def obterDiaHorariosByAtividade(self, atividadesIds: List[int]) -> List[DiaHoraAtividade]:
        query = """SELECT distinct dha.* FROM dia_hora_atividade dha
                    LEFT JOIN atividade_turno at ON at.turno_id = dha.turno_id
                    WHERE atividade_edicao_id IN :AtividadesIds
                    OR at.atividade_id IN :AtividadesIds
                    ORDER BY dha.dia"""
        return query_db(self.connection, query, {
            'AtividadesIds': atividadesIds}, model=DiaHoraAtividade)

    def deletetarHorariosByAtividade(self, atividadeId: int):
        query = f"DELETE FROM dia_hora_atividade WHERE atividade_edicao_id = {atividadeId}"
        exec_session_sql(self.session, query)

    def deletetarHorariosByTurno(self, turnoId: int):
        query = f"DELETE FROM dia_hora_atividade WHERE turno_id = {turnoId}"
        exec_session_sql(self.session, query)
