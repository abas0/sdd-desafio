import json
from pathlib import Path

import pytest

from motor.leitura import ler_entrada
from motor.regras_item import descricao_incompativel, reconhecer_categoria
from tests.fabrica import despesa

EXEMPLO = Path(__file__).resolve().parent.parent / "exemplos" / "despesas-exemplo.json"


@pytest.mark.parametrize(
    "categoria, descricao",
    [
        ("alimentacao", "Cafe da manha hotel"),
        ("transporte_urbano", "Corrida hotel"),
        ("alimentacao", "Despesa diversa"),
        ("hospedagem", "Jantar no hotel"),
        ("hospedagem", "Hotéis - 2 diárias"),
        ("alimentacao", "Refeições da equipe"),
        ("alimentacao", "Jantares com cliente no hotel"),
    ],
)
def test_rn011_descricao_aceita(categoria, descricao):
    assert descricao_incompativel(despesa(categoria=categoria, descricao=descricao)) is None


@pytest.mark.parametrize(
    "categoria, descricao",
    [
        ("alimentacao", "Hotel Copa Sul"),
        ("hospedagem", "Almoço com cliente"),
        ("transporte_urbano", "Jantar"),
        ("alimentacao", "Uber até o cliente"),
    ],
)
def test_rn011_descricao_so_com_palavra_de_outra_categoria_e_recusada(categoria, descricao):
    ocorrencia = descricao_incompativel(despesa(categoria=categoria, descricao=descricao))
    assert ocorrencia.situacao == "recusado"
    assert ocorrencia.motivo == "descricao_incompativel"


def test_rn011_palavra_dentro_de_outra_nao_conta():
    # "noite" dentro de "pernoite" não é a palavra "noite"
    assert descricao_incompativel(despesa(categoria="alimentacao", descricao="Pernoite")) is None


def test_rn011_itens_do_exemplo_com_categoria_da_politica_sao_aceitos():
    entrada = ler_entrada(EXEMPLO.read_text(encoding="utf-8"))
    da_politica = [d for d in entrada.despesas if reconhecer_categoria(d.categoria_informada)]
    assert len(da_politica) == 13
    assert all(descricao_incompativel(d) is None for d in da_politica)
