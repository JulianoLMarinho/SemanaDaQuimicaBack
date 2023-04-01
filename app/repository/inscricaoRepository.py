from typing import Any, List
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, Inscricao, InscricaoCreate
from app.model.tabelas import InscricoesEdicao
from app.model.usuario import NomeEmail, Usuario
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

    def obterAtividadesUsuario(self, usuario_id, edicao_id) -> List[AtividadeUsuario]:
        query = """SELECT ia.atividade_id, i.status, ia.inscricao_id, i.camisa_kit, i.cotista_sbq FROM inscricao_atividade ia
                    INNER JOIN inscricao i ON i.id = ia.inscricao_id
                    WHERE i.usuario_id = :UsuarioId 
                    AND (:EdicaoId IS NULL OR i.edicao_semana_id = :EdicaoId)
                    AND i.status <> 'CANCELADA'"""
        return query_db(self.connection, query, {'UsuarioId': usuario_id, 'EdicaoId': edicao_id}, model=AtividadeUsuario)

    def obterInscricoes(self, usuario_id) -> List[Inscricao]:
        query = """SELECT * FROM inscricao WHERE usuario_id = :UsuarioId ORDER BY data_criacao DESC"""
        return query_db(self.connection, query, {'UsuarioId': usuario_id}, model=Inscricao)

    def obterInscricoesConfirmacao(self) -> List[Inscricao]:
        query = """SELECT i.*, u.nome, u.email  FROM inscricao i 
                    inner join usuario u on u.id = i.usuario_id 
                    WHERE status = 'PAGAMENTO_INFORMADO' ORDER BY data_criacao DESC"""
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

    def obterInscricoesPorAtividade(self, atividadeId: int) -> List[NomeEmail]:
        query = """select u.nome, u.email, ia.atividade_id  from inscricao i 
                    inner join inscricao_atividade ia on ia.inscricao_id = i.id 
                    inner join usuario u on u.id = i.usuario_id 
                    where i.status = 'PAGAMENTO_CONFIRMADO'
                    and ia.atividade_id = :AtividadeId
                    order by u.nome"""
        return query_db(self.connection, query, {"AtividadeId": atividadeId}, model=NomeEmail)

    def obterInscricoesPorEdicao(self, edicaoId: int) -> List[InscricoesEdicao]:
        query = """select u.nome, u.email, u.nivel, u.curso, u.universidade, u.tamanho_camisa, u.genero, sum(1) as numero_atividades from usuario u
                    inner join inscricao i on i.usuario_id = u.id 
                                                and i.status = 'PAGAMENTO_CONFIRMADO' 
                    inner join inscricao_atividade ia on ia.inscricao_id = i.id
                    where i.edicao_semana_id = :EdicaoSemanaId
                    group by u.nome, u.email, u.nivel, u.curso, u.universidade, u.tamanho_camisa, u.genero"""
        param = {
            "EdicaoSemanaId": edicaoId
        }

        return query_db(self.connection, query, param, model=InscricoesEdicao)

    def obterInscricoesAguardandoPagamento3Dias(self) -> List[Inscricao]:
        query = """select * from inscricao i 
                    where status = 'AGUARDANDO_PAGAMENTO'
                    and now()::date - data_criacao::date >= 3"""
        return query_db(self.connection, query, model=Inscricao)

    def obterAlunosPrimeiroCurso(self, edicao_id: int):
        query = """select aluno, curso, dia, horario from vw_primeiro_curso_usuario where edicao_semana_id = :EdicaoID"""
        return query_db(self.connection, query, {"EdicaoID": edicao_id})

    def tamanhoCamisaUsuarioInscrito(self, edicao_id: int):
        query = """
            select u.nome as Nome, u.tamanho_camisa as Tamanho from usuario u
            inner join inscricao i on i.usuario_id = u.id and i.camisa_kit = true and i.status = 'PAGAMENTO_CONFIRMADO'
            where i.edicao_semana_id = :EdicaoID
            order by u.nome
        """
        return query_db(self.connection, query, {"EdicaoID": edicao_id})
