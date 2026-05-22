import streamlit as st
import time
import random
from datetime import datetime
from textwrap import dedent

import gspread
from google.oauth2.service_account import Credentials

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(
    page_title="Projeto Desencalha",
    page_icon="💘",
    layout="centered"
)

# ==================================================
# FUNÇÃO HTML
# ==================================================
def html(code):
    st.markdown(
        dedent(code).strip(),
        unsafe_allow_html=True
    )

# ==================================================
# GOOGLE SHEETS
# ==================================================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("Projeto Desencalha - Ranking").sheet1

# ==================================================
# CSS
# ==================================================
html("""
<style>

.main {
    background: radial-gradient(circle at top, #3b0764, #111827 55%, #020617);
}

.block-container {
    max-width: 720px;
    padding-top: 3rem;
}

.card {
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
    text-align: center;
}

.badge {
    display: inline-block;
    background: rgba(236,72,153,0.15);
    color: #f9a8d4;
    border: 1px solid rgba(236,72,153,0.35);
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 18px;
}

.title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    margin-bottom: 10px;
}

.subtitle {
    color: #cbd5e1;
    line-height: 1.6;
    font-size: 17px;
    margin-bottom: 18px;
}

.success-title {
    color: #86efac;
    font-size: 36px;
    font-weight: 900;
}

.error-title {
    color: #fca5a5;
    font-size: 36px;
    font-weight: 900;
}

.mini-card {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    margin: 14px 0;
    text-align: left;
    color: #e5e7eb;
}

.mini-card h3 {
    color: #facc15;
    margin-bottom: 8px;
}

div.stButton > button {
    width: 100%;
    border-radius: 14px;
    padding: 0.7rem 1rem;
    font-weight: 700;
    border: none;
}

</style>
""")

# ==================================================
# SESSION
# ==================================================
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"

if "motivo" not in st.session_state:
    st.session_state.motivo = ""

if "idade" not in st.session_state:
    st.session_state.idade = 0

if "score" not in st.session_state:
    st.session_state.score = 0

# ==================================================
# FUNÇÕES
# ==================================================
def resetar():
    st.session_state.etapa = "inicio"
    st.session_state.motivo = ""
    st.session_state.idade = 0
    st.session_state.score = 0

def loading(destino):

    html("""
    <div class="card">
        <div class="badge">
            ANÁLISE EM ANDAMENTO
        </div>

        <div class="title">
            Analisando candidato...
        </div>

        <div class="subtitle">
            Consultando histórico emocional,
            risco de sumiço e capacidade de
            assumir relacionamento sério.
        </div>
    </div>
    """)

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    st.session_state.etapa = destino
    st.rerun()

def salvar_candidato(nome, idade, instagram, score):

    sheet.append_row([
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        nome,
        idade,
        instagram,
        score,
        "Aprovado"
    ])

def buscar_ranking():

    dados = sheet.get_all_records()

    ranking = sorted(
        dados,
        key=lambda x: int(x["score"]),
        reverse=True
    )

    return ranking[:10]

# ==================================================
# INÍCIO
# ==================================================
if st.session_state.etapa == "inicio":

    html("""
    <div class="card">

        <div class="badge">
            PROCESSO SELETIVO AFETIVO 2026
        </div>

        <div class="title">
            Projeto Desencalha
        </div>

        <div class="subtitle">
            Bem-vindo ao processo oficial de triagem amorosa.<br>
            Responda com sinceridade.<br>
            Mentiras emocionais serão detectadas.
        </div>

    </div>
    """)

    st.write("")

    if st.button("💘 Iniciar candidatura"):
        st.session_state.etapa = "solteiro"
        st.rerun()

# ==================================================
# PERGUNTA 1
# ==================================================
elif st.session_state.etapa == "solteiro":

    st.progress(33)

    html("""
    <div class="card">

        <div class="badge">
            ETAPA 1 DE 3
        </div>

        <div class="title">
            Você é solteiro?
        </div>

        <div class="subtitle">
            Pergunta eliminatória.
        </div>

    </div>
    """)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sim, solteiríssimo"):
            st.session_state.etapa = "idade"
            st.rerun()

    with col2:
        if st.button("Não"):

            st.session_state.motivo = (
                "Infelizmente candidatos comprometidos "
                "não podem prosseguir."
            )

            st.session_state.etapa = "loading_reprovado"
            st.rerun()

