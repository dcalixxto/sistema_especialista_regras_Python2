"""Fase 4 — validação do sistema especialista com personas de teste.

Executar:  python -m pytest -v
"""

import random

import pytest

from consultor import PERGUNTAS, REGRAS, TRILHAS, diagnosticar
from consultor.motor import ConsultorCarreira
from consultor.personas import PERSONAS


@pytest.mark.parametrize("persona", PERSONAS, ids=[p["esperado"] for p in PERSONAS])
def test_persona_recebe_trilha_esperada(persona):
    resultado = diagnosticar(persona["respostas"])
    assert resultado.trilha == persona["esperado"], resultado.ranking[:3]
    # A vencedora deve ter vantagem clara (sem empate com a segunda colocada)
    assert resultado.ranking[0][1] > resultado.ranking[1][1]
    # E ao menos uma regra decisiva (peso 3) como justificativa
    assert any(j["peso"] == 3 for j in resultado.justificativas)


def test_personas_cobrem_as_10_trilhas():
    assert {p["esperado"] for p in PERSONAS} == set(TRILHAS)


def test_desambiguacao_cientista_x_engenheiro_de_dados():
    base = dict(matematica="alta", atividade="dados", ferramenta="python", entrega="dados",
                plataforma="indiferente", automacao="media", comunicacao="media")
    assert diagnosticar({**base, "dados_foco": "modelar"}).trilha == "dados_ml"
    assert diagnosticar({**base, "dados_foco": "pipelines"}).trilha == "eng_dados"


def test_desambiguacao_devops_x_cloud():
    base = dict(matematica="media", atividade="servidores", ferramenta="linux_redes", entrega="infraestrutura",
                dados_foco="nenhum", comunicacao="media")
    assert diagnosticar({**base, "plataforma": "indiferente", "automacao": "alta"}).trilha == "devops"
    assert diagnosticar({**base, "plataforma": "nuvem", "automacao": "media"}).trilha == "cloud"


def test_desambiguacao_frontend_x_mobile():
    base = dict(matematica="media", atividade="layouts", ferramenta="javascript", entrega="produto_usuario",
                dados_foco="nenhum", automacao="baixa", comunicacao="media")
    assert diagnosticar({**base, "plataforma": "web"}).trilha == "frontend"
    assert diagnosticar({**base, "plataforma": "mobile"}).trilha == "mobile"


def test_regras_suficientes_e_catalogo_sincronizado():
    regras_motor = {nome[:3].upper() for nome in dir(ConsultorCarreira) if nome[:1] == "r" and nome[1:3].isdigit()}
    assert regras_motor == set(REGRAS)
    assert len(regras_motor) >= 25


def test_respostas_aleatorias_sempre_geram_diagnostico():
    rng = random.Random(42)
    for _ in range(200):
        respostas = {p["chave"]: rng.choice(list(p["opcoes"])) for p in PERGUNTAS}
        resultado = diagnosticar(respostas)
        assert resultado.trilha in TRILHAS
        assert "R99" in resultado.regras_disparadas


def test_respostas_invalidas_sao_rejeitadas():
    with pytest.raises(ValueError):
        diagnosticar({"matematica": "alta"})
    with pytest.raises(ValueError):
        diagnosticar({**PERSONAS[0]["respostas"], "plataforma": "tv"})
