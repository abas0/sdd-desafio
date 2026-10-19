"""Criação de despesas para os testes."""

from dataclasses import replace
from datetime import date
from decimal import Decimal

from motor.modelo import Despesa


def despesa(
    id="d-001",
    data="2026-07-06",
    categoria="alimentacao",
    descricao="Almoço",
    fornecedor="Restaurante",
    valor="30.00",
    nota=True,
    posicao=0,
):
    return Despesa(
        id=id,
        data=date.fromisoformat(data),
        categoria_informada=categoria,
        descricao=descricao,
        fornecedor=fornecedor,
        valor_informado=Decimal(valor),
        tem_nota_fiscal=nota,
        posicao=posicao,
    )


def em_ordem(*despesas):
    """Numera as despesas na ordem dada, como se viessem nessa ordem no arquivo."""
    return tuple(replace(d, posicao=i) for i, d in enumerate(despesas))
