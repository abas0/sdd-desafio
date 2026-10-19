"""Estruturas de dados do motor (plan.md §3)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


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


@dataclass(frozen=True)
class Entrada:
    colaborador: dict
    periodo: dict
    inicio: date
    fim: date
    despesas: tuple
