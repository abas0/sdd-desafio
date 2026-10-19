from motor.agregacao import totais_diarios
from motor.modelo import SituacaoItem
from tests.fabrica import despesa, em_ordem


def test_rn003_valor_reembolsado_e_do_total_do_dia_nao_dos_itens():
    itens = [SituacaoItem(d, None) for d in em_ordem(
        despesa(id="d-001", data="2026-07-03", valor="72.50"),
        despesa(id="d-002", data="2026-07-03", valor="38.00"),
    )]
    totais = totais_diarios(itens, {})
    assert len(totais) == 1
    assert totais[0].itens == ("d-001", "d-002")
    assert totais[0].valor_reembolsado == 6000


def test_rn003_dia_com_um_unico_item_corresponde_a_esse_item():
    [total] = totais_diarios([SituacaoItem(despesa(id="d-014", data="2026-07-31", categoria="ALIMENTACAO", valor="61.00"), None)], {})
    assert total.itens == ("d-014",)
    assert total.categoria == "alimentacao"
    assert total.valor_reembolsado == 6000
