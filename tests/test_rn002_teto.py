from datetime import date

import pytest

from motor.agregacao import totais_diarios
from motor.modelo import SituacaoItem
from tests.fabrica import despesa


def total_do_dia(valor, categoria="alimentacao", viagem=None):
    item = despesa(data="2026-07-06", categoria=categoria, descricao="Corrida almoço", valor=valor)
    [total] = totais_diarios([SituacaoItem(item, None)], viagem or {})
    return total


@pytest.mark.parametrize(
    "valor, categoria, reembolsado, situacao",
    [
        ("61.00", "alimentacao", 6000, "parcial"),
        ("60.00", "alimentacao", 6000, "integral"),
        ("60.01", "alimentacao", 6000, "parcial"),
        ("80.01", "transporte_urbano", 8000, "parcial"),
        ("80.00", "transporte_urbano", 8000, "integral"),
        ("54.90", "alimentacao", 5490, "integral"),
    ],
)
def test_rn002_reembolso_nunca_excede_o_limite(valor, categoria, reembolsado, situacao):
    total = total_do_dia(valor, categoria)
    assert (total.valor_reembolsado, total.situacao) == (reembolsado, situacao)


def test_rn002_d001_e_d002_somam_110_50_e_reembolsam_60():
    itens = [
        SituacaoItem(despesa(id="d-001", data="2026-07-03", valor="72.50", posicao=0), None),
        SituacaoItem(despesa(id="d-002", data="2026-07-03", valor="38.00", posicao=1), None),
    ]
    [total] = totais_diarios(itens, {})
    assert (total.valor_total, total.limite, total.valor_reembolsado) == (11050, 6000, 6000)


@pytest.mark.parametrize(
    "categoria, valor, limite, reembolsado",
    [("alimentacao", "95.00", 9000, 9000), ("transporte_urbano", "100.00", 12000, 10000)],
)
def test_rn002_limite_ampliado_em_dia_de_viagem(categoria, valor, limite, reembolsado):
    total = total_do_dia(valor, categoria, {date(2026, 7, 6): "estadia de x"})
    assert (total.em_viagem, total.limite, total.valor_reembolsado) == (True, limite, reembolsado)
