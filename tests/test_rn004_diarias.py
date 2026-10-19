import pytest

from motor.diarias import numero_de_diarias


@pytest.mark.parametrize(
    "descricao, diarias",
    [
        # aceites da RN-004
        ("Hotel Rio - 2 diarias", 2),
        ("Airbnb 3 noites", 3),
        ("Pousada - duas Diárias", 2),
        ("Hotel - 2 diárias e 1 noite", 3),
        ("Hotel - 2 diárias + meia diária", 2),
        ("Hotel 3 estrelas", 1),
        ("Hotel - 0 diárias", 1),
        ("Hotel - meia diária", 1),
    ],
)
def test_rn004_aceites_numero_de_diarias(descricao, diarias):
    assert numero_de_diarias(descricao) == diarias


@pytest.mark.parametrize(
    "descricao, diarias",
    [
        ("Hotel - 1 diária(s)", 1),
        ("Hotel - 4 diária(s)", 4),
        ("HOTEL 5 NOITES", 5),
        ("Pousada uma noite", 1),
        ("Hotel vinte e uma diárias", 21),
        ("Hotel cento e vinte noites", 120),
        ("Hotel - 30 diarias", 30),
        ("Hotel -2 diárias", 1),
        ("Hotel 2,5 diárias", 1),
        ("Hotel - diárias: 2", 1),
        ("Pernoite no hotel", 1),
    ],
)
def test_rn004_formas_do_numero_de_diarias(descricao, diarias):
    assert numero_de_diarias(descricao) == diarias
