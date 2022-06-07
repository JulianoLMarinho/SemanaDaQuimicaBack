from app.repository.baseRepository import BaseRepository
from app.sql.crud import query_db


class AuthorizationRepository(BaseRepository):

    def test(self):
        query = "SELECT * FROM usuario"
        return query_db(self.connection, query)
