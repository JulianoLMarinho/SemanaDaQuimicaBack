from typing import List
from fastapi import Depends
from app.model.atividades import Atividade
from app.model.inscricao import AtividadeUsuario, Inscricao, InscricaoAtividades
from app.repository.inscricaoRepository import InscricaoRepository


class InscricaoService:
    def __init__(self, repo: InscricaoRepository = Depends()):
        self.repo = repo

    async def criarInscricao(self, inscricao: InscricaoAtividades):
        with self.repo.session.begin():
            try:
                inscricaoId = await self.repo.adicionarInscricao(inscricao)
                for evento in inscricao.atividades:
                    await self.repo.adicionarAtividadeInscricao(inscricaoId.id, evento)
                self.repo.session.commit()
            except Exception as e:
                self.repo.session.rollback()
                raise e

    async def obterAtividadesUsuario(self, usuario_id) -> List[AtividadeUsuario]:
        return await self.repo.obterAtividadesUsuario(usuario_id)

    async def obterInscricoes(self, usuario_id) -> List[Inscricao]:
        return await self.repo.obterInscricoes(usuario_id)

    async def obterInscricoesConfirmacao(self) -> List[Inscricao]:
        return await self.repo.obterInscricoesConfirmacao()

    async def obterAtividade(self, inscricao_id) -> List[Atividade]:
        return await self.repo.obterAtividade(inscricao_id)

    async def informarPagamento(self, inscricao_id, numero_documento):
        await self.repo.informarPagamento(inscricao_id, numero_documento)

    async def cancelarInscricao(self, inscricao_id):
        await self.repo.alterarStatusInscricao(inscricao_id, 'CANCELADA')

    async def confirmarInscricao(self, inscricao_id):
        await self.repo.alterarStatusInscricao(inscricao_id, 'PAGAMENTO_CONFIRMADO')

    async def totalInscricoesPagamentoInformado(self):
        total = await self.repo.totalInscricoesPagamentoInformado()
        return total.total
