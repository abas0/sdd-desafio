import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

from tests.test_saida import saida_da_spec, sem_justificativas

RAIZ = Path(__file__).resolve().parent.parent
EXEMPLO = RAIZ / "exemplos" / "despesas-exemplo.json"


def calcular(entrada, saida):
    return subprocess.run(
        [sys.executable, "reembolso.py", "calcular", "--input", str(entrada), "--output", str(saida)],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_spec9_exemplo_gera_a_saida_da_spec(tmp_path):
    saida = tmp_path / "saida.json"
    resultado = calcular(EXEMPLO, saida)
    assert resultado.returncode == 0, resultado.stderr
    gerada = json.loads(saida.read_text(encoding="utf-8"), parse_float=Decimal)
    assert sem_justificativas(gerada) == sem_justificativas(saida_da_spec())


def test_spec9_mesma_entrada_gera_sempre_a_mesma_saida(tmp_path):
    primeira, segunda = tmp_path / "a.json", tmp_path / "b.json"
    calcular(EXEMPLO, primeira)
    calcular(EXEMPLO, segunda)
    assert primeira.read_bytes() == segunda.read_bytes()


def test_spec9_valores_com_duas_casas_no_arquivo(tmp_path):
    saida = tmp_path / "saida.json"
    calcular(EXEMPLO, saida)
    texto = saida.read_text(encoding="utf-8")
    assert '"total_reembolsado": 788.23' in texto
    assert '"limite": 60.00' in texto
    assert '"valor_informado": 33.333' in texto


def test_rn018_entrada_invalida_nao_grava_saida_e_indica_erro(tmp_path):
    entrada = tmp_path / "entrada.json"
    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    dados["despesas"][0]["valor"] = "abc"
    entrada.write_text(json.dumps(dados), encoding="utf-8")
    saida = tmp_path / "saida.json"
    resultado = calcular(entrada, saida)
    assert resultado.returncode != 0
    assert "valor" in resultado.stderr
    assert not saida.exists()


def test_rn018_arquivo_inexistente_indica_erro(tmp_path):
    saida = tmp_path / "saida.json"
    resultado = calcular(tmp_path / "nao-existe.json", saida)
    assert resultado.returncode != 0
    assert not saida.exists()


def test_rn018_lista_vazia_gera_saida_sem_itens(tmp_path):
    entrada = tmp_path / "entrada.json"
    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    dados["despesas"] = []
    entrada.write_text(json.dumps(dados), encoding="utf-8")
    saida = tmp_path / "saida.json"
    assert calcular(entrada, saida).returncode == 0
    gerada = json.loads(saida.read_text(encoding="utf-8"))
    assert gerada["itens"] == []
    assert gerada["totais_diarios"] == []
    assert gerada["resumo"]["total_reembolsado"] == 0
