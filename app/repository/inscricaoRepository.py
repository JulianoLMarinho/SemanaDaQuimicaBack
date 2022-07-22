from typing import Any, List
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, Inscricao, InscricaoCreate
from app.model.usuario import Usuario
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_sql, exec_sql, insert_command_from_models, query_db, query_db


class InscricaoRepository(BaseRepository):

    def adicionarInscricao(self, inscricao: InscricaoCreate):
        columnsTable = InscricaoCreate.construct().__fields__
        query = insert_command_from_models(
            'inscricao', columnsTable, [inscricao])
        return query_db(self.connection, query[0] + " RETURNING id", query[1], single=True)

    def adicionarAtividadeInscricao(self, inscricao_id: int, atividade_id: int):
        query = """INSERT INTO inscricao_atividade(inscricao_id, atividade_id) VALUES (:InscricaoId, :AtividadeId)"""
        params = {
            "InscricaoId": inscricao_id,
            "AtividadeId": atividade_id
        }
        exec_sql(self.connection, query, params)

    def obterAtividadesUsuario(self, usuario_id) -> List[AtividadeUsuario]:
        query = """SELECT ia.atividade_id, i.status, ia.inscricao_id FROM inscricao_atividade ia
                    INNER JOIN inscricao i ON i.id = ia.inscricao_id
                    WHERE i.usuario_id = :UsuarioId 
                    AND i.status <> 'CANCELADA'"""
        return query_db(self.connection, query, {'UsuarioId': usuario_id}, model=AtividadeUsuario)

    def obterInscricoes(self, usuario_id) -> List[Inscricao]:
        query = """SELECT * FROM inscricao WHERE usuario_id = :UsuarioId ORDER BY data_criacao DESC"""
        return query_db(self.connection, query, {'UsuarioId': usuario_id}, model=Inscricao)

    def obterInscricoesConfirmacao(self) -> List[Inscricao]:
        query = """SELECT * FROM inscricao WHERE status = 'PAGAMENTO_INFORMADO' ORDER BY data_criacao DESC"""
        return query_db(self.connection, query, model=Inscricao)

    def obterAtividade(self, inscricao_id) -> List[Atividade]:
        query = """SELECT a.* FROM inscricao_atividade ia
                    INNER JOIN atividade a ON a.id = ia.atividade_id
                    WHERE ia.inscricao_id = :InscricaoId"""
        return query_db(self.connection, query, {"InscricaoId": inscricao_id}, model=Atividade)

    def informarPagamento(self, inscricao_id, numero_documento):
        query = """UPDATE inscricao SET
                   status = 'PAGAMENTO_INFORMADO',
                   numero_comprovante = :NumeroDocumento
                   WHERE id = :InscricaoId"""
        params = {
            "InscricaoId": inscricao_id,
            "NumeroDocumento": numero_documento
        }
        exec_sql(self.connection, query, params)

    def alterarStatusInscricao(self, inscricao_id, status):
        query = """UPDATE inscricao SET
                    status = :Status 
                    WHERE id = :InscricaoId"""
        param = {
            'InscricaoId': inscricao_id,
            'Status': status
        }
        exec_sql(self.connection, query, param)

    def totalInscricoesPagamentoInformado(self):
        query = """SELECT COUNT(1) as total FROM inscricao WHERE status = 'PAGAMENTO_INFORMADO'"""
        return query_db(self.connection, query, single=True)

    def obterUsuarioPorInscricao(self, inscricao_id: int) -> Usuario:
        query = """SELECT u.email, u.id FROM Usuario u
                    INNER JOIN inscricao I on I.usuario_id = u.id
                    WHERE I.id = :InscricaoId"""
        return query_db(self.connection, query, {"InscricaoId": inscricao_id}, single=True, model=Usuario)
