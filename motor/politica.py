"""Valores da política de reembolso (DT-007). Nenhum valor da política aparece fora deste arquivo."""

# Feriados nacionais de data fixa, como (mês, dia) (RN-007).
FERIADOS_FIXOS = frozenset(
    {
        (1, 1),
        (4, 21),
        (5, 1),
        (9, 7),
        (10, 12),
        (11, 2),
        (11, 15),
        (11, 20),
        (12, 25),
    }
)

# Sexta-feira Santa: dias antes do Domingo de Páscoa (RN-007).
DIAS_SEXTA_SANTA_ANTES_DA_PASCOA = 2
