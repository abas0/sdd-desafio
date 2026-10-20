"""Montagem da saída, justificativas e escrita do JSON (§4 da spec; DT-010)."""

import json
from decimal import Decimal

from motor.agregacao import calcular_hospedagem, totais_diarios
from motor.politica import PATAMAR_NOTA_FISCAL
from motor.regras_item import (
    avaliar_situacoes,
    eh_estadia,
    reconhecer_categoria,
    vincular_estornos_de_hospedagem,
)
from motor.viagem import dias_de_viagem

SITUACOES = (
    "compoe_total_do_dia",
    "abatido",
    "reembolsado",
    "reembolsado_parcialmente",
    "recusado",
    "pendente",
    "desconsiderado",
)

NOMES_CATEGORIAS = {
    "alimentacao": "alimentação",
    "transporte_urbano": "transporte urbano",
    "hospedagem": "hospedagem",
}


class Dinheiro(int):
    """Valor em centavos, escrito no JSON com exatamente duas casas decimais (DT-010)."""


def montar_resultado(entrada):
    """Aplica as etapas 3 a 8 da §8 da spec e monta a saída da §4."""
    situacoes = avaliar_situacoes(entrada)
    situacoes, abatimentos = vincular_estornos_de_hospedagem(situacoes)
    viagem = dias_de_viagem(entrada.despesas)
    totais = totais_diarios(situacoes, viagem)
    total_por_chave = {(t.data, t.categoria): t for t in totais}

    itens = []
    for situacao in situacoes:
        estornos = abatimentos.get(situacao.despesa.posicao, ())
        itens.append(_item(situacao, total_por_chave, estornos, entrada))

    totais_json = [_total(t, entrada.despesas) for t in totais]
    total_reembolsado = sum(t.valor_reembolsado for t in totais) + sum(
        i["valor_reembolsado"] for i in itens if i["situacao"].startswith("reembolsado")
    )
    quantidade = {nome: 0 for nome in SITUACOES}
    for item in itens:
        quantidade[item["situacao"]] += 1

    return {
        "colaborador": dict(entrada.colaborador),
        "periodo": dict(entrada.periodo),
        "itens": itens,
        "totais_diarios": totais_json,
        "resumo": {
            "total_reembolsado": Dinheiro(total_reembolsado),
            "quantidade_por_situacao": quantidade,
        },
    }


def _item(situacao, total_por_chave, estornos, entrada):
    d = situacao.despesa
    categoria = reconhecer_categoria(d.categoria_informada)
    ocorrencia = situacao.ocorrencia
    item = {
        "id": d.id,
        "data": d.data.isoformat(),
        "categoria_informada": d.categoria_informada,
        "categoria": categoria,
        "descricao": d.descricao,
        "fornecedor": d.fornecedor,
        "valor_informado": d.valor_informado,
        "valor_considerado": Dinheiro(d.valor),
        "tem_nota_fiscal": d.tem_nota_fiscal,
    }
    previas = _regras_previas(d, categoria)

    if ocorrencia is not None:
        item.update(
            situacao=ocorrencia.situacao,
            motivo=ocorrencia.motivo,
            outros_motivos=list(situacao.outros_motivos),
            referencia=ocorrencia.referencia,
            total_do_dia=None,
        )
        if ocorrencia.situacao == "abatido":
            item["valor_reembolsado"] = None
            item["regras"] = previas + ["RN-016"]
        else:
            item["valor_reembolsado"] = Dinheiro(0)
            item["regras"] = (["RN-005"] if ocorrencia.motivo in ("duplicata", "identificador_repetido") else []) + [ocorrencia.regra]
        item["justificativa"] = _justificativa_ocorrencia(d, ocorrencia, entrada)
        return _ordenar_item(item)

    item.update(motivo=None, outros_motivos=list(situacao.outros_motivos), referencia=None)
    if eh_estadia(d):
        calculo = calcular_hospedagem(d, estornos)
        item.update(situacao=calculo.situacao, total_do_dia=None, diarias=calculo.diarias, teto=Dinheiro(calculo.teto))
        if calculo.valor_liquido is not None:
            item["valor_liquido"] = Dinheiro(calculo.valor_liquido)
        item["valor_reembolsado"] = Dinheiro(calculo.valor_reembolsado)
        item["regras"] = previas + ["RN-004", "RN-002"] + (["RN-016"] if estornos else [])
        item["justificativa"] = _justificativa_hospedagem(d, calculo, estornos)
        return _ordenar_item(item)

    total = total_por_chave[(d.data, categoria)]
    item.update(
        situacao="compoe_total_do_dia",
        total_do_dia={"data": total.data.isoformat(), "categoria": total.categoria},
        valor_reembolsado=None,
        regras=previas + ["RN-001", "RN-003"],
        justificativa=_justificativa_compoe(d, categoria),
    )
    return _ordenar_item(item)


