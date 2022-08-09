import logging
from typing import Awaitable, Callable, Dict, Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os
from dotenv import load_dotenv
import urllib.parse

logger = logging.getLogger("uvicorn.error")

load_dotenv()


class DBEngine:

    def __init__(self):
        self._db_engine: Optional[Engine] = None

    def open_connection_pools(self):
        logger.info("Creating connection pools.")
        password = urllib.parse.quote(os.getenv("DB_PASSWORD"))
        user = urllib.parse.quote(os.getenv("DB_USER"))
        db_url = urllib.parse.quote(os.getenv("DB_URL"))
        db_table = urllib.parse.quote(os.getenv("DB_DATATABLE"))
        connString = f'postgresql+psycopg2://{user}:{password}@{db_url}/{db_table}'
        self._db_engine = create_engine(connString)

    def close_connection_pools(self):
        logger.info("Disposing connection pools.")
        if self._db_engine:
            self._db_engine.dispose()

    def DbEngine(self) -> Engine:
        def get_engine():
            assert self._db_engine is not None
            return self._db_engine
        return get_engine


engine = DBEngine()
