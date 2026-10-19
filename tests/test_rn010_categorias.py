import pytest

from motor.regras_item import categoria_fora_da_politica, reconhecer_categoria
from tests.fabrica import despesa


@pytest.mark.parametrize(
    "informada, reconhecida",
    [
        ("alimentacao", "alimentacao"),
        ("ALIMENTACAO", "alimentacao"),
        ("Alimentação", "alimentacao"),
        (" alimentacao ", "alimentacao"),
        ("transporte_urbano", "transporte_urbano"),
        ("Transporte Urbano", "transporte_urbano"),
        ("transporte-urbano", "transporte_urbano"),
        ("transporte   urbano", "transporte_urbano"),
        ("Hospedagem", "hospedagem"),
    ],
)
def test_rn010_reconhece_categorias_da_politica_com_grafias_diferentes(informada, reconhecida):
    assert reconhecer_categoria(informada) == reconhecida


@pytest.mark.parametrize("informada", ["coworking", "transporte", "", "alimentacao extra"])
def test_rn010_categoria_fora_da_politica_nao_e_reconhecida(informada):
    assert reconhecer_categoria(informada) is None


def test_rn010_d005_coworking_e_recusado():
    ocorrencia = categoria_fora_da_politica(despesa(categoria="coworking"))
    assert ocorrencia.situacao == "recusado"
    assert ocorrencia.motivo == "categoria_fora_da_politica"


def test_rn010_d014_alimentacao_em_maiusculas_nao_e_recusado():
    assert categoria_fora_da_politica(despesa(categoria="ALIMENTACAO")) is None
