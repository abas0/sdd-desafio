"""Arredondamento dos valores da entrada em centavos (RN-009; DT-003)."""

from decimal import ROUND_HALF_UP, Decimal


def para_centavos(valor):
    """Arredonda para duas casas, com a metade afastando do zero, e devolve centavos inteiros."""
    return int((valor * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
