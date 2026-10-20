from datetime import date

from motor.agregacao import calcular_hospedagem, totais_diarios
from motor.modelo import Entrada, SituacaoItem
from motor.regras_item import avaliar_situacoes, vincular_estornos_de_hospedagem
from tests.fabrica import despesa, em_ordem


def total(*despesas):
    [t] = totais_diarios([SituacaoItem(d, None) for d in em_ordem(*despesas)], {})
    return t


def corrida(valor, id="c"):
    return despesa(id=id, data="2026-07-06", categoria="transporte_urbano", descricao="Corrida", valor=valor, nota=True)


def test_rn016_estorno_abate_a_soma_do_dia_antes_do_limite():
    t = total(corrida("100.00", "a"), corrida("-45.00", "b"))
    assert (t.valor_total, t.valor_reembolsado, t.situacao) == (5500, 5500, "integral")


def test_rn016_soma_liquida_acima_do_limite_reembolsa_o_limite():
    t = total(corrida("150.00", "a"), corrida("-45.00", "b"))
    assert (t.valor_total, t.valor_reembolsado) == (10500, 8000)


def test_rn016_estorno_sozinho_no_dia_util_reembolsa_zero():
    t = total(corrida("-45.00"))
    assert (t.valor_total, t.valor_reembolsado, t.situacao) == (-4500, 0, "sem_valor")


def test_rn016_d009_estorno_no_sabado_fica_pendente_por_dia_nao_util():
    d009 = despesa(id="d-009", data="2026-07-11", categoria="transporte_urbano", descricao="Estorno de corrida cancelada", valor="-45.00", nota=False)
    [s] = avaliar_situacoes(Entrada({}, {}, date(2026, 7, 1), date(2026, 7, 31), em_ordem(d009)))
    assert (s.ocorrencia.situacao, s.ocorrencia.motivo) == ("pendente", "dia_nao_util")


def processar_hospedagem(*despesas):
    entrada = Entrada({}, {}, date(2026, 7, 1), date(2026, 7, 31), em_ordem(*despesas))
    return vincular_estornos_de_hospedagem(avaliar_situacoes(entrada))


def test_rn016_estorno_de_hospedagem_abatido_da_estadia_com_a_mesma_entrada():
    hotel = despesa(id="H", data="2026-07-14", categoria="hospedagem", descricao="Hotel - 2 diárias", valor="480.00")
    estorno = despesa(id="E", data="2026-07-14", categoria="hospedagem", descricao="Estorno diária hotel", valor="-80.00")
    situacoes, abatimentos = processar_hospedagem(hotel, estorno)
    assert situacoes[0].ocorrencia is None
    assert (situacoes[1].ocorrencia.situacao, situacoes[1].ocorrencia.referencia) == ("abatido", "H")
    calculo = calcular_hospedagem(situacoes[0].despesa, abatimentos[0])
    assert (calculo.valor_liquido, calculo.teto, calculo.valor_reembolsado) == (40000, 50000, 40000)


def test_rn016_estorno_de_hospedagem_sem_estadia_correspondente_fica_pendente():
    hotel = despesa(id="H", data="2026-07-14", categoria="hospedagem", descricao="Hotel - 2 diárias", valor="480.00")
    estorno = despesa(id="E", data="2026-07-16", categoria="hospedagem", descricao="Estorno taxa hotel", valor="-30.00")
    situacoes, abatimentos = processar_hospedagem(hotel, estorno)
    assert (situacoes[1].ocorrencia.situacao, situacoes[1].ocorrencia.motivo) == ("pendente", "estorno_sem_hospedagem")
    assert abatimentos == {}


def test_rn016_estorno_vinculado_a_hospedagem_pendente_acompanha_a_situacao_dela():
    airbnb = despesa(id="A", data="2026-07-22", categoria="hospedagem", descricao="Airbnb 3 noites", valor="690.00", nota=False)
    estorno = despesa(id="E", data="2026-07-22", categoria="hospedagem", descricao="Estorno limpeza Airbnb", valor="-50.00", nota=False)
    situacoes, abatimentos = processar_hospedagem(airbnb, estorno)
    o = situacoes[1].ocorrencia
    assert (o.situacao, o.motivo, o.referencia) == ("pendente", "nota_fiscal_ausente", "A")
    assert abatimentos == {}


def test_rn016_valor_liquido_negativo_da_hospedagem_reembolsa_zero():
    hotel = despesa(id="H", data="2026-07-14", categoria="hospedagem", descricao="Hotel - 1 diária", valor="100.00")
    estorno = despesa(id="E", data="2026-07-14", categoria="hospedagem", descricao="Estorno hotel", valor="-150.00")
    situacoes, abatimentos = processar_hospedagem(hotel, estorno)
    calculo = calcular_hospedagem(situacoes[0].despesa, abatimentos[0])
    assert (calculo.valor_liquido, calculo.valor_reembolsado) == (-5000, 0)
