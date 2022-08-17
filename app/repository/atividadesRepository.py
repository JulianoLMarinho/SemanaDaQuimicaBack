from typing import Any, List
from app.model.atividades import Atividade, AtividadeCreate, AtividadeLista, AtividadeORM, DiaHoraAtividade, ResponsavelAtividade, TipoAtividade
from app.model.certificadoUsuario import CertificadoUsuario
from app.model.comum import OpcaoSelecao
from app.model.tabelas import TotaisAtividades
from app.model.usuarioModel import Usuario
from app.repository.baseRepository import BaseRepository
from app.sql.crud import columns, columnsList, exec_sql, insert_command_from_models, query_db, update_command_from_model
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
                    ae.valor,
                    ae.atividade_presencial,
                    ae.local,
                    ae.link
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
                    ta.cod_tipo,
                    t.nome_turno,
                    at.turno_id,
                    ae.aceita_inscricao,
                    ae.valor,
                    sum(case when i.status <> 'CANCELADA' then 1 else 0 end) as total_inscritos,
                    ae.atividade_presencial,
                    ae.local,
                    ae.link
                    FROM atividade ae
                    INNER JOIN tipo_atividade ta ON ta.id = ae.tipo_atividade
                    LEFT JOIN atividade_turno at ON at.atividade_id = ae.id
                    LEFT JOIN turno t ON t.id = at.turno_id
                    LEFT JOIN inscricao_atividade ia ON ia.atividade_id = ae.id
                    LEFT JOIN inscricao i ON i.id = ia.inscricao_id
                    WHERE ae.edicao_semana_id = :EdicaoId
                    AND ta.cod_tipo IN :TipoAtividade
                    GROUP BY ae.id, ae.titulo, ae.ativa, ta.cod_tipo, ae.descricao_atividade, ae.vagas, ta.nome_tipo, t.nome_turno, at.turno_id, ae.aceita_inscricao, ae.valor
                    ORDER BY ae.titulo"""
        return query_db(self.connection, query, {'EdicaoId': idEdicao, 'TipoAtividade': tipoAtividade}, AtividadeLista)

    def getAtividadesDetalhesByIds(self, atividadeIds: List[int]) -> List[AtividadeLista]:
        query = """SELECT 
                    ae.id,
                    ae.titulo,
                    ae.ativa,
                    ae.descricao_atividade,
                    ae.vagas,
                    ta.nome_tipo,
                    ta.cod_tipo,
                    t.nome_turno,
                    at.turno_id,
                    ae.aceita_inscricao,
                    ae.valor,
                    sum(case when i.status <> 'CANCELADA' then 1 else 0 end) as total_inscritos,
                    ae.atividade_presencial,
                    ae.local,
                    ae.link
                    FROM atividade ae
                    INNER JOIN tipo_atividade ta ON ta.id = ae.tipo_atividade
                    LEFT JOIN atividade_turno at ON at.atividade_id = ae.id
                    LEFT JOIN turno t ON t.id = at.turno_id
                    LEFT JOIN inscricao_atividade ia ON ia.atividade_id = ae.id
                    LEFT JOIN inscricao i ON i.id = ia.inscricao_id
                    WHERE ae.id IN :AtividadeIds
                    GROUP BY ae.id, ae.titulo, ae.ativa, ta.cod_tipo, ae.descricao_atividade, ae.vagas, ta.nome_tipo, t.nome_turno, at.turno_id, ae.aceita_inscricao, ae.valor
                    ORDER BY ae.titulo"""
        return query_db(self.connection, query, {'AtividadeIds': atividadeIds}, AtividadeLista)

    def getResponsaveisByAtividades(self, atividadesIds: List[int]) -> List[ResponsavelAtividade]:
        query = """SELECT r.*, ar.id_atividade 
                   FROM atividade_responsavel ar
                   INNER JOIN responsavel r on r.id = ar.id_responsavel
                   WHERE ar.id_atividade IN :AtividadeIds"""
        return query_db(self.connection, query, {'AtividadeIds': atividadesIds}, model=ResponsavelAtividade)

    def getResponsaveisByAtividade(self, atividadeId: int):
        query = """SELECT r.nome_responsavel
                   FROM atividade_responsavel ar
                   INNER JOIN responsavel r on r.id = ar.id_responsavel
                   WHERE ar.id_atividade = :AtividadeId"""
        return query_db(self.connection, query, {'AtividadeId': atividadeId})

    def tiposAtividades(self) -> List[OpcaoSelecao]:
        query = """SELECT id as value, nome_tipo as name FROM tipo_atividade"""
        return query_db(self.connection, query, model=OpcaoSelecao)

    def criarAtividade(self, atividade: AtividadeCreate) -> int:
        columnsTable = AtividadeCreate.construct().__fields__
        query = insert_command_from_models(
            'atividade', columnsTable, [atividade])
        return query_db(self.connection, query[0] + " RETURNING id", query[1], single=True)

    def salvarHorariosAtividades(self, horarios: List[DiaHoraAtividade]):
        columnsTable = DiaHoraAtividade.construct().__fields__
        query = insert_command_from_models(
            'dia_hora_atividade', columnsTable, horarios)
        exec_sql(self.connection, query[0], query[1])

    def salvarTurnoAtividade(self, turnoId, atividadeId):
        query = f"""INSERT INTO atividade_turno VALUES({atividadeId}, {turnoId})"""
        exec_sql(self.connection, query)

    def salvarResponsavelAtividade(self, atividadeId, responsavelId):
        query = f"""INSERT INTO atividade_responsavel VALUES ({atividadeId}, {responsavelId})"""
        exec_sql(self.connection, query)

    def atualizarAtividade(self, atividade: AtividadeCreate):
        g = update_command_from_model(
            'atividade', AtividadeCreate.construct().__fields__)
        g += " WHERE id = :id"

        exec_sql(self.connection, g, atividade.dict())

    def obterListaCertificadosUsuario(self, usuarioId: int) -> List[CertificadoUsuario]:
        query = """select id, numero_edicao, cod_tipo, data_inicio, data_fim, tema, titulo, (inteira*1.0 + meia/2.0)/(dias*1.0) as percentual_presenca, duracao_atividade from (
                    select id, numero_edicao, cod_tipo, data_inicio, data_fim, tema, titulo, inteira, meia, count(1) as dias, sum(diff) as duracao_atividade from (
                        select a.id, 
                               es.numero_edicao, 
                               a.titulo, 
                               es.data_inicio, 
                               es.data_fim, 
                               es.tema, 
                               dha.dia, 
                               dha2.dia,
                               tp.cod_tipo, 
                               (coalesce(dha.hora_fim - dha.hora_inicio, '00:00:00')+coalesce(dha2.hora_fim - dha2.hora_inicio, '00:00:00')) as diff, 
                               count( case when p.inteira then 1 end) as inteira, 
                               count(case when p.meia then 1 end) as meia 
                        from atividade a 
                        inner join tipo_atividade tp on tp.id = a.tipo_atividade
                        inner join inscricao_atividade ia on ia.atividade_id = a.id 
                        inner join inscricao i on i.id = ia.inscricao_id and i.usuario_id = :UsuarioId
                                                    and i.status = 'PAGAMENTO_CONFIRMADO'
                        inner join edicao_semana es on es.id = a.edicao_semana_id and es.certificado_liberado = true
                        left join atividade_turno at2 on at2.atividade_id = a.id 
                        left join dia_hora_atividade dha on dha.turno_id = at2.turno_id 
                        left join presenca p on p.inscricao_atividade_id = ia.id 
                        left join dia_hora_atividade dha2 on dha2.atividade_edicao_id = a.id
                        group by a.id, tp.cod_tipo, es.numero_edicao, a.titulo, es.data_inicio, es.data_fim, es.tema, dha.dia, dha.hora_fim, dha.hora_inicio, dha2.dia, dha2.hora_fim, dha2.hora_inicio
                        ) b
                    group by id, cod_tipo, numero_edicao, titulo, inteira, meia, data_inicio, data_fim, tema
                ) c"""

        return query_db(self.connection, query, {'UsuarioId': usuarioId}, model=CertificadoUsuario)

    def obterTotaisAtividades(self, edicaoId: int) -> List[TotaisAtividades]:
        query = """
            select a.titulo, a.vagas as vagas, a.vagas - sum(case 
                when i.status = 'PAGAMENTO_CONFIRMADO' then 1
                else 0
            end) as vagas_restantes,
            sum(case 
                when i.status = 'PAGAMENTO_CONFIRMADO' then 1
                else 0
            end) as inscricoes_confirmadas,
            sum(case 
                when i.status = 'CANCELADA' then 1
                else 0
            end) as inscricoes_canceladas,
            sum(case 
                when i.status = 'AGUARDANDO_PAGAMENTO' then 1
                else 0
            end) as inscricoes_aguardando_pagamento,
            sum(case 
                when i.status = 'PAGAMENTO_INFORMADO' then 1
                else 0
            end) as inscricoes_pagamento_informado
            from atividade a 
            inner join inscricao_atividade ia on ia.atividade_id = a.id 
            inner join inscricao i on ia.inscricao_id = i.id 
            where i.edicao_semana_id = :EdicaoSemanaId
            group by a.titulo, a.vagas
        """

        param = {
            "EdicaoSemanaId": edicaoId
        }

        return query_db(self.connection, query, param, model=TotaisAtividades)

    def deletarAtividade(self, atividadeId):
        query = "DELETE FROM atividade WHERE id = :AtividadeId"
        param = {
            "AtividadeId": atividadeId
        }
        exec_sql(self.connection, query, param)
