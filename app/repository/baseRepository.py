from app.sql.connections import MainConnection
from sqlalchemy.engine import Connection
from fastapi import Depends


class BaseRepository:
    def __init__(self, conn: Connection = Depends(MainConnection)):
        self.connection = conn
