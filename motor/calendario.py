"""Dias não úteis: fins de semana, feriados nacionais fixos e Sexta-feira Santa (RN-007)."""

from datetime import date, timedelta

from motor.politica import DIAS_SEXTA_SANTA_ANTES_DA_PASCOA, FERIADOS_FIXOS

SABADO = 5


def pascoa(ano):
    """Domingo de Páscoa no calendário gregoriano (algoritmo de Meeus/Jones/Butcher)."""
    a = ano % 19
    b, c = divmod(ano, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes, dia = divmod(h + l - 7 * m + 114, 31)
    return date(ano, mes, dia + 1)


def sexta_feira_santa(ano):
    return pascoa(ano) - timedelta(days=DIAS_SEXTA_SANTA_ANTES_DA_PASCOA)


def dia_nao_util(data):
    return (
        data.weekday() >= SABADO
        or (data.month, data.day) in FERIADOS_FIXOS
        or data == sexta_feira_santa(data.year)
    )
