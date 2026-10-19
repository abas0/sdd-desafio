from datetime import date
from pathlib import Path

from motor.leitura import ler_entrada
from motor.modelo import Entrada
from motor.regras_item import avaliar_situacoes
from tests.fabrica import despesa, em_ordem

EXEMPLO = Path(__file__).resolve().parent.parent / "exemplos" / "despesas-exemplo.json"


def avaliar(*despesas):
    entrada = Entrada({}, {}, date(2026, 7, 1), date(2026, 7, 31), em_ordem(*despesas))
    return avaliar_situacoes(entrada)


def resumo(situacao):
    o = situacao.ocorrencia
    return (o.situacao, o.motivo, situacao.outros_motivos) if o else (None, None, ())


def test_rn019_sabado_fora_do_periodo_e_recusado_com_dia_nao_util_em_outros_motivos():
    [s] = avaliar(despesa(data="2026-04-18"))
    assert resumo(s) == ("recusado", "fora_do_periodo", ("dia_nao_util",))


def test_rn019_duas_iguais_fora_do_periodo():
    primeira, segunda = avaliar(despesa(id="d-1", data="2026-04-15"), despesa(id="d-2", data="2026-04-15"))
    assert resumo(primeira) == ("recusado", "fora_do_periodo", ())
    assert resumo(segunda) == ("desconsiderado", "duplicata", ("fora_do_periodo",))
    assert segunda.ocorrencia.referencia == "d-1"


def test_rn019_hospedagens_identicas_nao_se_sobrepoem():
    hotel = dict(data="2026-07-14", categoria="hospedagem", descricao="Hotel - 2 diárias", valor="400.00")
    primeira, segunda = avaliar(despesa(id="A", **hotel), despesa(id="B", **hotel))
    assert primeira.ocorrencia is None
    assert resumo(segunda) == ("desconsiderado", "duplicata", ())


def test_rn019_recusa_vem_antes_da_pendencia_de_nota():
    [s] = avaliar(despesa(categoria="coworking", descricao="Sala", valor="150.00", nota=False))
    assert resumo(s) == ("recusado", "categoria_fora_da_politica", ("nota_fiscal_ausente",))


def test_rn019_dia_nao_util_vem_antes_da_nota_fiscal():
    [s] = avaliar(despesa(data="2026-07-19", categoria="transporte_urbano", descricao="Corrida", valor="120.00", nota=False))
    assert resumo(s) == ("pendente", "dia_nao_util", ("nota_fiscal_ausente",))


def test_rn019_situacoes_do_exemplo_conforme_a_spec():
    situacoes = avaliar_situacoes(ler_entrada(EXEMPLO.read_text(encoding="utf-8")))
    obtido = {s.despesa.id: resumo(s)[:2] for s in situacoes}
    assert obtido == {
        "d-001": (None, None),
        "d-002": (None, None),
        "d-003": (None, None),
        "d-004": ("pendente", "nota_fiscal_ausente"),
        "d-005": ("recusado", "categoria_fora_da_politica"),
        "d-006": (None, None),
        "d-007": ("desconsiderado", "duplicata"),
        "d-008": ("recusado", "fora_do_periodo"),
        "d-009": ("pendente", "dia_nao_util"),
        "d-010": (None, None),
        "d-011": (None, None),
        "d-012": ("pendente", "dia_nao_util"),
        "d-013": ("pendente", "nota_fiscal_ausente"),
        "d-014": (None, None),
    }
    assert all(s.outros_motivos == () for s in situacoes)
