from typing import List
from sqlalchemy import true
from app.model.edicaoSemana import Assinatura, CarouselImage, CarouselImageCreation, ComissaoEdicao, EdicaoLogo, EdicaoSemana, EdicaoSemanaComComissao, EdicaoSemanaCreate
from app.repository.baseRepository import BaseRepository
from app.sql.crud import exec_sql, exec_sql, insert_command_from_models, query_db, query_db, update_command_from_model


class EdicaoSemanaRepository(BaseRepository):
    def getEdicaoAtiva(self) -> EdicaoSemanaComComissao:
        query = """SELECT * FROM edicao_semana WHERE ativa = true"""
        return query_db(connection=self.connection, query=query, model=EdicaoSemanaComComissao, single=true)

    def updateTemaEdicaoAtiva(self, tema: str):
        query = f"UPDATE edicao_semana SET tema = :Tema WHERE ativa = true"
        exec_sql(self.connection, query, {'Tema': tema})

    def getEdicoes(self) -> List[EdicaoSemanaComComissao]:
        query = "SELECT * FROM edicao_semana ORDER BY data_inicio DESC"
        return query_db(connection=self.connection, query=query, model=EdicaoSemanaComComissao)

    def adicionarCarrousselImage(self, carrousselImage: CarouselImageCreation):
        columnsTable = CarouselImageCreation.construct().__fields__
        query = insert_command_from_models(
            'carousel_header', columnsTable, [carrousselImage])
        exec_sql(self.connection, query[0], query[1])

    def getCarouselEdicao(self, edicaoId: int) -> List[CarouselImage]:
        query = f"SELECT * FROM carousel_header WHERE edicao_semana_id = {edicaoId} ORDER BY ordem"
        return query_db(self.connection, query, model=CarouselImage)

    def editarCarouselImage(self, carouselImage: CarouselImage):
        query = update_command_from_model(
            'carousel_header', CarouselImage.construct().__fields__) + """ WHERE id = :id"""
        exec_sql(self.connection, query, carouselImage.dict())

    def deletarCarouselImage(self, carouselImageId: int):
        query = f'DELETE FROM carousel_header WHERE id = {carouselImageId}'
        exec_sql(self.connection, query)

    def adicionarEdicaoSemana(self, edicaoSemana: EdicaoSemanaCreate):
        columnsTable = EdicaoSemanaCreate.construct().__fields__
        query = insert_command_from_models(
            'edicao_semana', columnsTable, [edicaoSemana])
        return query_db(self.connection, query[0] + " RETURNING id", query[1], single=True)

    def editarEdicaoSemana(self, edicaoSemana: EdicaoSemana):
        query = update_command_from_model(
            'edicao_semana', EdicaoSemana.construct().__fields__) + " WHERE id = :id"
        exec_sql(self.connection, query, edicaoSemana.dict())

    def deletarEdicaoSemana(self, edicaoSemanaId: int):
        query = f"DELETE FROM edicao_semana WHERE id = {edicaoSemanaId}"
        exec_sql(self.connection, query)

    def obterQuemSomos(self, edicaoSemanaId: int) -> List[ComissaoEdicao]:
        query = f"""SELECT r.*, ec.edicao_semana_id FROM responsavel r
                    INNER JOIN edicao_comissao ec ON ec.responsavel_id = r.id
                                                        AND ec.edicao_semana_id = {edicaoSemanaId}"""
        return query_db(self.connection, query, model=ComissaoEdicao)

    def liberarCertificados(self, edicaoSemanaId: int, liberar: bool):
        query = f"UPDATE edicao_semana SET certificado_liberado = :Liberar WHERE id = :EdicaoSemanaId"
        params = {
            'Liberar': liberar,
            'EdicaoSemanaId': edicaoSemanaId
        }
        exec_sql(self.connection, query, params)

    def aceitarInscricoesAtividades(self, edicaoSemanaId: int, aceitarInscricao: bool):
        query = f"UPDATE edicao_semana SET aceita_inscricao_atividade = :AceitarInscricao WHERE id = :EdicaoSemanaId"
        params = {
            'AceitarInscricao': aceitarInscricao,
            'EdicaoSemanaId': edicaoSemanaId
        }
        exec_sql(self.connection, query, params)

    def salvarLogo(self, edicaoLogo: EdicaoLogo):
        if edicaoLogo.tipo_logo == 'logo':
            query = f"UPDATE edicao_semana SET logo = :logo WHERE id = :edicao_semana_id"
        else:
            query = f"UPDATE edicao_semana SET logo_completa = :logo WHERE id = :edicao_semana_id"
        exec_sql(self.connection, query, edicaoLogo.dict())

    def salvarAssinaturaPresidente(self, assinatura: Assinatura):
        if assinatura.tipo_assinatura == 'presidente':
            query = """UPDATE edicao_semana SET assinatura_presidente_edicao = :assinatura,
                       presidente_edicao = :nome 
                       WHERE id = :edicao_semana_id"""
        elif assinatura.tipo_assinatura == 'direcao':
            query = """UPDATE edicao_semana SET assinatura_direcao_instituto = :assinatura,
                       direcao_instituto = :nome 
                       WHERE id = :edicao_semana_id"""
        exec_sql(self.connection, query, assinatura.dict())

    def ativarSiteEmConstrucao(self, edicaoSemanaId: int, siteEmConstrucao: bool):
        query = f"UPDATE edicao_semana SET site_em_construcao = :SiteEmConstrucao WHERE id = :EdicaoSemanaId"
        params = {
            'SiteEmConstrucao': siteEmConstrucao,
            'EdicaoSemanaId': edicaoSemanaId
        }
        exec_sql(self.connection, query, params)

    def salvarQuemSomos(self, quemSomosTexto: str, edicaoSemanaId: int):
        query = "UPDATE edicao_semana SET quem_somos = :QuemSomos WHERE id = :EdicaoSemanaId"
        params = {
            "QuemSomos": quemSomosTexto,
            "EdicaoSemanaId": edicaoSemanaId
        }
        exec_sql(self.connection, query, params)
