from typing import List
from app.model.carrouselInicio import CarrouselInicio
from app.repository.baseRepository import BaseRepository
from app.sql.crud import query_db


class CarrouselInicioRepository(BaseRepository):

    def getImages(self) -> List[CarrouselInicio]:
        query = "SELECT id, edicao_semana_id, encode(imagem, 'base64') as imagem FROM caroussel_header"
        return query_db(self.connection, query, model=CarrouselInicio)
