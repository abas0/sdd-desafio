from datetime import date

from motor.agregacao import totais_diarios
from motor.modelo import SituacaoItem
from tests.fabrica import despesa, em_ordem


def situacoes(*despesas):
    return [SituacaoItem(d, None) for d in em_ordem(*despesas)]


def test_rn001_soma_as_despesas_da_mesma_categoria_na_mesma_data():
    [total] = totais_diarios(
        situacoes(
            despesa(id="d-001", data="2026-07-03", valor="72.50"),
            despesa(id="d-002", data="2026-07-03", valor="38.00"),
        ),
        {},
    )
    assert total.itens == ("d-001", "d-002")
    assert total.valor_total == 11050


def test_rn001_categorias_diferentes_nao_se_somam():
    totais = totais_diarios(
        situacoes(
            despesa(id="a", data="2026-07-03", valor="72.50"),
            despesa(id="b", data="2026-07-03", categoria="transporte_urbano", descricao="Corrida", valor="20.00"),
        ),
        {},
    )
    assert [(t.categoria, t.valor_total) for t in totais] == [("alimentacao", 7250), ("transporte_urbano", 2000)]


def test_rn001_datas_diferentes_nao_se_somam():
    totais = totais_diarios(situacoes(despesa(id="a", data="2026-07-03"), despesa(id="b", data="2026-07-06")), {})
    assert [t.data for t in totais] == [date(2026, 7, 3), date(2026, 7, 6)]


def test_rn001_item_com_ocorrencia_nao_entra_na_soma():
    from motor.modelo import Ocorrencia

    a, b = em_ordem(despesa(id="a", valor="30.00"), despesa(id="b", valor="40.00"))
    pendente = Ocorrencia("pendente", "nota_fiscal_ausente", "RN-012")
    [total] = totais_diarios([SituacaoItem(a, None), SituacaoItem(b, pendente)], {})
    assert total.itens == ("a",)
    assert total.valor_total == 3000


def test_rn001_hospedagem_nao_forma_total_diario():
    hotel = despesa(categoria="hospedagem", descricao="Hotel - 1 diária", valor="200.00")
    assert totais_diarios(situacoes(hotel), {}) == []
