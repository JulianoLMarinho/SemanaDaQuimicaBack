from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.types import NonNegativeInt


class Usuario(BaseModel):
    id: NonNegativeInt
    nome: str
    estado: Optional[str]
    cidade: Optional[str]
    universidade: Optional[str]
    curso: Optional[str]
    nivel: Optional[str]
    tamanho_camisa: Optional[str]
    genero: Optional[str]
    email: str
    url_foto_perfil: Optional[str]
    id_google: Optional[str]
    perfil_usuario: Optional[int]
    permissoes: Optional[List[str]]
    perfil: Optional[str]

    class Config:
        allow_population_by_field_name = True

    def getUpdateData(self):
        query = 'UPDATE usuario SET '
        params = {}
        attr = vars(self)
        for field in self.__fields__:
            query += self.__fields__[field].alias
            query += " = :"+field+", "
            params[field] = attr[field]
        return query

    def getInsertQuery(self):
        query = "INSERT INTO usuario("
        query += ",".join([self.__fields__[field].alias for field in self.__fields__])+")"
        query += "("+", :".join([field for field in self.__fields__])+")"
        params = {}
        attr = vars(self)
        for field in self.__fields__:
            params[field] = attr[field]
        return (query, attr)
