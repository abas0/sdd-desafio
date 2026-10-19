"""Estruturas de dados do motor (plan.md §3)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from motor.arredondamento import para_centavos


class EntradaInvalida(Exception):
    """Entrada que não atende à §4 da spec (RN-018)."""


@dataclass(frozen=True)
class Despesa:
    id: str
    data: date
    categoria_informada: str
    descricao: str
    fornecedor: str
    valor_informado: Decimal
    tem_nota_fiscal: bool
    posicao: int

    @property
    def valor(self):
        """Valor considerado, em centavos (RN-009)."""
        return para_centavos(self.valor_informado)


@dataclass(frozen=True)
class Ocorrencia:
    """Regra que se aplica a um item e a situação que ela determina (§4 da spec)."""

    situacao: str
    motivo: str
    regra: str
    referencia: str | None = None


@dataclass(frozen=True)
class SituacaoItem:
    """Resultado das etapas 3 a 5 da §8 da spec para um item (RN-019)."""

    despesa: Despesa
    ocorrencia: Ocorrencia | None
    outros_motivos: tuple = ()


@dataclass(frozen=True)
class TotalDiario:
    """Total de alimentação ou transporte urbano em um dia (RN-001 a RN-003). Valores em centavos."""

    data: date
    categoria: str
    itens: tuple
    valor_total: int
    em_viagem: bool
    origem_viagem: str | None
    limite: int
    valor_reembolsado: int
    situacao: str


@dataclass(frozen=True)
class Entrada:
    colaborador: dict
    periodo: dict
    inicio: date
    fim: date
    despesas: tuple