# ==================================================
# PERGUNTA 2
# ==================================================
elif st.session_state.etapa == "idade":

    st.progress(66)

    html("""
    <div class="card">

        <div class="badge">
            ETAPA 2 DE 3
        </div>

        <div class="title">
            Você tem quantos anos?
        </div>

        <div class="subtitle">
            Faixa aceita pela comissão:
            entre 25 e 35 anos.
        </div>

    </div>
    """)

    idade = st.number_input(
        "Digite sua idade",
        min_value=0,
        max_value=120,
        step=1
    )

    if st.button("Próximo"):

        if idade < 25:

            st.session_state.motivo = (
                "Infelizmente você não passou. "
                "Candidato ainda está em fase "
                "de desenvolvimento emocional."
            )

            st.session_state.etapa = "loading_reprovado"
            st.rerun()

        elif idade > 35:

            st.session_state.motivo = (
                "Vixi... perdeu a chance. "
                "Volte no tempo e tente novamente."
            )

            st.session_state.etapa = "loading_reprovado"
            st.rerun()

        else:

            st.session_state.idade = idade
            st.session_state.etapa = "preparado"
            st.rerun()

# ==================================================
# PERGUNTA 3
# ==================================================
elif st.session_state.etapa == "preparado":

    st.progress(100)

    html("""
    <div class="card">

        <div class="badge">
            ETAPA 3 DE 3
        </div>

        <div class="title">
            Está 100% preparado?
        </div>

        <div class="subtitle">
            Essa etapa mede coragem,
            maturidade e ausência de trauma
            não resolvido.
        </div>

    </div>
    """)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sim, nasci preparado"):
            st.session_state.etapa = "loading_aprovado"
            st.rerun()

    with col2:
        if st.button("Não sei se estou pronto"):

            st.session_state.motivo = (
                "A candidata procura guerreiros "
                "preparados psicologicamente."
            )

            st.session_state.etapa = "loading_reprovado"
            st.rerun()

# ==================================================
# LOADING
# ==================================================
elif st.session_state.etapa == "loading_reprovado":
    loading("reprovado")

elif st.session_state.etapa == "loading_aprovado":
    loading("formulario")

# ==================================================
# REPROVADO
# ==================================================
elif st.session_state.etapa == "reprovado":

    html(f"""
    <div class="card">

        <div style="font-size:58px;">
            ❌
        </div>

        <div class="error-title">
            Infelizmente você não passou
        </div>

        <div class="subtitle">
            {st.session_state.motivo}
        </div>

    </div>
    """)

    st.write("")

    if st.button("Tentar novamente"):
        resetar()
        st.rerun()

# ==================================================
# FORMULÁRIO
# ==================================================
elif st.session_state.etapa == "formulario":

    html("""
    <div class="card">

        <div style="font-size:58px;">
            🎉
        </div>

        <div class="success-title">
            Aprovado na triagem!
        </div>

        <div class="subtitle">
            Você desbloqueou o formulário oficial
            de candidatura sentimental.
        </div>

    </div>
    """)

    st.write("")

    nome = st.text_input("Seu nome")
    instagram = st.text_input("Instagram")

    if st.button("Enviar candidatura"):

        score = random.randint(70, 100)

        salvar_candidato(
            nome,
            st.session_state.idade,
            instagram,
            score
        )

        st.session_state.score = score
        st.session_state.nome = nome
        st.session_state.etapa = "ranking"

        st.rerun()

# ==================================================
# RANKING
# ==================================================
elif st.session_state.etapa == "ranking":

    html(f"""
    <div class="card">

        <div style="font-size:58px;">
            🏆
        </div>

        <div class="success-title">
            Candidatura enviada!
        </div>

        <div class="subtitle">
            Score emocional de
            <b>{st.session_state.score}</b>
            pontos detectado.
        </div>

    </div>
    """)

    st.write("")

    st.subheader("🏆 Ranking dos Pretendentes")

    ranking = buscar_ranking()

    for i, pessoa in enumerate(ranking, start=1):

        html(f"""
        <div class="mini-card">

            <h3>
                {i}º lugar — {pessoa['nome']}
            </h3>

            <p>
                Score: <b>{pessoa['score']}</b><br>
                Instagram: @{pessoa['instagram']}
            </p>

        </div>
        """)

    st.write("")

    if st.button("Voltar ao início"):
        resetar()
        st.rerun()
