from app.sql.connections import MainConnection, MainSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from app.sql.crud import exec_sql, query_db


class BaseRepository:
    def __init__(self, conn: MainConnection = Depends(), session: sessionmaker = Depends(MainSession)):
        self.connection = conn
        self.session = session

    def BeginTransaction(self):
        exec_sql(self.connection, "BEGIN")

    def CommitTransaction(self):
        exec_sql(self.connection, "COMMIT")

    def RollbackTransaction(self):
        exec_sql(self.connection, "ROLLBACK")
