"""Regras que decidem a situação de cada item (etapas 3 a 6 da §8 da spec)."""

import re

from motor.calendario import dia_nao_util
from motor.diarias import dias_cobertos_pela_estadia, noites_da_estadia
from motor.modelo import Ocorrencia, SituacaoItem
from motor.politica import CATEGORIAS, PALAVRAS_POR_CATEGORIA, PATAMAR_NOTA_FISCAL
from motor.texto import contem_alguma, normalizar


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


def descricao_incompativel(despesa):
    """RN-011: recusa o item cuja descrição só tem palavras de outra categoria."""
    categoria = reconhecer_categoria(despesa.categoria_informada)
    if categoria is None:
        return None
    da_categoria = contem_alguma(despesa.descricao, PALAVRAS_POR_CATEGORIA[categoria])
    de_outra = any(
        contem_alguma(despesa.descricao, lista)
        for outra, lista in PALAVRAS_POR_CATEGORIA.items()
        if outra != categoria
    )
    if de_outra and not da_categoria:
        return Ocorrencia("recusado", "descricao_incompativel", "RN-011")
    return None


def fora_do_periodo(despesa, inicio, fim):
    """RN-014: recusa o item com data fora do período; em hospedagem vale a data de entrada."""
    if not inicio <= despesa.data <= fim:
        return Ocorrencia("recusado", "fora_do_periodo", "RN-014")
    return None


def valor_zero(despesa):
    """RN-008: recusa o item de valor zero, já arredondado."""
    if despesa.valor == 0:
        return Ocorrencia("recusado", "valor_zero", "RN-008")
    return None


def eh_estadia(despesa):
    """Item de hospedagem de valor positivo; estornos não são estadias (RN-007, RN-017)."""
    return reconhecer_categoria(despesa.categoria_informada) == "hospedagem" and despesa.valor > 0


def pendente_por_dia_nao_util(despesa):
    """RN-007: item em dia não útil fica pendente; a estadia que cobre um dia útil, não.
    Estorno de hospedagem não é estadia (D-012)."""
    if not dia_nao_util(despesa.data):
        return None
    if eh_estadia(despesa) and any(
        not dia_nao_util(dia) for dia in dias_cobertos_pela_estadia(despesa)
    ):
        return None
    return Ocorrencia("pendente", "dia_nao_util", "RN-007")


def pendente_por_nota_fiscal(despesa):
    """RN-012: item de valor maior que o patamar, sem nota, fica pendente."""
    if despesa.valor > PATAMAR_NOTA_FISCAL and not despesa.tem_nota_fiscal:
        return Ocorrencia("pendente", "nota_fiscal_ausente", "RN-012")
    return None


def sobreposicoes(despesas, excluidas=frozenset()):
    """RN-017: estadias com pelo menos uma noite em comum ficam todas pendentes.
    `excluidas` são posições desconsideradas ou recusadas nas etapas 3 e 4 da §8."""
    estadias = [d for d in despesas if d.posicao not in excluidas and eh_estadia(d)]
    noites = {d.posicao: set(noites_da_estadia(d)) for d in estadias}
    sobrepostas = set()
    for i, a in enumerate(estadias):
        for b in estadias[i + 1 :]:
            if noites[a.posicao] & noites[b.posicao]:
                sobrepostas.update((a.posicao, b.posicao))
    return {
        posicao: Ocorrencia("pendente", "sobreposicao_hospedagem", "RN-017")
        for posicao in sorted(sobrepostas)
    }


def avaliar_situacoes(entrada):
    """Etapas 3 a 5 da §8 da spec: cópias, recusas e pendências, nesta ordem.
    A primeira ocorrência define a situação; as demais vão para `outros_motivos` (RN-019)."""
    despesas = entrada.despesas
    repetidos = identificadores_repetidos(despesas)
    copias = {**repetidos, **duplicatas(despesas, excluidas=set(repetidos))}

    recusas = {
        d.posicao: [
            o
            for o in (
                categoria_fora_da_politica(d),
                descricao_incompativel(d),
                fora_do_periodo(d, entrada.inicio, entrada.fim),
                valor_zero(d),
            )
            if o is not None
        ]
        for d in despesas
    }
    retiradas = set(copias) | {p for p, lista in recusas.items() if lista}
    sobrepostas = sobreposicoes(despesas, excluidas=retiradas)

    situacoes = []
    for d in despesas:
        ocorrencias = [o for o in (copias.get(d.posicao),) if o is not None]
        ocorrencias += recusas[d.posicao]
        ocorrencias += [
            o
            for o in (
                pendente_por_dia_nao_util(d),
                pendente_por_nota_fiscal(d),
                sobrepostas.get(d.posicao),
            )
            if o is not None
        ]
        principal = ocorrencias[0] if ocorrencias else None
        outros = tuple(o.motivo for o in ocorrencias[1:])
        situacoes.append(SituacaoItem(d, principal, outros))
    return situacoes


def vincular_estornos_de_hospedagem(situacoes):
    """Etapa 6 da §8 da spec (RN-016): cada estorno de hospedagem ainda sem ocorrência é
    vinculado à estadia com a mesma data de entrada. Devolve as situações atualizadas e
    {posição da estadia: estornos a abater}."""
    estadias_por_data = {}
    for s in situacoes:
        if eh_estadia(s.despesa):
            estadias_por_data.setdefault(s.despesa.data, []).append(s)

    abatimentos = {}
    atualizadas = []
    for s in situacoes:
        d = s.despesa
        estorno = (
            s.ocorrencia is None
            and d.valor < 0
            and reconhecer_categoria(d.categoria_informada) == "hospedagem"
        )
        if not estorno:
            atualizadas.append(s)
            continue
        estadias = estadias_por_data.get(d.data)
        if not estadias:
            ocorrencia = Ocorrencia("pendente", "estorno_sem_hospedagem", "RN-016")
        else:
            estadia = estadias[0]
            if estadia.ocorrencia is not None:
                ocorrencia = Ocorrencia(
                    estadia.ocorrencia.situacao, estadia.ocorrencia.motivo, "RN-016", estadia.despesa.id
                )
            else:
                ocorrencia = Ocorrencia("abatido", None, "RN-016", estadia.despesa.id)
                abatimentos.setdefault(estadia.despesa.posicao, []).append(d)
        atualizadas.append(SituacaoItem(d, ocorrencia, s.outros_motivos))
    return atualizadas, {p: tuple(e) for p, e in abatimentos.items()}
