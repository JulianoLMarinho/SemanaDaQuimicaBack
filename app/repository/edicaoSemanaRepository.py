from typing import List
from sqlalchemy import true
from app.model.edicaoSemana import CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaCreate
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_session_sql, exec_sql, insert_command_from_models, query_db, query_db_session, update_command_from_model


class EdicaoSemanaRepository(BaseRepository):
    async def getEdicaoAtiva(self) -> EdicaoSemanaComComissao:
        query = """SELECT * FROM edicao_semana WHERE ativa = true"""
        return query_db(connection=self.connection, query=query, model=EdicaoSemanaComComissao, single=true)

    async def updateTemaEdicaoAtiva(self, tema: str):
        query = f"UPDATE edicao_semana SET tema = :Tema WHERE ativa = true"
        exec_sql(self.connection, query, {'Tema': tema})

    async def getEdicoes(self) -> List[EdicaoSemanaComComissao]:
        query = "SELECT * FROM edicao_semana ORDER BY data_inicio DESC"
        return query_db(connection=self.connection, query=query, model=EdicaoSemanaComComissao)

    async def adicionarCarrousselImage(self, carrousselImage: CarouselImageCreation):
        columnsTable = CarouselImageCreation.construct().__fields__
        query = insert_command_from_models(
            'carousel_header', columnsTable, [carrousselImage])
        exec_sql(self.connection, query[0], query[1])

    async def getCarouselEdicao(self, edicaoId: int) -> List[CarouselImage]:
        query = f"SELECT * FROM carousel_header WHERE edicao_semana_id = {edicaoId} ORDER BY ordem"
        return query_db(self.connection, query, model=CarouselImage)

    async def editarCarouselImage(self, carouselImage: CarouselImage):
        query = update_command_from_model(
            'carousel_header', CarouselImage.construct().__fields__) + """ WHERE id = :id"""
        exec_sql(self.connection, query, carouselImage.dict())

    async def deletarCarouselImage(self, carouselImageId: int):
        query = f'DELETE FROM carousel_header WHERE id = {carouselImageId}'
        exec_sql(self.connection, query)

    async def adicionarEdicaoSemana(self, edicaoSemana: EdicaoSemanaCreate):
        columnsTable = EdicaoSemanaCreate.construct().__fields__
        query = insert_command_from_models(
            'edicao_semana', columnsTable, [edicaoSemana])
        return query_db_session(self.session, query[0] + " RETURNING id", query[1], single=True)

    async def editarEdicaoSemana(self, edicaoSemana: EdicaoSemana):
        query = update_command_from_model(
            'edicao_semana', EdicaoSemana.construct().__fields__) + " WHERE id = :id"
        exec_session_sql(self.session, query, edicaoSemana.dict())

    async def deletarEdicaoSemana(self, edicaoSemanaId: int):
        query = f"DELETE FROM edicao_semana WHERE id = {edicaoSemanaId}"
        exec_session_sql(self.session, query)

    async def obterQuemSomos(self, edicaoSemanaId: int) -> List[ComissaoEdicao]:
        query = f"""SELECT r.*, ec.edicao_semana_id FROM responsavel r
                    INNER JOIN edicao_comissao ec ON ec.responsavel_id = r.id
                                                        AND ec.edicao_semana_id = {edicaoSemanaId}"""
        return query_db(self.connection, query, model=ComissaoEdicao)
