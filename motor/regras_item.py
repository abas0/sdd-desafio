"""Regras que decidem a situação de cada item (etapas 3 a 6 da §8 da spec)."""

from motor.modelo import Ocorrencia
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
