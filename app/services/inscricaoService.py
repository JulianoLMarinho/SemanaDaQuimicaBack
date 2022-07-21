from typing import List
from fastapi import Depends
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, Inscricao, InscricaoAtividades
from app.repository.inscricaoRepository import InscricaoRepository
from app.services.emailService import EmailService


class InscricaoService:
    def __init__(self, repo: InscricaoRepository = Depends(), emailService: EmailService = Depends()):
        self.repo = repo
        self.email = emailService

    def criarInscricao(self, inscricao: InscricaoAtividades):
        inscricaoId = 0
        with self.repo.session.begin():
            try:
                inscricaoId = self.repo.adicionarInscricao(inscricao)
                for evento in inscricao.atividades:
                    self.repo.adicionarAtividadeInscricao(
                        inscricaoId.id, evento)
                self.repo.session.commit()
                return inscricaoId.id
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

    def enviarEmailConfirmacaoInscricao(self, usuarioEmail: str, inscricaoId: int):
        atividades = self.obterAtividade(inscricaoId)

        mensagem = f"<p>Sua inscrição com identificação {inscricaoId} na(s) atividade(s):<br>"
        for atividade in atividades:
            mensagem += "<span style='margin-left: 20px'><b>" + \
                atividade.titulo + "</b></span><br>"
        mensagem += "foi cadastrata e está aguardando o pagamento.</p>"
        self.email.sendEmail("Confirmação de Inscrição",
                             mensagem, usuarioEmail)

    def enviarEmailConfirmacaoPagamentoInscricao(self, inscricaoId: int):
        atividades = self.obterAtividade(inscricaoId)
        usuario = self.repo.obterUsuarioPorInscricao(inscricaoId)
        mensagem = f"<p>O pagamento da sua inscrição com identificação {inscricaoId} na(s) atividade(s):<br>"
        for atividade in atividades:
            mensagem += "<span style='margin-left: 20px'><b>" + \
                atividade.titulo + "</b></span><br>"
        mensagem += "foi confirmado.</p>"
        self.email.sendEmail("Confirmação de Pagamento",
                             mensagem, usuario.email)

    def enviarEmailCancelamentoInscricao(self, inscricaoId: int):
        atividades = self.obterAtividade(inscricaoId)
        usuario = self.repo.obterUsuarioPorInscricao(inscricaoId)
        mensagem = f"<p>A sua inscrição com identificação {inscricaoId} na(s) atividade(s):<br>"
        for atividade in atividades:
            mensagem += "<span style='margin-left: 20px'><b>" + \
                atividade.titulo + "</b></span><br>"
        mensagem += "foi cancelada.</p>"
        mensagem += "<p>Se você acha que isto foi um engano, entre em contato com a Comissão Organizadora da Semana da Química.</p>"
        self.email.sendEmail("Cancelamento de Inscrição",
                             mensagem, usuario.email)
