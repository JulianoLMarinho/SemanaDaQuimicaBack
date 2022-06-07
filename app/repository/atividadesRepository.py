from typing import Any, List
from app.model.atividades import Atividade, AtividadeCreate, AtividadeLista, AtividadeORM, DiaHoraAtividade, ResponsavelAtividade, TipoAtividade
from app.model.comum import OpcaoSelecao
from app.model.usuarioModel import Usuario
from app.repository.baseRepository import BaseRepository
from app.sql.crud import columns, columnsList, exec_session_sql, exec_sql, insert_command_from_models, query_db, query_db_session, update_command_from_model
from app.schemas.db import Usuario


class AtividadesRepository(BaseRepository):
    def getAtividadesByEdicao(self, idEdicao: int) -> List[Atividade]:
        query = """SELECT * FROM atividade
                    WHERE edicao_semana_id = :EdicaoId
                    ORDER BY titulo"""
        return query_db(self.connection, query, {'EdicaoId': idEdicao}, Atividade)

    def getAtividadesDetalhesByEdicao(self, idEdicao: int) -> List[AtividadeLista]:
        query = """SELECT 
                    ae.id,
                    ae.titulo,
                    ae.ativa,
                    ae.descricao_atividade,
                    ae.vagas,
                    ta.nome_tipo,
                    ae.tipo_atividade,
                    ae.aceita_inscricao,
                    at.turno_id,
                    ae.valor
                    FROM atividade ae
                    INNER JOIN tipo_atividade ta ON ta.id = ae.tipo_atividade
                    LEFT JOIN atividade_turno at ON at.atividade_id = ae.id
                    WHERE edicao_semana_id = :EdicaoId
                    ORDER BY ae.titulo"""
        return query_db(self.connection, query, {'EdicaoId': idEdicao}, AtividadeLista)

    def getAtividadesDetalhesByEdicaoAndTipo(self, idEdicao: int, tipoAtividade: List[str]) -> List[AtividadeLista]:
        query = """SELECT 
                    ae.id,
                    ae.titulo,
                    ae.ativa,
                    ae.descricao_atividade,
                    ae.vagas,
                    ta.nome_tipo,
                    t.nome_turno,
                    at.turno_id,
                    ae.aceita_inscricao,
                    ae.valor,
                    count(1) - 1 as total_inscritos
                    FROM atividade ae
                    INNER JOIN tipo_atividade ta ON ta.id = ae.tipo_atividade
                    LEFT JOIN atividade_turno at ON at.atividade_id = ae.id
                    LEFT JOIN turno t ON t.id = at.turno_id
                    LEFT JOIN inscricao_atividade ia ON ia.atividade_id = ae.id
                    LEFT JOIN inscricao i ON i.id = ia.inscricao_id
                    WHERE ae.edicao_semana_id = :EdicaoId
                    AND ta.cod_tipo IN :TipoAtividade
                    GROUP BY ae.id, ae.titulo, ae.ativa, ae.descricao_atividade, ae.vagas, ta.nome_tipo, t.nome_turno, at.turno_id, ae.aceita_inscricao, ae.valor
                    ORDER BY ae.titulo"""
        return query_db(self.connection, query, {'EdicaoId': idEdicao, 'TipoAtividade': tipoAtividade}, AtividadeLista)

    def getResponsaveisByAtividades(self, atividadesIds: List[int]) -> List[ResponsavelAtividade]:
        query = """SELECT r.*, ar.id_atividade 
                   FROM atividade_responsavel ar
                   INNER JOIN responsavel r on r.id = ar.id_responsavel
                   WHERE ar.id_atividade IN :AtividadeIds"""
        return query_db(self.connection, query, {'AtividadeIds': atividadesIds}, model=ResponsavelAtividade)

    def tiposAtividades(self) -> List[OpcaoSelecao]:
        query = """SELECT id as value, nome_tipo as name FROM tipo_atividade"""
        return query_db(self.connection, query, model=OpcaoSelecao)

    def criarAtividade(self, atividade: AtividadeCreate) -> int:
        columnsTable = AtividadeCreate.construct().__fields__
        query = insert_command_from_models(
            'atividade', columnsTable, [atividade])
        return query_db_session(self.session, query[0] + " RETURNING id", query[1], single=True)

    def salvarHorariosAtividades(self, horarios: List[DiaHoraAtividade]):
        columnsTable = DiaHoraAtividade.construct().__fields__
        query = insert_command_from_models(
            'dia_hora_atividade', columnsTable, horarios)
        exec_session_sql(self.session, query[0], query[1])

    def salvarTurnoAtividade(self, turnoId, atividadeId):
        query = f"""INSERT INTO atividade_turno VALUES({atividadeId}, {turnoId})"""
        exec_session_sql(self.session, query)

    def salvarResponsavelAtividade(self, atividadeId, responsavelId):
        query = f"""INSERT INTO atividade_responsavel VALUES ({atividadeId}, {responsavelId})"""
        exec_session_sql(self.session, query)

    def atualizarAtividade(self, atividade: AtividadeCreate):
        g = update_command_from_model(
            'atividade', AtividadeCreate.construct().__fields__)
        g += " WHERE id = :id"

        exec_session_sql(self.session, g, atividade.dict())
