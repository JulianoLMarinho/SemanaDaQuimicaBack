from typing import List
from fastapi import Depends
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, Inscricao, InscricaoAtividades
from app.repository.inscricaoRepository import InscricaoRepository


class InscricaoService:
    def __init__(self, repo: InscricaoRepository = Depends()):
        self.repo = repo

    def criarInscricao(self, inscricao: InscricaoAtividades):
        with self.repo.session.begin():
            try:
                inscricaoId = self.repo.adicionarInscricao(inscricao)
                for evento in inscricao.atividades:
                    self.repo.adicionarAtividadeInscricao(
                        inscricaoId.id, evento)
                self.repo.session.commit()
            except Exception as e:
                self.repo.session.rollback()
                raise e

    def obterAtividadesUsuario(self, usuario_id) -> List[AtividadeUsuario]:
        return self.repo.obterAtividadesUsuario(usuario_id)

    def obterInscricoes(self, usuario_id) -> List[Inscricao]:
        return self.repo.obterInscricoes(usuario_id)

    def obterInscricoesConfirmacao(self) -> List[Inscricao]:
        return self.repo.obterInscricoesConfirmacao()

    def obterAtividade(self, inscricao_id) -> List[Atividade]:
        return self.repo.obterAtividade(inscricao_id)

    def informarPagamento(self, inscricao_id, numero_documento):
        self.repo.informarPagamento(inscricao_id, numero_documento)

    def cancelarInscricao(self, inscricao_id):
        self.repo.alterarStatusInscricao(inscricao_id, 'CANCELADA')

    def confirmarInscricao(self, inscricao_id):
        self.repo.alterarStatusInscricao(inscricao_id, 'PAGAMENTO_CONFIRMADO')

    def totalInscricoesPagamentoInformado(self):
        total = self.repo.totalInscricoesPagamentoInformado()
        return total.total
