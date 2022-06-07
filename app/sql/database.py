from typing import Awaitable, Callable
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()


def DbEngine() -> Callable[[None], Awaitable[Engine]]:
    async def get_engine():
        password = urllib.parse.quote(os.getenv("DB_PASSWORD"))
        user = urllib.parse.quote(os.getenv("DB_USER"))
        db_url = urllib.parse.quote(os.getenv("DB_URL"))
        db_table = urllib.parse.quote(os.getenv("DB_DATATABLE"))
        connString = f'postgresql+psycopg2://{user}:{password}@{db_url}/{db_table}'
        return create_engine(connString)
    return get_engine