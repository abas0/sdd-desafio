"""Normalização de texto usada nas comparações da spec (RN-004, RN-005, RN-010, RN-011, RN-013)."""

import re
import unicodedata


def normalizar(texto):
    """Minúsculas, sem acentos, sem espaços no início e no fim nem repetidos entre palavras."""
    sem_acentos = "".join(
        c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c)
    )
    return re.sub(r"\s+", " ", sem_acentos.lower()).strip()
