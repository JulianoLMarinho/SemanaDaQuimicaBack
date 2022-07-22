
from typing import AsyncIterable, Callable
from sqlalchemy.engine import Connection
from fastapi.params import Depends
from app.sql.database import DbEngine, logger
from sqlalchemy.orm.session import Session
from time import time


def UseConnection() -> Connection:
    def CustomConnection(db_engine=Depends(DbEngine())) -> Connection:
        session = Session(bind=db_engine, autocommit=True)
        start_time = time()
        try:
            return session.connection()
        finally:
            elapsed_time = time() - start_time
            logger.info(
                f"Connection leased for {elapsed_time} seconds.")
            session.close()
    return CustomConnection


MainConnection: Connection = UseConnection()
