from typing import List
from app.model.comum import OpcaoSelecao
from app.model.responsavel import Responsavel, ResponsavelCreate
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_session_sql, exec_sql, insert_command_from_models, query_db, update_command_from_model


class ResponsavelRepository(BaseRepository):
    def obterTodosResponsaveis(self) -> List[OpcaoSelecao]:
        query = """SELECT id as value, nome_responsavel as name FROM responsavel"""
        return query_db(self.connection, query, model=OpcaoSelecao)

    def obterResponsaveis(self) -> List[Responsavel]:
        query = f"SELECT * FROM responsavel"
        gfd = query_db(self.connection, query, model=Responsavel)
        return gfd

    def salvarNovoResponsavel(self, responsavel: ResponsavelCreate):
        columnsTable = ResponsavelCreate.construct().__fields__
        query = insert_command_from_models(
            'responsavel', columnsTable, [responsavel])
        exec_sql(self.connection, query[0], query[1])

    def deletarResponsavelAtividadeByAtividade(self, atividadeId: int):
        query = f"DELETE FROM atividade_responsavel WHERE id_atividade = {atividadeId}"
        exec_session_sql(self.session, query)

    def deletarEdicaoComissaoByEdicao(self, edicaoSemanaId: int):
        query = f"DELETE FROM edicao_comissao WHERE edicao_semana_id = {edicaoSemanaId}"
        exec_session_sql(self.session, query)

    def atualizarResponsavel(self, responsavel: Responsavel):
        g = update_command_from_model(
            'responsavel', Responsavel.construct().__fields__)
        g += " WHERE id = :id"

        exec_sql(self.connection, g, responsavel.dict())

    def salvarEdicaoComissao(self, edicaoSemanaId: int, integranteComissaoId: int):
        query = f"INSERT INTO edicao_comissao VALUES ({edicaoSemanaId}, {integranteComissaoId})"
        exec_session_sql(self.session, query)

    def obterComissaoByEdicao(self, edicaoSemanaId: int) -> List[Responsavel]:
        query = """SELECT * FROM responsavel r
                    INNER JOIN edicao_comissao ec ON ec.responsavel_id = r.id
                    WHERE ec.edicao_semana_id = :EdicaoId"""
        return query_db(self.connection, query, {'EdicaoId': edicaoSemanaId}, model=Responsavel)
