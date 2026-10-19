"""Dias de viagem (RN-013; etapa 7 da §8 da spec)."""

from motor.diarias import dias_cobertos_pela_estadia
from motor.politica import PALAVRAS_VIAGEM
from motor.regras_item import eh_estadia
from motor.texto import formas_singular_e_plural, palavras


def dias_de_viagem(despesas):
    """{data: origem} dos dias de viagem, com todos os itens da entrada, reembolsados ou não.
    A origem descreve o primeiro item que marcou o dia, para a justificativa."""
    dias = {}
    for despesa in despesas:
        if eh_estadia(despesa):
            for dia in dias_cobertos_pela_estadia(despesa):
                dias.setdefault(dia, f"estadia de {despesa.id}")
        palavra = _palavra_de_viagem(despesa.descricao)
        if palavra:
            dias.setdefault(despesa.data, f'"{palavra}" em {despesa.id}')
    return dias


def _palavra_de_viagem(descricao):
    encontradas = palavras(descricao)
    for palavra in PALAVRAS_VIAGEM:
        comum = encontradas & formas_singular_e_plural(palavra)
        if comum:
            return min(comum)
    return None
