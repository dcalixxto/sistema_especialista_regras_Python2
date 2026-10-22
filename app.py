"""Interface web (Streamlit) do Consultor Inteligente de Carreiras em TI.

Executar:  streamlit run app.py
"""

import pandas as pd
import streamlit as st

from consultor import PERGUNTAS, REGRAS, TRILHAS, diagnosticar
from consultor.personas import PERSONAS

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="wide")

TIPOS_REGRA = {
    "caracteristica": "Característica (fato intermediário)",
    "afinidade": "Afinidade direta",
    "decisiva": "Decisiva (+3)",
    "suporte": "Suporte (+1/+2)",
    "desambiguacao": "Desambiguação (negativa)",
    "diagnostico": "Diagnóstico final",
}

with st.sidebar:
    st.title("🧭 Consultor de Carreiras")
    st.write(
        "Sistema Especialista baseado em regras (**Experta**, encadeamento para frente) "
        "que recomenda uma entre 10 trilhas de carreira em TI."
    )
    st.metric("Regras na base de conhecimento", len(REGRAS))
    st.metric("Trilhas possíveis", len(TRILHAS))
    st.caption("UNIPAC Barbacena — Inteligência Artificial")

aba_consultor, aba_base, aba_personas = st.tabs(["🧭 Consultor", "📚 Base de conhecimento", "🧪 Validação (personas)"])

# --------------------------------------------------------------------------- #
# Aba 1 — entrevista e diagnóstico
# --------------------------------------------------------------------------- #
with aba_consultor:
    st.header("Entrevista de carreira")
    st.write("Responda às perguntas abaixo. Não há respostas certas — escolha o que mais combina com você.")

    with st.form("entrevista"):
        respostas = {}
        col_a, col_b = st.columns(2)
        for i, p in enumerate(PERGUNTAS):
            with (col_a if i % 2 == 0 else col_b):
                respostas[p["chave"]] = st.radio(
                    f"**{i + 1}. {p['pergunta']}**",
                    options=list(p["opcoes"]),
                    format_func=p["opcoes"].get,
                    index=None,
                    key=f"q_{p['chave']}",
                )
        enviado = st.form_submit_button("Descobrir minha trilha", type="primary", width="stretch")

    if enviado:
        pendentes = [i + 1 for i, p in enumerate(PERGUNTAS) if respostas[p["chave"]] is None]
        if pendentes:
            st.warning(f"Responda todas as perguntas. Pendentes: {', '.join(map(str, pendentes))}.")
        else:
            st.session_state["resultado"] = diagnosticar(respostas)

    resultado = st.session_state.get("resultado")
    if resultado:
        info = resultado.info
        st.divider()
        st.subheader("Recomendação")
        st.success(f"## {info['icone']} {info['nome']}\n{info['descricao']}")

        col_just, col_rank = st.columns([3, 2])
        with col_just:
            st.markdown("#### Por que esta trilha?")
            st.caption("Regras que dispararam a favor (ou contra) a trilha recomendada:")
            for j in resultado.justificativas:
                sinal = "✅" if j["peso"] > 0 else "⚠️"
                st.markdown(f"{sinal} **{j['regra']}** ({j['peso']:+d}) — {j['motivo']}")

            if resultado.caracteristicas:
                st.markdown("#### Características inferidas do seu perfil")
                for c in resultado.caracteristicas:
                    st.markdown(f"- **{c['nome'].upper()}** ({c['regra']}) — {c['motivo']}")

            st.markdown("#### Primeiros passos sugeridos")
            for passo in info["passos"]:
                st.markdown(f"- {passo}")

        with col_rank:
            st.markdown("#### Pontuação por trilha")
            df = pd.DataFrame(
                [(TRILHAS[t]["nome"], pts) for t, pts in resultado.ranking],
                columns=["Trilha", "Pontos"],
            ).set_index("Trilha")
            st.bar_chart(df, horizontal=True)
            segunda, pts2 = resultado.ranking[1]
            if pts2 > 0:
                st.info(f"Segunda opção: **{TRILHAS[segunda]['nome']}** ({pts2} pontos)")

        with st.expander("Detalhes técnicos da inferência"):
            st.write("Regras disparadas:", ", ".join(resultado.regras_disparadas))
            st.json(respostas)

# --------------------------------------------------------------------------- #
# Aba 2 — base de conhecimento
# --------------------------------------------------------------------------- #
with aba_base:
    st.header("Base de conhecimento")
    st.write(
        "O motor trabalha em **dois níveis**: regras de *característica* derivam fatos intermediários "
        "(ex.: perfil ANALÍTICO) que alimentam as regras de cada trilha. Regras de *desambiguação* "
        "aplicam pesos negativos para separar trilhas parecidas (Ciência × Engenharia de Dados, "
        "DevOps × Cloud, Front-end × Mobile)."
    )
    tabela = pd.DataFrame(
        [(rid, TIPOS_REGRA[tipo], texto) for rid, (tipo, texto) in REGRAS.items()],
        columns=["Regra", "Tipo", "SE … ENTÃO …"],
    )
    st.dataframe(tabela, hide_index=True, width="stretch")

    st.subheader("As 10 trilhas")
    for t in TRILHAS.values():
        st.markdown(f"**{t['icone']} {t['nome']}** — {t['descricao']}")

# --------------------------------------------------------------------------- #
# Aba 3 — validação com personas
# --------------------------------------------------------------------------- #
with aba_personas:
    st.header("Validação com personas de teste")
    linhas = []
    for persona in PERSONAS:
        r = diagnosticar(persona["respostas"])
        linhas.append({
            "Persona": persona["nome"],
            "Esperado": TRILHAS[persona["esperado"]]["nome"],
            "Obtido": TRILHAS[r.trilha]["nome"],
            "Pontos": r.pontos,
            "Regras decisivas": ", ".join(j["regra"] for j in r.justificativas if j["peso"] == 3),
            "Resultado": "✅ Acertou" if r.trilha == persona["esperado"] else "❌ Errou",
        })
    acertos = sum(l["Resultado"].startswith("✅") for l in linhas)
    st.metric("Taxa de acerto", f"{acertos}/{len(linhas)}", f"{acertos / len(linhas):.0%}")
    st.dataframe(pd.DataFrame(linhas), hide_index=True, width="stretch")
