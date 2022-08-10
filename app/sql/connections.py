
from typing import AsyncIterable, Callable
from sqlalchemy.engine import Connection
from fastapi.params import Depends
from app.sql.database import dbEngine, logger
from sqlalchemy.orm.session import Session
from time import time


def UseConnection() -> Callable[..., AsyncIterable[Connection]]:

    async def CustomConnection() -> AsyncIterable[Connection]:
        #start_time = time()
        conn = dbEngine._db_engine.connect()
        try:
            yield conn
        finally:
            conn.close()
            #elapsed_time = time() - start_time
            # logger.info(
            # f"Connection leased for {elapsed_time} seconds.")
    return CustomConnection


MainConnection: Callable[..., AsyncIterable[Connection]] = UseConnection()
