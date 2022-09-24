from app.sql.connections import MainConnection
from sqlalchemy.engine import Connection
from fastapi import Depends

from app.sql.crud import exec_sql


class BaseRepository:
    def __init__(self, conn: Connection = Depends(MainConnection)):
        self.connection = conn

    def upsertUltimasAlteracoes(self, tabela: str):
        query = """INSERT INTO ultimas_atualizacoes values (:tabela, 'now()')
                    ON CONFLICT (tabela)
                    DO UPDATE SET data_alteracao = 'now()'"""
        exec_sql(self.connection, query, {'tabela': tabela})
