from typing import List, Tuple
from app.model.usuario import Usuario
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_sql, query_db


class UserRepository(BaseRepository):

    def get_all_users(self):
        query = "SELECT * FROM usuario"
        return query_db(self.connection, query)

    def getUserByEmail(self, email: str) -> Usuario:
        query = f"""SELECT u.*, pu.codigo_perfil AS perfil FROM usuario u
                    INNER JOIN perfil_usuario pu ON pu.id = u.perfil_usuario
                    WHERE email = :UserEmail"""
        params = {
            'UserEmail': email
        }
        result = query_db(connection=self.connection, params=params,
                          query=query, single=True, model=Usuario)
        return result

    def getUserByEmailAndGoogleUser(self, email: str, googleUserId: str):
        query = "SELECT * FROM usuario WHERE email = :UserEmail AND 'id_google' = :GoogleUserId"
        params = {
            'UserEmail': email,
            'GoogleUserId': googleUserId
        }
        return query_db(self.connection, query, params, single=True)

    def addUser(self, usuario: Usuario):
        query = """INSERT INTO usuario(nome, 
                                       url_foto_perfil, 
                                       estado, 
                                       cidade,  
                                       email, 
                                       id_google, 
                                       universidade,  
                                       curso, 
                                       nivel, 
                                       tamanho_camisa, 
                                       genero,
                                       perfil_usuario)
                    VALUES(:Nome, 
                           :UrlFotoPerfil,
                           :Estado,
                           :Cidade, 
                           :Email, 
                           :IdGoogle, 
                           :Universidade, 
                           :Curso, 
                           :Nivel, 
                           :TamanhoCamisa, 
                           :Genero,
                           1)"""
        params = {
            'Nome': usuario.nome,
            'UrlFotoPerfil': usuario.url_foto_perfil,
            'Email': usuario.email,
            'IdGoogle': usuario.id_google,
            'Universidade': usuario.universidade,
            'Curso': usuario.curso,
            'Nivel': usuario.nivel,
            'TamanhoCamisa': usuario.tamanho_camisa,
            'Genero': usuario.genero,
            'Cidade': usuario.cidade,
            'Estado': usuario.estado
        }
        exec_sql(self.connection, query, params)

    def getUserById(self, userId: int) -> Usuario:
        query = f"SELECT * FROM usuario WHERE id = {userId}"
        return query_db(query=query, connection=self.connection, single=True)

    def updateUser(self, user: Usuario):
        query = f"""UPDATE usuario SET
                        nome = :nome
                        ,url_foto_perfil = :url_foto_perfil
                        ,estado = :estado
                        ,cidade = :cidade
                        ,email = :email
                        ,id_google = :id_google
                        ,universidade =  :universidade
                        ,curso = :curso
                        ,nivel = :nivel
                        ,tamanho_camisa = :tamanho_camisa
                        ,genero = :genero
                    WHERE id = :id"""
        exec_sql(self.connection, query, user.dict())

    def getPermissaoUsuario(self, userId: int) -> List[str]:
        query = """SELECT p.codigo_permissao
                    FROM permissao p
                    INNER JOIN perfil_permissao pp ON pp.id_permissao = p.id
                    INNER JOIN usuario u ON u.perfil_usuario = pp.id_perfil
                    WHERE u.id = :ID"""
        return query_db(self.connection, query, {"ID": userId})
