from motor.regras_item import mesmo_conteudo
from tests.fabrica import despesa


def test_rn005_d006_e_d007_tem_mesmo_conteudo_apesar_dos_ids():
    d006 = despesa(id="d-006", data="2026-07-09", descricao="Almoco", fornecedor="Bistro Central", valor="54.90")
    d007 = despesa(id="d-007", data="2026-07-09", descricao="Almoco", fornecedor="Bistro Central", valor="54.90")
    assert mesmo_conteudo(d006, d007)


def test_rn005_textos_comparados_sem_maiusculas_acentos_e_espacos_a_mais():
    a = despesa(descricao="Almoço", fornecedor="Bistro Central")
    b = despesa(descricao="almoco", fornecedor="bistro  central ")
    assert mesmo_conteudo(a, b)


def test_rn005_d003_e_d004_tem_conteudo_diferente():
    d003 = despesa(id="d-003", categoria="transporte_urbano", descricao="Corrida aeroporto", fornecedor="TaxiApp", valor="100.00", nota=False)
    d004 = despesa(id="d-004", categoria="transporte_urbano", descricao="Corrida hotel", fornecedor="TaxiApp", valor="100.01", nota=False)
    assert not mesmo_conteudo(d003, d004)


def test_rn005_diferenca_so_na_nota_fiscal_e_conteudo_diferente():
    assert not mesmo_conteudo(despesa(nota=True), despesa(nota=False))


def test_rn005_valor_comparado_depois_do_arredondamento():
    assert mesmo_conteudo(despesa(valor="33.333"), despesa(valor="33.33"))
