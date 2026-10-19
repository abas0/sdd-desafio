"""Normalização de texto usada nas comparações da spec (RN-004, RN-005, RN-010, RN-011, RN-013)."""

import re
import unicodedata


def normalizar(texto):
    """Minúsculas, sem acentos, sem espaços no início e no fim nem repetidos entre palavras."""
    sem_acentos = "".join(
        c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c)
    )
    return re.sub(r"\s+", " ", sem_acentos.lower()).strip()


def palavras(texto):
    """Palavras do texto normalizado."""
    return set(re.findall(r"[a-z0-9]+", normalizar(texto)))


def formas_singular_e_plural(palavra):
    """A palavra normalizada e seus plurais regulares em português."""
    p = normalizar(palavra)
    formas = {p, p + "s"}
    if p.endswith("l"):
        formas.add(p[:-1] + "is")
    if p.endswith(("r", "z", "s")):
        formas.add(p + "es")
    if p.endswith("ao"):
        formas.add(p[:-2] + "oes")
    return formas


def contem_alguma(texto, lista):
    """Se o texto contém, como palavra inteira no singular ou no plural, alguma palavra da lista."""
    encontradas = palavras(texto)
    return any(encontradas & formas_singular_e_plural(p) for p in lista)
