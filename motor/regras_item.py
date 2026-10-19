"""Regras que decidem a situação de cada item (etapas 3 a 6 da §8 da spec)."""

import re

from motor.modelo import Ocorrencia
from motor.politica import CATEGORIAS
from motor.texto import normalizar


def mesmo_conteudo(a, b):
    """RN-005: todos os campos coincidem, exceto o identificador."""
    return (
        a.data == b.data
        and normalizar(a.categoria_informada) == normalizar(b.categoria_informada)
        and normalizar(a.descricao) == normalizar(b.descricao)
        and normalizar(a.fornecedor) == normalizar(b.fornecedor)
        and a.valor == b.valor
        and a.tem_nota_fiscal == b.tem_nota_fiscal
    )


def identificadores_repetidos(despesas):
    """RN-006: devolve {posição: Ocorrencia} para os itens com identificador repetido."""
    grupos = {}
    for despesa in despesas:
        grupos.setdefault(despesa.id, []).append(despesa)
    ocorrencias = {}
    for grupo in grupos.values():
        if len(grupo) < 2:
            continue
        primeiro = grupo[0]
        if all(mesmo_conteudo(primeiro, outro) for outro in grupo[1:]):
            for outro in grupo[1:]:
                ocorrencias[outro.posicao] = Ocorrencia(
                    "desconsiderado", "identificador_repetido", "RN-006", primeiro.id
                )
        else:
            for despesa in grupo:
                ocorrencias[despesa.posicao] = Ocorrencia(
                    "recusado", "identificador_repetido_conteudo_diferente", "RN-006"
                )
    return ocorrencias


def duplicatas(despesas, excluidas=frozenset()):
    """RN-015: entre itens de identificadores diferentes, o primeiro de cada conteúdo é calculado
    e os demais são desconsiderados. `excluidas` são posições já retiradas pela RN-006."""
    originais = []
    ocorrencias = {}
    for despesa in despesas:
        if despesa.posicao in excluidas:
            continue
        original = next((o for o in originais if mesmo_conteudo(o, despesa)), None)
        if original is None:
            originais.append(despesa)
        else:
            ocorrencias[despesa.posicao] = Ocorrencia(
                "desconsiderado", "duplicata", "RN-015", original.id
            )
    return ocorrencias


def _forma_da_categoria(texto):
    return re.sub(r"\s+", " ", re.sub(r"[_-]", " ", normalizar(texto))).strip()


_CATEGORIAS_POR_FORMA = {_forma_da_categoria(c): c for c in CATEGORIAS}


def reconhecer_categoria(texto):
    """RN-010: categoria da política correspondente ao texto informado, ou None."""
    return _CATEGORIAS_POR_FORMA.get(_forma_da_categoria(texto))


def categoria_fora_da_politica(despesa):
    """RN-010: recusa o item cuja categoria não é da política."""
    if reconhecer_categoria(despesa.categoria_informada) is None:
        return Ocorrencia("recusado", "categoria_fora_da_politica", "RN-010")
    return None