def _regras_previas(d, categoria):
    regras = []
    if Decimal(d.valor) / 100 != d.valor_informado:
        regras.append("RN-009")
    if categoria is not None and d.categoria_informada != categoria:
        regras.append("RN-010")
    if not d.tem_nota_fiscal and 0 < d.valor <= PATAMAR_NOTA_FISCAL:
        regras.append("RN-012")
    return regras


_ORDEM_CAMPOS = (
    "id", "data", "categoria_informada", "categoria", "descricao", "fornecedor",
    "valor_informado", "valor_considerado", "tem_nota_fiscal", "situacao", "motivo",
    "outros_motivos", "referencia", "total_do_dia", "diarias", "teto", "valor_liquido",
    "valor_reembolsado", "regras", "justificativa",
)


def _ordenar_item(item):
    """Campos na ordem da §4 da spec."""
    return {campo: item[campo] for campo in _ORDEM_CAMPOS if campo in item}


def _total(t, despesas):
    tem_estorno = any(d.id in t.itens and d.valor < 0 for d in despesas)
    regras = (["RN-013"] if t.em_viagem else []) + ["RN-001", "RN-002", "RN-003"]
    if tem_estorno:
        regras.append("RN-016")
    return {
        "data": t.data.isoformat(),
        "categoria": t.categoria,
        "itens": list(t.itens),
        "valor_total": Dinheiro(t.valor_total),
        "em_viagem": t.em_viagem,
        "limite": Dinheiro(t.limite),
        "valor_reembolsado": Dinheiro(t.valor_reembolsado),
        "situacao": t.situacao,
        "regras": regras,
        "justificativa": _justificativa_total(t),
    }


# --- justificativas (AMB-024) ----------------------------------------------


def reais(centavos):
    """Valor em reais no formato brasileiro: R$ 1.234,56."""
    sinal = "-" if centavos < 0 else ""
    inteiro, resto = divmod(abs(centavos), 100)
    return f"{sinal}R$ {inteiro:,}".replace(",", ".") + f",{resto:02d}"


def _justificativa_compoe(d, categoria):
    partes = []
    if Decimal(d.valor) / 100 != d.valor_informado:
        informado = str(d.valor_informado).replace(".", ",")
        partes.append(f"Valor de R$ {informado} arredondado para {reais(d.valor)}")
    if d.categoria_informada != categoria:
        partes.append(f'Categoria "{d.categoria_informada}" reconhecida como {NOMES_CATEGORIAS[categoria]}')
    if not d.tem_nota_fiscal and 0 < d.valor <= PATAMAR_NOTA_FISCAL:
        partes.append(f"Valor de {reais(d.valor)} não exige nota fiscal")
    compoe = f"compõe o total de {NOMES_CATEGORIAS[categoria]} de {d.data.isoformat()}"
    if not partes:
        compoe += "; o valor reembolsado é apurado no total do dia"
    partes.append(compoe)
    texto = "; ".join(partes)
    return texto[0].upper() + texto[1:] + "."


def _justificativa_hospedagem(d, calculo, estornos):
    diarias = f"{calculo.diarias} diária" + ("s" if calculo.diarias > 1 else "")
    texto = f"{diarias}, teto de {reais(calculo.teto)}; "
    if estornos:
        texto += (
            f"valor de {reais(d.valor)} menos estornos de {reais(-sum(e.valor for e in estornos))} "
            f"= {reais(calculo.valor_liquido)}"
        )
    else:
        texto += f"valor de {reais(d.valor)}"
    if calculo.situacao == "reembolsado":
        texto += " dentro do teto."
    else:
        texto += f" acima do teto; reembolsados {reais(calculo.valor_reembolsado)}."
    return texto[0].upper() + texto[1:]


