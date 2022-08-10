
from typing import AsyncIterable, Callable
from sqlalchemy.engine import Connection
from fastapi.params import Depends
from app.sql.database import dbEngine, logger
from sqlalchemy.orm.session import Session
from time import time


def UseConnection() -> Callable[..., AsyncIterable[Connection]]:

    async def CustomConnection(db_engine=Depends(dbEngine.DbEngine())) -> AsyncIterable[Connection]:
        session = dbEngine.get_session()
        conn = session.connection()
        start_time = time()
        try:
            yield conn
        finally:
            elapsed_time = time() - start_time
            logger.info(
                f"Connection leased for {elapsed_time} seconds.")
            conn.close()
    return CustomConnection


MainConnection: Callable[..., AsyncIterable[Connection]] = UseConnection()
