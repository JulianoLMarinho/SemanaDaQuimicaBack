from pydantic import BaseModel


class InscricoesEdicao(BaseModel):
    nome: str
    email: str
    nivel: str
    curso: str
    universidade: str
    tamanho_camisa: str
    genero: str
    numero_atividades: int


class TotaisAtividades(BaseModel):
    titulo: str
    vagas: int
    vagas_restantes: int
    inscricoes_confirmadas: int
    inscricoes_canceladas: int
    inscricoes_aguardando_pagamento: int
    inscricoes_pagamento_informado: int
