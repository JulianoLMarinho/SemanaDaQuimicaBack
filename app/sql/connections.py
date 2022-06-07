
from typing import AsyncIterable, Callable
from sqlalchemy.engine import Connection
from fastapi.params import Depends
from app.sql.database import DbEngine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from time import time


def UseConnection() -> Callable[..., AsyncIterable[Connection]]:
    async def CustomConnection(db_engine=Depends(DbEngine())) -> AsyncIterable[Connection]:
        session = Session(bind=db_engine, autocommit=True)
        start_time = time()
        try:
            yield session.connection()
        finally:
            elapsed_time = time() - start_time
            session.close()
    return CustomConnection


def UseSession() -> sessionmaker:
    async def CustomSession(db_engine=Depends(DbEngine())) -> AsyncIterable[sessionmaker]:
        # Session(bind=db_engine, autocommit=True)
        Session = sessionmaker(bind=db_engine)
        start_time = time()
        try:
            yield Session()
        finally:
            Session.close_all()
    return CustomSession


MainConnection: Callable[..., AsyncIterable[Connection]] = UseConnection()
MainSession: sessionmaker = UseSession()
