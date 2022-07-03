from typing import List
from app.model.patrocinador import Patrocinador, PatrocinadorCreate
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_sql, insert_command_from_models, query_db, update_command_from_model


class PatrocinadorRepository(BaseRepository):
    def salvarNovoPatrocinador(self, patrocinador: PatrocinadorCreate):
        columnsTable = PatrocinadorCreate.construct().__fields__
        query = insert_command_from_models(
            'patrocinador', columnsTable, [patrocinador])
        exec_sql(self.connection, query[0], query[1])

    def obterPatrocindorEdicao(self, edicaoId: int) -> List[Patrocinador]:
        query = f"""SELECT * FROM patrocinador WHERE edicao_semana_id = {edicaoId} ORDER BY ordem"""
        return query_db(self.connection, query, model=Patrocinador)

    def atualizarPatrocinador(self, patrocinador: Patrocinador):
        query = update_command_from_model(
            'patrocinador', Patrocinador.construct().__fields__) + """ WHERE id = :id"""
        exec_sql(self.connection, query, patrocinador.dict())

    def deletarPatrocinador(self, patrocinadorId: int):
        query = f"DELETE FROM patrocinador WHERE id = {patrocinadorId}"
        exec_sql(self.connection, query)
