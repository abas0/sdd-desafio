from motor.regras_item import sobreposicoes
from tests.fabrica import despesa, em_ordem


def hotel(id, data, diarias, valor="400.00"):
    return despesa(id=id, data=data, categoria="hospedagem", descricao=f"Hotel - {diarias} diárias", valor=valor)


def test_rn017_noite_em_comum_deixa_as_duas_pendentes():
    ocorrencias = sobreposicoes(em_ordem(hotel("A", "2026-07-20", 2), hotel("B", "2026-07-21", 1)))
    assert sorted(ocorrencias) == [0, 1]
    assert all(o.situacao == "pendente" and o.motivo == "sobreposicao_hospedagem" for o in ocorrencias.values())


def test_rn017_saida_no_dia_da_entrada_seguinte_nao_e_sobreposicao():
    assert sobreposicoes(em_ordem(hotel("A", "2026-07-20", 2), hotel("B", "2026-07-22", 1))) == {}


def test_rn017_d010_e_d013_nao_se_sobrepoem():
    d010 = despesa(id="d-010", data="2026-07-14", categoria="hospedagem", descricao="Hotel Rio - 2 diarias", valor="480.00")
    d013 = despesa(id="d-013", data="2026-07-22", categoria="hospedagem", descricao="Airbnb 3 noites", valor="690.00", nota=False)
    assert sobreposicoes(em_ordem(d010, d013)) == {}


def test_rn017_estorno_com_a_mesma_data_de_entrada_nao_e_sobreposicao():
    estorno = despesa(id="E", data="2026-07-14", categoria="hospedagem", descricao="Estorno diária hotel", valor="-80.00")
    assert sobreposicoes(em_ordem(hotel("A", "2026-07-14", 2, "480.00"), estorno)) == {}


def test_rn017_itens_excluidos_nas_etapas_anteriores_nao_participam():
    despesas = em_ordem(hotel("A", "2026-07-20", 2), hotel("B", "2026-07-21", 1))
    assert sobreposicoes(despesas, excluidas={1}) == {}


def test_rn017_cadeia_de_sobreposicoes_deixa_todas_pendentes():
    despesas = em_ordem(hotel("A", "2026-07-20", 2), hotel("B", "2026-07-21", 2), hotel("C", "2026-07-22", 1))
    assert sorted(sobreposicoes(despesas)) == [0, 1, 2]
