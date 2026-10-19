"""Número de diárias lido na descrição da hospedagem (RN-004; AMB-003)."""

import re
from datetime import timedelta

from motor.texto import normalizar

_PALAVRA_DIARIA = re.compile(r"(?<![a-z])(?:diaria|noite)(?:s|\(s\))?(?![a-z])")
_TOKEN = re.compile(r"-?\d+(?:[.,]\d+)?|[a-z]+")

_NUMEROS_POR_EXTENSO = {
    "zero": 0, "um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4,
    "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11,
    "doze": 12, "treze": 13, "catorze": 14, "quatorze": 14, "quinze": 15,
    "dezesseis": 16, "dezessete": 17, "dezoito": 18, "dezenove": 19, "vinte": 20,
    "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta": 70,
    "oitenta": 80, "noventa": 90, "cem": 100, "cento": 100, "duzentos": 200,
    "duzentas": 200, "trezentos": 300, "trezentas": 300, "quatrocentos": 400,
    "quatrocentas": 400, "quinhentos": 500, "quinhentas": 500, "seiscentos": 600,
    "seiscentas": 600, "setecentos": 700, "setecentas": 700, "oitocentos": 800,
    "oitocentas": 800, "novecentos": 900, "novecentas": 900,
}


def numero_de_diarias(descricao):
    """Soma dos números válidos (inteiros >= 1) imediatamente antes de "diária" ou "noite"; sem nenhum, 1."""
    texto = normalizar(descricao)
    total = 0
    for ocorrencia in _PALAVRA_DIARIA.finditer(texto):
        numero = _numero_no_fim(_TOKEN.findall(texto[: ocorrencia.start()]))
        if numero is not None and numero >= 1:
            total += numero
    return total if total else 1


def noites_da_estadia(despesa):
    """Noites da estadia: a data de entrada e os dias seguintes, uma por diária (RN-017)."""
    n = numero_de_diarias(despesa.descricao)
    return [despesa.data + timedelta(days=k) for k in range(n)]


def dias_cobertos_pela_estadia(despesa):
    """Dias cobertos: as noites e o dia de saída, "diárias + 1" dias (RN-013)."""
    n = numero_de_diarias(despesa.descricao)
    return [despesa.data + timedelta(days=k) for k in range(n + 1)]


def _numero_no_fim(tokens):
    if not tokens:
        return None
    ultimo = tokens[-1]
    if ultimo[0].isdigit() or ultimo[0] == "-":
        return int(ultimo) if ultimo.isdigit() else None
    return _extenso_no_fim(tokens)


def _extenso_no_fim(tokens):
    palavras = []
    for token in reversed(tokens):
        if token in _NUMEROS_POR_EXTENSO or token in ("mil", "e"):
            palavras.insert(0, token)
        else:
            break
    while palavras and palavras[0] == "e":
        palavras.pop(0)
    if not palavras or palavras[-1] == "e":
        return None
    total = atual = 0
    for palavra in palavras:
        if palavra == "e":
            continue
        if palavra == "mil":
            total += (atual or 1) * 1000
            atual = 0
        else:
            atual += _NUMEROS_POR_EXTENSO[palavra]
    return total + atual
