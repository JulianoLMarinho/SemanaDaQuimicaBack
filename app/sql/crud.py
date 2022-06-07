from dataclasses import dataclass, is_dataclass
import time
import json
from types import FunctionType
from typing import Any, Dict, List, Tuple, Union

from sqlalchemy.engine import Connection, CursorResult
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

from app.logger import logger


def columns(o: BaseModel, prefix='') -> str:
    """
    Returns the string of columns for the given model in the SQL Server format.
    Ex: [OrderDetailId],[BusinessUnitId],[Qty]
    """
    column_str = ",".join(
        [f"{prefix + '.' if prefix else ''}{f}" for f in o.construct().__fields__])
    return column_str


def columnsList(o: BaseModel, prefix='') -> str:
    """
    Returns the string of columns for the given model in the SQL Server format.
    Ex: [OrderDetailId],[BusinessUnitId],[Qty]
    """
    cols = columns(o, prefix)
    return cols.split(',')


def log_query(query: str):
    """
    Cleans and logs a query
    """
    query_parts = query.replace('\n', '<ENTER>').replace(
        '<ENTER><ENTER>', '<ENTER>').split()
    clean_query = ' '.join(query_parts).replace('<ENTER>', '\n')
    logger.info(clean_query)


def update_command_from_model(table: str, columns: List[str]) -> str:
    query = f"""UPDATE {table} SET """
    for column in columns:
        query += f""" {column} = :{column},"""
    query = query[0:-1]

    return query


def insert_command_from_models(table: str,
                               columns: List[str], models: List[Any],
                               model_preprocessor: FunctionType = None) -> Tuple[str, Dict]:
    """
    Creates an INSERT statement and a dictionary of parameters from
    a list of models.

    The *model_preprocessor* is a function that receives a model and will
    be called before each model is converted into a dict. It may
    be used to set values for each given model.
    """

    values_clauses = []
    flatened_parameters = {}
    for index, model in enumerate(models, start=1):
        if model_preprocessor:
            model_preprocessor(model)
        values_clauses.append(
            f"""({ ','.join([ f':{c}{index}' for c in columns ]) })"""
        )
        for attribute, value in model.__dict__.items():
            if attribute in columns:
                flatened_parameters[f"{attribute}{index}"] = value

    values_string = ',\n'.join(values_clauses)
    created_insert = f"""INSERT INTO {table}
        ({ ','.join([ f'{c}' for c in columns  ])}) 
        VALUES 
        { values_string }"""

    return created_insert, flatened_parameters


def get_insert_query_parameter(entity: List[BaseModel], database: str, model: Union[BaseModel, dataclass]):
    columnsTable = model.construct().__fields__
    query = insert_command_from_models(
        database, columnsTable, entity)
    return query


def expand_list_parameters(query: str, params: dict) -> Tuple[str, dict]:
    """
    Allows using a list as a parameter. Required for statements that
    use the IN clause.
    """
    parameters = [*params.keys()]
    for parameter in parameters:
        if isinstance(params[parameter], List):
            num_of_subparams = len(params[parameter])
            # expand query parameter
            subparams = [f":{parameter}{i}" for i in range(num_of_subparams)]
            subparam_str = f"({','.join(subparams)})"
            query = query.replace(f":{parameter}", subparam_str)
            # expand parameter value
            list_of_subparams = params.pop(parameter, None)
            for i, subparam in enumerate(list_of_subparams):
                params[f"{parameter}{i}"] = subparam
    return query, params


def exec_sql(connection: Connection, query: str, params: dict = {}, n_retries=3, log=False) -> CursorResult:
    if log:
        log_query(query)
        logger.info(repr(params))

    query, params = expand_list_parameters(query, params)
    query_text = text(query)
    for i in range(n_retries + 1):
        try:

            rs = connection.execute(query_text, params)
            return rs
        except Exception as error:
            logger.warning(error)
            logger.warning("Retrying in 1 second")
            time.sleep(1)
            if i == n_retries:
                raise error
            continue
    raise Exception


def exec_session_sql(session: sessionmaker, query: str, params: dict = {}, n_retries=3, log=False) -> CursorResult:
    if log:
        log_query(query)
        logger.info(repr(params))

    query, params = expand_list_parameters(query, params)
    query_text = text(query)
    for i in range(n_retries + 1):
        try:

            rs = session.execute(query_text, params)
            return rs
        except Exception as error:
            logger.warning(error)
            logger.warning("Retrying in 1 second")
            time.sleep(1)
            if i == n_retries:
                raise error
            continue
    raise Exception


def query_db(connection: Connection, query: str, params: dict = {},
             model: Union[BaseModel, dataclass] = None, log=False, single=False):
    """Execute a query that returns rows in the database. 
    Returned rows may be automatically parsed into a Pydantic model or dataclass
    by passing a class to the model parameter.
    It may also log the query according to the log parameter.
    The single flag may be used if the query is expected to return a single result,
    in this case, the function will return the first result or None
    """
    rs = exec_sql(connection, query, params, log=log)
    return query_db_common(rs, model, log, single)


def query_db_session(session: sessionmaker, query: str, params: dict = {},
                     model: Union[BaseModel, dataclass] = None, log=False, single=False):
    """Execute a query that returns rows in the database. 
    Returned rows may be automatically parsed into a Pydantic model or dataclass
    by passing a class to the model parameter.
    It may also log the query according to the log parameter.
    The single flag may be used if the query is expected to return a single result,
    in this case, the function will return the first result or None
    """
    rs = exec_session_sql(session, query, params, log=log)
    return query_db_common(rs, model, log, single)


def query_db_common(rs: Any, model: Union[BaseModel, dataclass] = None, log=False, single=False):
    if model and issubclass(model, BaseModel):
        r = [model.parse_obj(row) for row in rs]
    elif is_dataclass(model):
        r = [model(**row._mapping) for row in rs]
    else:
        r = [row._mapping for row in rs]
    if log:
        logger.info(f"{len(r)} rows")
    if single:
        try:
            r = r[0]
        except IndexError:
            return None
    return r


def read_json(connection: Connection, query: str, params: dict = {}):
    rs = exec_sql(connection, query, params)
    result_string = "".join([row[0] for row in rs])
    result_json = json.loads(result_string)
    return result_json
