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

# Categorias da política (RN-010).
CATEGORIAS = ("alimentacao", "transporte_urbano", "hospedagem")

# Palavras associadas a cada categoria, na descrição (RN-011).
PALAVRAS_POR_CATEGORIA = {
    "alimentacao": ("almoço", "jantar", "café", "lanche", "refeição", "restaurante", "padaria"),
    "transporte_urbano": ("corrida", "táxi", "uber", "ônibus", "metrô"),
    "hospedagem": ("hotel", "pousada", "hostel", "airbnb", "diária", "noite"),
}

# Nota fiscal obrigatória para valor maior que este, em centavos (RN-012).
PATAMAR_NOTA_FISCAL = 10000

# Palavras que marcam o dia como de viagem, na descrição de qualquer item (RN-013).
PALAVRAS_VIAGEM = ("aeroporto", "rodoviária", "viagem", "voo", "embarque")

# Limites diários por categoria, em centavos (RN-001, RN-002).
LIMITES_DIARIOS = {"alimentacao": 6000, "transporte_urbano": 8000}

# Ampliação dos limites diários em dia de viagem, em porcentagem (RN-013).
AMPLIACAO_VIAGEM_PERCENTUAL = 50
