import pytest

from motor.agregacao import calcular_hospedagem
from tests.fabrica import despesa


@pytest.mark.parametrize(
    "descricao, valor, diarias, teto, reembolsado, situacao",
    [
        ("Hotel Rio - 2 diarias", "480.00", 2, 50000, 48000, "reembolsado"),
        ("Airbnb 3 noites", "690.00", 3, 75000, 69000, "reembolsado"),
        ("Pousada - duas Diárias", "600.00", 2, 50000, 50000, "reembolsado_parcialmente"),
        ("Hotel - 2 diárias e 1 noite", "700.00", 3, 75000, 70000, "reembolsado"),
        ("Hotel - 2 diárias + meia diária", "600.00", 2, 50000, 50000, "reembolsado_parcialmente"),
        ("Hotel 3 estrelas", "300.00", 1, 25000, 25000, "reembolsado_parcialmente"),
        ("Hotel - 0 diárias", "300.00", 1, 25000, 25000, "reembolsado_parcialmente"),
        ("Hotel - meia diária", "150.00", 1, 25000, 15000, "reembolsado"),
        ("Hotel - 1 diária", "250.00", 1, 25000, 25000, "reembolsado"),
        ("Hotel - 1 diária", "250.01", 1, 25000, 25000, "reembolsado_parcialmente"),
    ],
)
def test_rn004_aceites_teto_de_hospedagem(descricao, valor, diarias, teto, reembolsado, situacao):
    calculo = calcular_hospedagem(despesa(categoria="hospedagem", descricao=descricao, valor=valor))
    assert (calculo.diarias, calculo.teto, calculo.valor_reembolsado, calculo.situacao) == (
        diarias, teto, reembolsado, situacao,
    )
    assert calculo.valor_liquido is None
