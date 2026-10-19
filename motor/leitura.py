"""Leitura e validação da entrada (RN-018; etapa 1 da §8 da spec)."""

import calendar
import json
import re
from datetime import date
from decimal import Decimal

from motor.modelo import Despesa, Entrada, EntradaInvalida

_FORMATO_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_FORMATO_COMPETENCIA = re.compile(r"^(\d{4})-(\d{2})$")


def ler_entrada(texto):
    """Converte o texto JSON em `Entrada`; levanta `EntradaInvalida` se não atender à §4."""
    try:
        dados = json.loads(texto, parse_float=Decimal, parse_int=Decimal)
    except json.JSONDecodeError as erro:
        raise EntradaInvalida(f"o arquivo não é um JSON válido: {erro}") from erro
    if not isinstance(dados, dict):
        raise EntradaInvalida("o arquivo deve conter um objeto JSON")

    colaborador = _objeto(dados, "colaborador")
    colaborador = {
        campo: _texto(colaborador, campo, "colaborador")
        for campo in ("id", "nome", "centro_custo")
    }

    periodo = _objeto(dados, "periodo")
    periodo = {
        campo: _texto(periodo, campo, "periodo")
        for campo in ("competencia", "inicio", "fim")
    }
    inicio, fim = _validar_periodo(periodo)

    if "despesas" not in dados:
        raise EntradaInvalida("falta o campo 'despesas'")
    if not isinstance(dados["despesas"], list):
        raise EntradaInvalida("'despesas' deve ser uma lista")

    despesas = tuple(
        _ler_despesa(item, posicao) for posicao, item in enumerate(dados["despesas"])
    )
    return Entrada(colaborador, periodo, inicio, fim, despesas)


def _objeto(dados, campo):
    if campo not in dados:
        raise EntradaInvalida(f"falta o campo '{campo}'")
    if not isinstance(dados[campo], dict):
        raise EntradaInvalida(f"'{campo}' deve ser um objeto")
    return dados[campo]


def _texto(dados, campo, onde, nao_vazio=False):
    if campo not in dados:
        raise EntradaInvalida(f"{onde}: falta o campo '{campo}'")
    valor = dados[campo]
    if not isinstance(valor, str):
        raise EntradaInvalida(f"{onde}: '{campo}' deve ser texto")
    if nao_vazio and not valor.strip():
        raise EntradaInvalida(f"{onde}: '{campo}' não pode ser vazio")
    return valor


def _data(texto, campo, onde):
    if not _FORMATO_DATA.match(texto):
        raise EntradaInvalida(f"{onde}: '{campo}' deve estar no formato AAAA-MM-DD")
    try:
        return date.fromisoformat(texto)
    except ValueError as erro:
        raise EntradaInvalida(f"{onde}: '{campo}' não é uma data existente") from erro


def _validar_periodo(periodo):
    """O período deve ser exatamente o mês da competência (RN-014)."""
    competencia = _FORMATO_COMPETENCIA.match(periodo["competencia"])
    if not competencia or not 1 <= int(competencia.group(2)) <= 12:
        raise EntradaInvalida("periodo: 'competencia' deve estar no formato AAAA-MM")
    ano, mes = int(competencia.group(1)), int(competencia.group(2))
    inicio = _data(periodo["inicio"], "inicio", "periodo")
    fim = _data(periodo["fim"], "fim", "periodo")
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    if inicio != date(ano, mes, 1) or fim != date(ano, mes, ultimo_dia):
        raise EntradaInvalida(
            "periodo: início e fim devem ser o primeiro e o último dia do mês da competência"
        )
    return inicio, fim


def _ler_despesa(item, posicao):
    onde = f"despesa {posicao + 1}"
    if not isinstance(item, dict):
        raise EntradaInvalida(f"{onde}: deve ser um objeto")
    id_ = _texto(item, "id", onde, nao_vazio=True)
    onde = f"despesa {posicao + 1} ({id_})"
    data = _data(_texto(item, "data", onde), "data", onde)
    categoria = _texto(item, "categoria", onde)
    descricao = _texto(item, "descricao", onde, nao_vazio=True)
    fornecedor = _texto(item, "fornecedor", onde, nao_vazio=True)
    if "valor" not in item:
        raise EntradaInvalida(f"{onde}: falta o campo 'valor'")
    valor = item["valor"]
    if not isinstance(valor, Decimal) or not valor.is_finite():
        raise EntradaInvalida(f"{onde}: 'valor' deve ser um número")
    if "tem_nota_fiscal" not in item:
        raise EntradaInvalida(f"{onde}: falta o campo 'tem_nota_fiscal'")
    if not isinstance(item["tem_nota_fiscal"], bool):
        raise EntradaInvalida(f"{onde}: 'tem_nota_fiscal' deve ser verdadeiro ou falso")
    return Despesa(
        id=id_,
        data=data,
        categoria_informada=categoria,
        descricao=descricao,
        fornecedor=fornecedor,
        valor_informado=valor,
        tem_nota_fiscal=item["tem_nota_fiscal"],
        posicao=posicao,
    )