def _justificativa_total(t):
    nome = NOMES_CATEGORIAS[t.categoria]
    texto = ""
    if t.em_viagem:
        texto = f"Dia de viagem ({t.origem_viagem}): limite ampliado para {reais(t.limite)}. "
    if t.situacao == "sem_valor":
        return texto + f"Total de {reais(t.valor_total)} sem valor a reembolsar; reembolsados R$ 0,00."
    relacao = "dentro do" if t.situacao == "integral" else "acima do"
    limite = "limite" if t.em_viagem else f"limite diário de {reais(t.limite)}"
    return texto + (
        f"Total de {reais(t.valor_total)} {relacao} {limite}; "
        f"reembolsados {reais(t.valor_reembolsado)}."
    )


_DIAS_DA_SEMANA = ("segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo")


def _dia_nao_util(d):
    tipo = _DIAS_DA_SEMANA[d.data.weekday()] if d.data.weekday() >= 5 else "feriado nacional"
    categoria = reconhecer_categoria(d.categoria_informada)
    nome = NOMES_CATEGORIAS.get(categoria, "despesa")
    return f"{d.data.isoformat()} é {tipo}; {nome} em dia não útil fica pendente de revisão."


def _justificativa_ocorrencia(d, o, entrada):
    motivo = o.motivo
    if o.situacao == "abatido":
        return f"Estorno de {reais(-d.valor)} abatido da hospedagem {o.referencia}."
    if o.regra == "RN-016":
        return (
            "Estorno de hospedagem sem estadia com a mesma data de entrada; pendente de revisão."
            if motivo == "estorno_sem_hospedagem"
            else f"Estorno vinculado à hospedagem {o.referencia}, que não foi reembolsada; segue a situação dela."
        )
    textos = {
        "categoria_fora_da_politica": f'Categoria "{d.categoria_informada}" fora da política (alimentação, transporte urbano, hospedagem).',
        "descricao_incompativel": f'Descrição "{d.descricao}" só tem palavras de outra categoria.',
        "fora_do_periodo": f"Data {d.data.isoformat()} fora do período de {entrada.inicio.isoformat()} a {entrada.fim.isoformat()}.",
        "valor_zero": "Valor de R$ 0,00; não há valor a reembolsar.",
        "identificador_repetido_conteudo_diferente": f"Identificador {d.id} repetido com conteúdo diferente.",
        "nota_fiscal_ausente": f"Valor de {reais(d.valor)} acima de {reais(PATAMAR_NOTA_FISCAL)} sem nota fiscal; pendente até o envio da nota.",
        "dia_nao_util": _dia_nao_util(d),
        "sobreposicao_hospedagem": "Hospedagem com noite em comum com outra; pendente de revisão.",
        "duplicata": f"Mesmo conteúdo de {o.referencia}; desconsiderado por duplicata.",
        "identificador_repetido": f"Identificador repetido, mesmo conteúdo de {o.referencia}; desconsiderado.",
    }
    return textos[motivo]


# --- escrita do JSON (DT-010) ----------------------------------------------


def escrever_json(valor, nivel=0):
    """Escreve o JSON com valores em centavos como número de duas casas e
    `valor_informado` com o texto original."""
    recuo = "  " * (nivel + 1)
    fim = "  " * nivel
    if isinstance(valor, dict):
        if not valor:
            return "{}"
        partes = [f"{recuo}{json.dumps(k, ensure_ascii=False)}: {escrever_json(v, nivel + 1)}" for k, v in valor.items()]
        return "{\n" + ",\n".join(partes) + "\n" + fim + "}"
    if isinstance(valor, list):
        if not valor:
            return "[]"
        if all(isinstance(v, str) for v in valor):
            return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in valor) + "]"
        partes = [f"{recuo}{escrever_json(v, nivel + 1)}" for v in valor]
        return "[\n" + ",\n".join(partes) + "\n" + fim + "]"
    if isinstance(valor, Dinheiro):
        sinal = "-" if valor < 0 else ""
        inteiro, resto = divmod(abs(int(valor)), 100)
        return f"{sinal}{inteiro}.{resto:02d}"
    if isinstance(valor, Decimal):
        return str(valor)
    return json.dumps(valor, ensure_ascii=False)
