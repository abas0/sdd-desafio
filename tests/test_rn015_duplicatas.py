from motor.regras_item import duplicatas
from tests.fabrica import despesa, em_ordem


def almoco(id):
    return despesa(id=id, data="2026-07-09", descricao="Almoco", fornecedor="Bistro Central", valor="54.90")


def test_rn015_d007_desconsiderado_com_referencia_a_d006():
    ocorrencias = duplicatas(em_ordem(almoco("d-006"), almoco("d-007")))
    assert list(ocorrencias) == [1]
    assert ocorrencias[1].situacao == "desconsiderado"
    assert ocorrencias[1].motivo == "duplicata"
    assert ocorrencias[1].referencia == "d-006"


def test_rn015_tres_iguais_calcula_o_primeiro_e_desconsidera_os_outros_dois():
    ocorrencias = duplicatas(em_ordem(almoco("d-1"), almoco("d-2"), almoco("d-3")))
    assert sorted(ocorrencias) == [1, 2]
    assert {o.referencia for o in ocorrencias.values()} == {"d-1"}


def test_rn015_itens_ja_retirados_pela_rn006_nao_participam():
    despesas = em_ordem(almoco("d-1"), almoco("d-2"))
    assert duplicatas(despesas, excluidas={0}) == {}


def test_rn015_conteudos_diferentes_nao_sao_duplicatas():
    assert duplicatas(em_ordem(almoco("d-1"), despesa(id="d-2", valor="10.00"))) == {}
