import logging
from typing import Awaitable, Callable, Dict, Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os
from dotenv import load_dotenv
import urllib.parse

logger = logging.getLogger("uvicorn.error")

load_dotenv()

_db_engine: Optional[Engine]


def open_connection_pools():
    global _db_engine
    logger.info("Creating connection pools.")
    password = urllib.parse.quote(os.getenv("DB_PASSWORD"))
    user = urllib.parse.quote(os.getenv("DB_USER"))
    db_url = urllib.parse.quote(os.getenv("DB_URL"))
    db_table = urllib.parse.quote(os.getenv("DB_DATATABLE"))
    connString = f'postgresql+psycopg2://{user}:{password}@{db_url}/{db_table}'
    _db_engine = create_engine(connString)


def close_connection_pools():
    global _db_engine
    logger.info("Disposing connection pools.")
    if _db_engine:
        _db_engine.dispose()


def DbEngine() -> Callable[[None], Awaitable[Engine]]:
    async def get_engine():
        assert _db_engine is not None
        return _db_engine
    return get_engine
