from datetime import date

import pytest

from motor.calendario import dia_nao_util, pascoa, sexta_feira_santa


@pytest.mark.parametrize(
    "ano, esperado",
    [(2024, date(2024, 3, 31)), (2025, date(2025, 4, 20)), (2026, date(2026, 4, 5))],
)
def test_rn007_pascoa(ano, esperado):
    assert pascoa(ano) == esperado


def test_rn007_sexta_feira_santa_de_2026():
    assert sexta_feira_santa(2026) == date(2026, 4, 3)


@pytest.mark.parametrize(
    "data",
    [
        date(2026, 7, 18),  # sábado
        date(2026, 7, 19),  # domingo
        date(2026, 4, 3),  # Sexta-feira Santa
        date(2026, 4, 21),  # Tiradentes, terça-feira
        date(2026, 11, 20),  # Consciência Negra, sexta-feira
        date(2026, 12, 25),  # Natal, sexta-feira
    ],
)
def test_rn007_dias_nao_uteis(data):
    assert dia_nao_util(data)


@pytest.mark.parametrize(
    "data",
    [
        date(2026, 2, 17),  # terça-feira de Carnaval: ponto facultativo
        date(2026, 6, 4),  # Corpus Christi: ponto facultativo
        date(2026, 7, 20),  # segunda-feira
        date(2026, 7, 31),  # sexta-feira
    ],
)
def test_rn007_dias_uteis(data):
    assert not dia_nao_util(data)
