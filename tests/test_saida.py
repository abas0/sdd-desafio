import json
import re
from decimal import Decimal
from pathlib import Path

from motor.leitura import ler_entrada
from motor.saida import Dinheiro, escrever_json, montar_resultado, reais

RAIZ = Path(__file__).resolve().parent.parent
EXEMPLO = RAIZ / "exemplos" / "despesas-exemplo.json"
SPEC = RAIZ / "specs" / "001-motor-reembolso" / "spec.md"


def saida_da_spec():
    texto = SPEC.read_text(encoding="utf-8")
    bloco = re.search(r"\*\*Exemplo:\*\* saída.*?```json\n(.*?)```", texto, re.S).group(1)
    return json.loads(bloco, parse_float=Decimal)


def sem_justificativas(valor):
    if isinstance(valor, dict):
        return {k: sem_justificativas(v) for k, v in valor.items() if k != "justificativa"}
    if isinstance(valor, list):
        return [sem_justificativas(v) for v in valor]
    return valor


def saida_do_exemplo():
    resultado = montar_resultado(ler_entrada(EXEMPLO.read_text(encoding="utf-8")))
    return json.loads(escrever_json(resultado), parse_float=Decimal)


def test_saida_do_exemplo_igual_a_da_spec_exceto_justificativas():
    assert sem_justificativas(saida_do_exemplo()) == sem_justificativas(saida_da_spec())


def test_saida_campos_dos_itens_na_ordem_da_spec():
    assert [list(i) for i in saida_do_exemplo()["itens"]] == [list(i) for i in saida_da_spec()["itens"]]


def test_saida_toda_despesa_tem_justificativa():
    saida = saida_do_exemplo()
    assert all(i["justificativa"] for i in saida["itens"])
    assert all(t["justificativa"] for t in saida["totais_diarios"])


def test_saida_resumo_do_exemplo():
    resumo = saida_do_exemplo()["resumo"]
    assert resumo["total_reembolsado"] == Decimal("788.23")
    assert list(resumo["quantidade_por_situacao"]) == [
        "compoe_total_do_dia", "abatido", "reembolsado", "reembolsado_parcialmente",
        "recusado", "pendente", "desconsiderado",
    ]


def test_saida_dt010_valores_com_duas_casas_e_valor_informado_original():
    texto = escrever_json({"a": Dinheiro(6000), "b": Dinheiro(-4500), "c": Dinheiro(5), "d": Decimal("33.333")})
    assert '"a": 60.00' in texto
    assert '"b": -45.00' in texto
    assert '"c": 0.05' in texto
    assert '"d": 33.333' in texto


def test_saida_justificativa_cita_valores_e_limite():
    totais = {t["data"]: t for t in saida_do_exemplo()["totais_diarios"]}
    assert totais["2026-07-03"]["justificativa"] == (
        "Total de R$ 110,50 acima do limite diário de R$ 60,00; reembolsados R$ 60,00."
    )


def test_saida_reais_no_formato_brasileiro():
    assert reais(123456) == "R$ 1.234,56"
    assert reais(-4500) == "-R$ 45,00"
