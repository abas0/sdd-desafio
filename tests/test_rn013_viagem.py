from datetime import date, timedelta

from motor.viagem import dias_de_viagem
from tests.fabrica import despesa, em_ordem

D010 = despesa(id="d-010", data="2026-07-14", categoria="hospedagem", descricao="Hotel Rio - 2 diarias", valor="480.00")
D013 = despesa(id="d-013", data="2026-07-22", categoria="hospedagem", descricao="Airbnb 3 noites", valor="690.00", nota=False)
D003 = despesa(id="d-003", data="2026-07-06", categoria="transporte_urbano", descricao="Corrida aeroporto", valor="100.00", nota=False)


def dias(inicio, n):
    return {date.fromisoformat(inicio) + timedelta(days=k) for k in range(n)}


def test_rn013_d010_cobre_14_15_e_16_de_julho():
    assert set(dias_de_viagem(em_ordem(D010))) == dias("2026-07-14", 3)


def test_rn013_d013_pendente_de_nota_ainda_marca_22_a_25_de_julho():
    assert set(dias_de_viagem(em_ordem(D013))) == dias("2026-07-22", 4)


def test_rn013_palavra_de_viagem_marca_o_dia_do_item():
    viagem = dias_de_viagem(em_ordem(D003))
    assert viagem == {date(2026, 7, 6): '"aeroporto" em d-003'}


def test_rn013_origem_da_estadia_para_a_justificativa():
    assert dias_de_viagem(em_ordem(D010))[date(2026, 7, 15)] == "estadia de d-010"


def test_rn013_estorno_de_hospedagem_nao_marca_viagem():
    estorno = despesa(data="2026-07-14", categoria="hospedagem", descricao="Estorno 2 diárias", valor="-80.00")
    assert dias_de_viagem(em_ordem(estorno)) == {}


def test_rn013_item_sem_hospedagem_nem_palavra_de_viagem_nao_marca():
    assert dias_de_viagem(em_ordem(despesa(descricao="Almoço com cliente"))) == {}


def test_rn013_palavras_de_viagem_com_acento_e_plural():
    itens = em_ordem(
        despesa(id="a", data="2026-07-01", descricao="Táxi até a Rodoviária"),
        despesa(id="b", data="2026-07-02", descricao="Lanche entre voos"),
    )
    assert set(dias_de_viagem(itens)) == {date(2026, 7, 1), date(2026, 7, 2)}
