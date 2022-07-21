from app.model.presenca import Presenca
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_sql, get_insert_query_parameter, query_db


class PresencaRepository(BaseRepository):
    def getAlunosPresenca(self, atividade_id):
        query = """SELECT u.nome, ia.atividade_id, ia.id, p.* FROM inscricao_atividade ia
                    INNER JOIN inscricao i on ia.inscricao_id = i.id
                    INNER JOIN usuario u on i.usuario_id = u.id
                    LEFT JOIN presenca p on ia.id = p.inscricao_atividade_id
                    WHERE ia.atividade_id = :AtividadeId"""
        params = {
            "AtividadeId": atividade_id
        }
        return query_db(self.connection, query, params)

    def salvarPresenca(self, presenca: Presenca):
        query = get_insert_query_parameter([presenca], 'presenca', Presenca)
        queryConflict = query[0] + ''' on conflict (inscricao_atividade_id, dia)
                    do update set inteira = excluded.inteira, meia = excluded.meia'''
        exec_sql(self.connection, queryConflict, query[1])
