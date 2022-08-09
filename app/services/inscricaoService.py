import asyncio
from typing import List
from fastapi import Depends
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, Inscricao, InscricaoAtividades
from app.model.tabelas import InscricoesEdicao
from app.model.usuario import NomeEmail
from app.repository.atividadesRepository import AtividadesRepository
from app.repository.inscricaoRepository import InscricaoRepository
from app.services.emailService import EmailService


class InscricaoService:
    def __init__(self, repo: InscricaoRepository = Depends(), atividadeRepo: AtividadesRepository = Depends(), emailService: EmailService = Depends()):
        self.repo = repo
        self.email = emailService
        self.atividadeRepo = atividadeRepo

    async def criarInscricao(self, inscricao: InscricaoAtividades, lock: asyncio.Lock):
        inscricaoId = 0
        transaction = self.repo.connection.begin()
        try:
            await lock.acquire()
            atividades = self.atividadeRepo.getAtividadesDetalhesByIds(
                inscricao.atividades)
            erros = []
            for atividade in atividades:
                if atividade.total_inscritos >= atividade.vagas:
                    erros.append(
                        f"A atividade {atividade.titulo} não possui mais vagas.")
            if len(erros) > 0:
                transaction.rollback()
                return erros
            inscricaoId = self.repo.adicionarInscricao(inscricao)
            for evento in inscricao.atividades:
                self.repo.adicionarAtividadeInscricao(
                    inscricaoId.id, evento)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        finally:
            lock.release()
        return inscricaoId.id

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

    def obterInscricoesPorAtividade(self, atividadeId: int) -> List[NomeEmail]:
        return self.repo.obterInscricoesPorAtividade(atividadeId)

    def obterInscricoesPorEdicao(self, edicaoId: int) -> List[InscricoesEdicao]:
        return self.repo.obterInscricoesPorEdicao(edicaoId)

    def obterInscricoesAguardandoPagamento3Dias(self) -> List[Inscricao]:
        return self.repo.obterInscricoesAguardandoPagamento3Dias()
