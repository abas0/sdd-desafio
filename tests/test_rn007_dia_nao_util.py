import pytest

from motor.regras_item import pendente_por_dia_nao_util
from tests.fabrica import despesa


def test_rn007_d012_sabado_fica_pendente():
    ocorrencia = pendente_por_dia_nao_util(despesa(id="d-012", data="2026-07-18", valor="47.20"))
    assert ocorrencia.situacao == "pendente"
    assert ocorrencia.motivo == "dia_nao_util"


@pytest.mark.parametrize("data", ["2026-04-03", "2026-04-21"])
def test_rn007_feriados_ficam_pendentes(data):
    assert pendente_por_dia_nao_util(despesa(data=data)).motivo == "dia_nao_util"


@pytest.mark.parametrize("data", ["2026-02-17", "2026-07-20"])
def test_rn007_dia_util_segue_as_demais_regras(data):
    assert pendente_por_dia_nao_util(despesa(data=data)) is None


def test_rn007_hospedagem_com_entrada_no_domingo_que_cobre_segunda_segue_as_demais_regras():
    hotel = despesa(data="2026-07-19", categoria="hospedagem", descricao="Hotel - 1 diária")
    assert pendente_por_dia_nao_util(hotel) is None


def test_rn007_hospedagem_com_entrada_no_sabado_sem_dia_util_fica_pendente():
    hotel = despesa(data="2026-07-18", categoria="hospedagem", descricao="Hotel - 1 diária")
    assert pendente_por_dia_nao_util(hotel).motivo == "dia_nao_util"


def test_rn007_jantar_no_domingo_durante_a_estadia_fica_pendente():
    jantar = despesa(data="2026-07-19", categoria="alimentacao", descricao="Jantar")
    assert pendente_por_dia_nao_util(jantar).motivo == "dia_nao_util"


def test_rn007_d009_estorno_no_sabado_fica_pendente():
    estorno = despesa(id="d-009", data="2026-07-11", categoria="transporte_urbano", descricao="Estorno de corrida cancelada", valor="-45.00", nota=False)
    assert pendente_por_dia_nao_util(estorno).motivo == "dia_nao_util"


def test_rn007_estorno_de_hospedagem_no_sabado_fica_pendente():
    estorno = despesa(data="2026-07-18", categoria="hospedagem", descricao="Estorno 2 diárias", valor="-80.00")
    assert pendente_por_dia_nao_util(estorno).motivo == "dia_nao_util"
