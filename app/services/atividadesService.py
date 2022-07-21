from typing import List
from xmlrpc.client import Boolean, boolean

from fastapi import Depends
from app.model.atividades import Atividade, AtividadeCreate, AtividadeCreateComHorarioResponsavel, AtividadeLista, TipoAtividade, TurnoAtividade
from app.model.certificadoUsuario import CertificadoUsuario
from app.model.comum import OpcaoSelecao
from app.repository.atividadesRepository import AtividadesRepository
from app.repository.diaHorarioRepository import DiaHorarioRepository
from app.repository.responsavelRepository import ResponsavelRepository
from app.services.turnoService import TurnoService


class AtividadesService():

    def __init__(
        self,
        repository: AtividadesRepository = Depends(),
        responsavelRepository: ResponsavelRepository = Depends(),
        turnosService: TurnoService = Depends(),
        diaHoraRepository: DiaHorarioRepository = Depends()
    ):
        self.repo = repository
        self.turnosService = turnosService
        self.diaHoraRepo = diaHoraRepository
        self.responsavelRepo = responsavelRepository

    def getAtividadesByEdicao(self, idEdicao: int) -> List[Atividade]:
        return self.repo.getAtividadesByEdicao(idEdicao)

    def getAtividadesDetalhesByEdicao(self, idEdicao: int) -> List[AtividadeLista]:
        atividades = self.repo.getAtividadesDetalhesByEdicao(idEdicao)
        if len(atividades) > 0:
            atividadesIds = [a.id for a in atividades]
            responsaveis = self.repo.getResponsaveisByAtividades(atividadesIds)
            horarios = self.diaHoraRepo.obterDiaHorariosByAtividade(
                atividadesIds)
            for atividade in atividades:
                atividade.responsaveis = list(filter(
                    lambda x: x.id_atividade == atividade.id, responsaveis))
                atividade.horarios = list(filter(
                    lambda x: x.atividade_edicao_id == atividade.id, horarios
                ))
        return atividades

    def getAtividadesDetalhesByEdicaoAndTipo(self, idEdicao: int, tipoAtividade: List[str]) -> List[AtividadeLista]:
        atividades = self.repo.getAtividadesDetalhesByEdicaoAndTipo(
            idEdicao, tipoAtividade)
        if len(atividades) > 0:
            atividadesIds = [a.id for a in atividades]
            horarios = self.diaHoraRepo.obterDiaHorariosByAtividade(
                atividadesIds)
            responsaveis = self.repo.getResponsaveisByAtividades(atividadesIds)
            for atividade in atividades:
                atividade.responsaveis = list(filter(
                    lambda x: x.id_atividade == atividade.id, responsaveis))
                if atividade.turno_id:
                    atividade.horarios = list(filter(
                        lambda x: x.turno_id == atividade.turno_id, horarios
                    ))
                else:
                    atividade.horarios = list(filter(
                        lambda x: x.atividade_edicao_id == atividade.id, horarios
                    ))

        return atividades

    def getAtividadesDetalhesByEdicaoTurnoAndTipo(self, idEdicao: int, tipoAtividade: str) -> List[TurnoAtividade]:
        atividades = self.repo.getAtividadesDetalhesByEdicaoAndTipo(
            idEdicao, [tipoAtividade])
        returnValue: List[TurnoAtividade] = []
        if len(atividades) > 0:
            atividadesIds = [a.id for a in atividades]
            responsaveis = self.repo.getResponsaveisByAtividades(atividadesIds)
            turnos = self.turnosService.obterTurnosComHorario(idEdicao)
            for atividade in atividades:
                atividade.responsaveis = list(filter(
                    lambda x: x.id_atividade == atividade.id, responsaveis))
            for turno in turnos:
                turnoAtividade = list(
                    filter(lambda x: x.turno_id == turno.id, returnValue))
                if (len(turnoAtividade) != 1):
                    returnValue.append(TurnoAtividade(turno_id=turno.id, turno=turno, atividades=list(
                        filter(lambda x: x.turno_id == turno.id, atividades))))
        return returnValue

    def tipoAtividades(self) -> List[OpcaoSelecao]:
        return self.repo.tiposAtividades()

    def criarAtividade(self, atividade: AtividadeCreateComHorarioResponsavel) -> Boolean:
        with self.repo.session.begin():
            try:
                atividadeId = self.repo.criarAtividade(atividade)
                if atividade.turno_atividade != None:
                    self.repo.salvarTurnoAtividade(
                        atividade.turno_atividade, atividadeId.id)
                else:
                    for hor in atividade.horarios:
                        hor.atividade_edicao_id = atividadeId.id
                    self.repo.salvarHorariosAtividades(atividade.horarios)
                if len(atividade.responsavel_atividade) > 0:
                    for res in atividade.responsavel_atividade:
                        self.repo.salvarResponsavelAtividade(
                            atividadeId.id, res)
                self.repo.session.commit()
                return True
            except:
                self.repo.session.rollback()
                return False

    def atualizarAtividade(self, atividade: AtividadeCreate) -> Boolean:
        with self.repo.session.begin():
            try:
                self.repo.atualizarAtividade(atividade)
                self.turnosService.deletarTurnosByAtividade(atividade.id)
                self.diaHoraRepo.deletetarHorariosByAtividade(atividade.id)
                self.responsavelRepo.deletarResponsavelAtividadeByAtividade(
                    atividade.id)

                if atividade.turno_atividade != None:
                    self.repo.salvarTurnoAtividade(
                        atividade.turno_atividade, atividade.id)
                else:
                    for hor in atividade.horarios:
                        hor.atividade_edicao_id = atividade.id
                    self.repo.salvarHorariosAtividades(atividade.horarios)
                if len(atividade.responsavel_atividade) > 0:
                    for res in atividade.responsavel_atividade:
                        self.repo.salvarResponsavelAtividade(
                            atividade.id, res)
                self.repo.session.commit()
                return True
            except:
                self.repo.RollbackTransaction()
                raise Exception('Não foi possível salvar a atividade')

    def obterListaCertificadosUsuario(self, usuarioId: int) -> List[CertificadoUsuario]:
        return self.repo.obterListaCertificadosUsuario(usuarioId)

    def getResponsaveisByAtividade(self, atividadeId: int) -> List[str]:
        responsaveis = self.repo.getResponsaveisByAtividade(atividadeId)
        return [a.nome_responsavel for a in responsaveis]
