from datetime import date

import pytest

from motor.regras_item import fora_do_periodo
from tests.fabrica import despesa

INICIO, FIM = date(2026, 7, 1), date(2026, 7, 31)


def test_rn014_d008_de_abril_e_recusado():
    ocorrencia = fora_do_periodo(despesa(id="d-008", data="2026-04-15"), INICIO, FIM)
    assert ocorrencia.situacao == "recusado"
    assert ocorrencia.motivo == "fora_do_periodo"


@pytest.mark.parametrize("data", ["2026-07-01", "2026-07-31"])
def test_rn014_primeiro_e_ultimo_dia_estao_dentro_do_periodo(data):
    assert fora_do_periodo(despesa(data=data), INICIO, FIM) is None


def test_rn014_hospedagem_com_diarias_apos_o_fim_nao_e_cortada():
    hospedagem = despesa(data="2026-07-30", categoria="hospedagem", descricao="Hotel - 3 diárias", valor="600.00")
    assert fora_do_periodo(hospedagem, INICIO, FIM) is None


def test_rn014_hospedagem_com_entrada_no_mes_seguinte_e_recusada():
    hospedagem = despesa(data="2026-08-10", categoria="hospedagem", descricao="Hotel - 2 diárias")
    assert fora_do_periodo(hospedagem, INICIO, FIM).motivo == "fora_do_periodo"
