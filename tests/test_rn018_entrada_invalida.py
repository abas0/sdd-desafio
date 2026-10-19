import json
from decimal import Decimal
from pathlib import Path

import pytest

from motor.leitura import ler_entrada
from motor.modelo import EntradaInvalida

EXEMPLO = Path(__file__).resolve().parent.parent / "exemplos" / "despesas-exemplo.json"


def entrada(**despesa):
    item = {
        "id": "d-001",
        "data": "2026-07-03",
        "categoria": "alimentacao",
        "descricao": "Almoco",
        "fornecedor": "Restaurante",
        "valor": 30.00,
        "tem_nota_fiscal": True,
    }
    item.update(despesa)
    item = {k: v for k, v in item.items() if v is not ...}
    return {
        "colaborador": {"id": "c-1", "nome": "Fulano", "centro_custo": "CC-1"},
        "periodo": {"competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31"},
        "despesas": [item],
    }


def ler(dados):
    return ler_entrada(json.dumps(dados))


def test_rn018_exemplo_e_valido():
    lida = ler_entrada(EXEMPLO.read_text(encoding="utf-8"))
    assert len(lida.despesas) == 14
    assert lida.despesas[10].valor_informado == Decimal("33.333")


def test_rn018_arquivo_que_nao_e_json_e_invalido():
    with pytest.raises(EntradaInvalida):
        ler_entrada("isto não é json")


def test_rn018_falta_colaborador_e_invalido():
    dados = entrada()
    del dados["colaborador"]
    with pytest.raises(EntradaInvalida):
        ler(dados)


def test_rn018_falta_despesas_e_invalido():
    dados = entrada()
    del dados["despesas"]
    with pytest.raises(EntradaInvalida):
        ler(dados)


def test_rn018_valor_nao_numerico_e_invalido():
    with pytest.raises(EntradaInvalida):
        ler(entrada(valor="abc"))


def test_rn018_data_inexistente_e_invalida():
    with pytest.raises(EntradaInvalida):
        ler(entrada(data="2026-02-30"))


def test_rn018_data_fora_do_formato_e_invalida():
    with pytest.raises(EntradaInvalida):
        ler(entrada(data="03/07/2026"))


def test_rn018_item_sem_fornecedor_e_invalido():
    with pytest.raises(EntradaInvalida):
        ler(entrada(fornecedor=...))


def test_rn018_item_sem_id_e_invalido():
    with pytest.raises(EntradaInvalida):
        ler(entrada(id=...))


def test_rn018_descricao_vazia_e_invalida():
    with pytest.raises(EntradaInvalida):
        ler(entrada(descricao="  "))


def test_rn018_nota_que_nao_e_booleano_e_invalida():
    with pytest.raises(EntradaInvalida):
        ler(entrada(tem_nota_fiscal="sim"))


def test_rn018_campo_a_mais_e_ignorado():
    lida = ler(entrada(moeda="BRL"))
    assert len(lida.despesas) == 1


def test_rn018_lista_vazia_e_valida():
    dados = entrada()
    dados["despesas"] = []
    assert ler(dados).despesas == ()


@pytest.mark.parametrize("fim", ["2026-07-15", "2026-08-05"])
def test_rn018_periodo_diferente_do_mes_da_competencia_e_invalido(fim):
    dados = entrada()
    dados["periodo"]["fim"] = fim
    with pytest.raises(EntradaInvalida):
        ler(dados)
