import pytest

from motor.regras_item import valor_zero
from tests.fabrica import despesa


@pytest.mark.parametrize("valor", ["0", "0.00", "0.004", "-0.004"])
def test_rn008_valor_zero_depois_do_arredondamento_e_recusado(valor):
    ocorrencia = valor_zero(despesa(valor=valor))
    assert ocorrencia.situacao == "recusado"
    assert ocorrencia.motivo == "valor_zero"


@pytest.mark.parametrize("valor", ["0.005", "30.00", "-45.00"])
def test_rn008_valor_diferente_de_zero_nao_e_recusado(valor):
    assert valor_zero(despesa(valor=valor)) is None
