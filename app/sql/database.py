import logging
from typing import Awaitable, Callable, Dict, Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os
from dotenv import load_dotenv
import urllib.parse
from sqlalchemy.orm.session import Session

logger = logging.getLogger("uvicorn.error")

load_dotenv()


class DBEngine:

    def __init__(self):
        self._db_engine: Optional[Engine] = None
        self._db_session: Session = None

    def open_connection_pools(self):
        logger.info("Creating connection pools.")
        password = urllib.parse.quote(os.getenv("DB_PASSWORD"))
        user = urllib.parse.quote(os.getenv("DB_USER"))
        db_url = urllib.parse.quote(os.getenv("DB_URL"))
        db_table = urllib.parse.quote(os.getenv("DB_DATATABLE"))
        connString = f'postgresql+psycopg2://{user}:{password}@{db_url}/{db_table}'
        self._db_engine = create_engine(connString,
                                        max_overflow=30,
                                        pool_size=30,
                                        pool_recycle=300,
                                        pool_timeout=300)

    def begin_session(self):
        self._db_session = Session(bind=self._db_engine, autocommit=True)

    def get_session(self):
        if self._db_session is None:
            self.begin_session()
        return self._db_session

    def close_session(self):
        if self._db_session is not None:
            self._db_session.close()

    def close_connection_pools(self):
        logger.info("Disposing connection pools.")
        self.close_session()
        if self._db_engine:
            self._db_engine.dispose()

    def DbEngine(self) -> Callable[[None], Awaitable[Engine]]:
        async def get_engine():
            assert self._db_engine is not None
            yield self._db_engine
        return get_engine


dbEngine = DBEngine()
