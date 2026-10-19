"""Somas do dia, estornos e limites (RN-001 a RN-004, RN-016; etapa 8 da §8 da spec)."""

from motor.modelo import TotalDiario
from motor.politica import AMPLIACAO_VIAGEM_PERCENTUAL, LIMITES_DIARIOS
from motor.regras_item import reconhecer_categoria


def limite_do_dia(categoria, em_viagem):
    limite = LIMITES_DIARIOS[categoria]
    if em_viagem:
        limite = limite * (100 + AMPLIACAO_VIAGEM_PERCENTUAL) // 100
    return limite


def totais_diarios(situacoes, dias_viagem):
    """Um total por dia e categoria com limite diário, só com os itens sem ocorrência (RN-003).
    Estornos entram na soma antes do limite (RN-016)."""
    grupos = {}
    for situacao in situacoes:
        if situacao.ocorrencia is not None:
            continue
        despesa = situacao.despesa
        categoria = reconhecer_categoria(despesa.categoria_informada)
        if categoria in LIMITES_DIARIOS:
            grupos.setdefault((despesa.data, categoria), []).append(despesa)

    totais = []
    for (data, categoria), despesas in sorted(grupos.items()):
        total = sum(d.valor for d in despesas)
        em_viagem = data in dias_viagem
        limite = limite_do_dia(categoria, em_viagem)
        if total <= 0:
            reembolsado, situacao = 0, "sem_valor"
        elif total <= limite:
            reembolsado, situacao = total, "integral"
        else:
            reembolsado, situacao = limite, "parcial"
        totais.append(
            TotalDiario(
                data=data,
                categoria=categoria,
                itens=tuple(d.id for d in despesas),
                valor_total=total,
                em_viagem=em_viagem,
                origem_viagem=dias_viagem.get(data),
                limite=limite,
                valor_reembolsado=reembolsado,
                situacao=situacao,
            )
        )
    return totais
