import json
from decimal import Decimal

import pytest

from motor.arredondamento import para_centavos
from motor.leitura import ler_entrada


@pytest.mark.parametrize(
    "valor, centavos",
    [
        ("33.333", 3333),
        ("33.335", 3334),
        ("33.334", 3333),
        ("-45.005", -4501),
        ("60.004", 6000),
        ("0.004", 0),
        ("100.004", 10000),
        ("72.50", 7250),
        ("100", 10000),
    ],
)
def test_rn009_arredonda_para_duas_casas_com_metade_afastando_do_zero(valor, centavos):
    assert para_centavos(Decimal(valor)) == centavos


def test_rn009_valor_lido_do_json_nao_passa_por_ponto_flutuante():
    texto = json.dumps(
        {
            "colaborador": {"id": "c", "nome": "n", "centro_custo": "cc"},
            "periodo": {"competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31"},
            "despesas": [],
        }
    )
    texto = texto.replace(
        '"despesas": []',
        '"despesas": [{"id": "d-1", "data": "2026-07-03", "categoria": "alimentacao",'
        ' "descricao": "Almoco", "fornecedor": "R", "valor": 33.335, "tem_nota_fiscal": true}]',
    )
    despesa = ler_entrada(texto).despesas[0]
    assert despesa.valor_informado == Decimal("33.335")
    assert despesa.valor == 3334
