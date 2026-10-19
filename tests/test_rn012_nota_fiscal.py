import pytest

from motor.regras_item import pendente_por_nota_fiscal
from tests.fabrica import despesa


def test_rn012_d003_cem_reais_sem_nota_nao_exige_nota():
    assert pendente_por_nota_fiscal(despesa(id="d-003", valor="100.00", nota=False)) is None


def test_rn012_d004_cem_reais_e_um_centavo_sem_nota_fica_pendente():
    ocorrencia = pendente_por_nota_fiscal(despesa(id="d-004", valor="100.01", nota=False))
    assert ocorrencia.situacao == "pendente"
    assert ocorrencia.motivo == "nota_fiscal_ausente"


def test_rn012_d013_hospedagem_sem_nota_fica_pendente():
    airbnb = despesa(id="d-013", categoria="hospedagem", descricao="Airbnb 3 noites", valor="690.00", nota=False)
    assert pendente_por_nota_fiscal(airbnb).motivo == "nota_fiscal_ausente"


def test_rn012_d010_hospedagem_com_nota_nao_fica_pendente():
    hotel = despesa(id="d-010", categoria="hospedagem", descricao="Hotel Rio - 2 diarias", valor="480.00", nota=True)
    assert pendente_por_nota_fiscal(hotel) is None


@pytest.mark.parametrize("valor", ["100.004", "-150.00"])
def test_rn012_valor_arredondado_ate_cem_ou_negativo_nao_exige_nota(valor):
    assert pendente_por_nota_fiscal(despesa(valor=valor, nota=False)) is None
