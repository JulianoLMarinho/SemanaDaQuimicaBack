from sqlalchemy import true
from app.model.coresEdicao import CoresEdicaoCreate
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_sql, get_insert_query_parameter, insert_command_from_models, query_db


class CoresEdicaoRepository(BaseRepository):
    def salvarCoresEdicao(self, coresEdicao: CoresEdicaoCreate):
        query = get_insert_query_parameter(
            [coresEdicao], 'cores_edicao', CoresEdicaoCreate)
        test = """insert into cores_edicao values(:edicao_semana_id, :cor1, :cor2, :cor3, :cor4, :cor5, :cor6)
                    on conflict(edicao_semana_id)
                    do update set 
                    cor1 = :cor1, 
                    cor2 = :cor2, 
                    cor3 = :cor3, 
                    cor4 = :cor4, 
                    cor5 = :cor5, 
                    cor6 = :cor6;"""
        exec_sql(self.connection, test, coresEdicao.dict())
        self.upsertUltimasAlteracoes('cores_edicao')

    def obterCoresEdicao(self, edicaoId: int) -> CoresEdicaoCreate:
        query = "SELECT * FROM cores_edicao WHERE edicao_semana_id = :EdicaoId"
        return query_db(self.connection, query, {'EdicaoId': edicaoId}, model=CoresEdicaoCreate, single=True)
