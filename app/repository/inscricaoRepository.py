from typing import Any, List
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, Inscricao, InscricaoCreate
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_session_sql, exec_sql, insert_command_from_models, query_db, query_db_session


class InscricaoRepository(BaseRepository):

    async def adicionarInscricao(self, inscricao: InscricaoCreate):
        columnsTable = InscricaoCreate.construct().__fields__
        query = insert_command_from_models(
            'inscricao', columnsTable, [inscricao])
        return query_db_session(self.session, query[0] + " RETURNING id", query[1], single=True)

    async def adicionarAtividadeInscricao(self, inscricao_id: int, atividade_id: int):
        query = """INSERT INTO inscricao_atividade(inscricao_id, atividade_id) VALUES (:InscricaoId, :AtividadeId)"""
        params = {
            "InscricaoId": inscricao_id,
            "AtividadeId": atividade_id
        }
        exec_session_sql(self.session, query, params)

    async def obterAtividadesUsuario(self, usuario_id) -> List[AtividadeUsuario]:
        query = """SELECT ia.atividade_id, i.status, ia.inscricao_id FROM inscricao_atividade ia
                    INNER JOIN inscricao i ON i.id = ia.inscricao_id
                    WHERE i.usuario_id = :UsuarioId 
                    AND i.status <> 'CANCELADA'"""
        return query_db(self.connection, query, {'UsuarioId': usuario_id}, model=AtividadeUsuario)

    async def obterInscricoes(self, usuario_id) -> List[Inscricao]:
        query = """SELECT * FROM inscricao WHERE usuario_id = :UsuarioId ORDER BY data_criacao DESC"""
        return query_db(self.connection, query, {'UsuarioId': usuario_id}, model=Inscricao)

    async def obterInscricoesConfirmacao(self) -> List[Inscricao]:
        query = """SELECT * FROM inscricao WHERE status = 'PAGAMENTO_INFORMADO' ORDER BY data_criacao DESC"""
        return query_db(self.connection, query, model=Inscricao)

    async def obterAtividade(self, inscricao_id) -> List[Atividade]:
        query = """SELECT a.* FROM inscricao_atividade ia
                    INNER JOIN atividade a ON a.id = ia.atividade_id
                    WHERE ia.inscricao_id = :InscricaoId"""
        return query_db(self.connection, query, {"InscricaoId": inscricao_id}, model=Atividade)

    async def informarPagamento(self, inscricao_id, numero_documento):
        query = """UPDATE inscricao SET
                   status = 'PAGAMENTO_INFORMADO',
                   numero_comprovante = :NumeroDocumento
                   WHERE id = :InscricaoId"""
        params = {
            "InscricaoId": inscricao_id,
            "NumeroDocumento": numero_documento
        }
        exec_sql(self.connection, query, params)

    async def alterarStatusInscricao(self, inscricao_id, status):
        query = """UPDATE inscricao SET
                    status = :Status 
                    WHERE id = :InscricaoId"""
        param = {
            'InscricaoId': inscricao_id,
            'Status': status
        }
        exec_sql(self.connection, query, param)

    async def totalInscricoesPagamentoInformado(self):
        query = """SELECT COUNT(1) as total FROM inscricao WHERE status = 'PAGAMENTO_INFORMADO'"""
        return query_db(self.connection, query, single=True)
