import itertools

import pytest

from motor.regras_item import identificadores_repetidos
from tests.fabrica import despesa, em_ordem

ALMOCO = despesa(id="d-020", data="2026-07-06", categoria="alimentacao", descricao="Almoço", valor="30.00")
CORRIDA = despesa(id="d-020", data="2026-07-13", categoria="transporte_urbano", descricao="Corrida", valor="45.00")


def test_rn006_mesmo_conteudo_calcula_o_primeiro_e_desconsidera_os_demais():
    despesas = em_ordem(ALMOCO, ALMOCO)
    ocorrencias = identificadores_repetidos(despesas)
    assert 0 not in ocorrencias
    assert ocorrencias[1].situacao == "desconsiderado"
    assert ocorrencias[1].motivo == "identificador_repetido"
    assert ocorrencias[1].referencia == "d-020"


def test_rn006_conteudo_diferente_recusa_todos():
    ocorrencias = identificadores_repetidos(em_ordem(ALMOCO, CORRIDA))
    assert {p: o.motivo for p, o in ocorrencias.items()} == {
        0: "identificador_repetido_conteudo_diferente",
        1: "identificador_repetido_conteudo_diferente",
    }
    assert all(o.situacao == "recusado" for o in ocorrencias.values())


@pytest.mark.parametrize("ordem", list(itertools.permutations([ALMOCO, ALMOCO, CORRIDA])))
def test_rn006_tres_itens_com_um_diferente_recusa_os_tres_em_qualquer_ordem(ordem):
    ocorrencias = identificadores_repetidos(em_ordem(*ordem))
    assert len(ocorrencias) == 3
    assert all(o.situacao == "recusado" for o in ocorrencias.values())


def test_rn006_identificadores_unicos_nao_geram_ocorrencia():
    assert identificadores_repetidos(em_ordem(despesa(id="d-1"), despesa(id="d-2"))) == {}
