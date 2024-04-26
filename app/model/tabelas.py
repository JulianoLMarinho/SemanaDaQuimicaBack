from typing import Optional
from pydantic import BaseModel


class InscricoesEdicao(BaseModel):
    nome: str
    email: str
    nivel: Optional[str]
    curso: Optional[str]
    universidade: Optional[str]
    tamanho_camisa: Optional[str]
    genero: Optional[str]
    numero_atividades: int


class TotaisAtividades(BaseModel):
    titulo: str
    vagas: int
    vagas_restantes: int
    inscricoes_confirmadas: int
    inscricoes_canceladas: int
    inscricoes_aguardando_pagamento: int
    inscricoes_pagamento_informado: int
