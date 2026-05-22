import streamlit as st
import time
import random
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="Projeto Desencalha",
    page_icon="💘",
    layout="centered"
)

# =========================
# GOOGLE SHEETS
# =========================
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

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #3b0764, #111827 55%, #020617);
}

.block-container {
    max-width: 720px;
    padding-top: 3rem;
}

.big-title {
    font-size: 46px;
    font-weight: 900;
    color: white;
    text-align: center;
    margin-bottom: 12px;
}

.subtitle {
    font-size: 18px;
    color: #cbd5e1;
    text-align: center;
    line-height: 1.6;
}

.badge {
    display: block;
    background: rgba(236,72,153,0.16);
    color: #f9a8d4;
    padding: 8px 14px;
    border-radius: 999px;
    text-align: center;
    width: fit-content;
    margin: 0 auto 18px auto;
    font-size: 13px;
    font-weight: 800;
    border: 1px solid rgba(236,72,153,0.35);
}

.box {
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
    margin-bottom: 22px;
}

.success-title {
    color: #86efac;
    font-size: 36px;
    text-align: center;
    font-weight: 900;
}

.error-title {
    color: #fca5a5;
    font-size: 36px;
    text-align: center;
    font-weight: 900;
}

.icon {
    font-size: 58px;
    text-align: center;
}

.mini-card {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    margin: 14px 0;
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
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"

if "motivo" not in st.session_state:
    st.session_state.motivo = ""

if "idade" not in st.session_state:
    st.session_state.idade = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "nome" not in st.session_state:
    st.session_state.nome = ""

# =========================
# FUNÇÕES
# =========================
def resetar():
    st.session_state.etapa = "inicio"
    st.session_state.motivo = ""
    st.session_state.idade = 0
    st.session_state.score = 0
    st.session_state.nome = ""

def abrir_box():
    st.markdown('<div class="box">', unsafe_allow_html=True)

def fechar_box():
    st.markdown('</div>', unsafe_allow_html=True)

def cabecalho(badge, titulo, subtitulo):
    abrir_box()
    st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-title">{titulo}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{subtitulo}</div>', unsafe_allow_html=True)
    fechar_box()

def loading(destino):
    cabecalho(
        "ANÁLISE EM ANDAMENTO",
        "Analisando candidato...",
        "Consultando histórico emocional, risco de sumiço e capacidade de assumir relacionamento sério."
    )

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

    if not dados:
        return []

    ranking = sorted(
        dados,
        key=lambda x: int(x.get("score", 0)),
        reverse=True
    )

    return ranking[:10]

# =========================
# INÍCIO
# =========================
if st.session_state.etapa == "inicio":
    cabecalho(
        "PROCESSO SELETIVO AFETIVO 2026",
        "Projeto Desencalha",
        "Bem-vindo ao processo oficial de triagem amorosa.<br>Responda com sinceridade.<br>Mentiras emocionais serão detectadas."
    )

    if st.button("💘 Iniciar candidatura"):
        st.session_state.etapa = "solteiro"
        st.rerun()

# =========================
# PERGUNTA 1
# =========================
elif st.session_state.etapa == "solteiro":
    st.progress(33)

    cabecalho(
        "ETAPA 1 DE 3",
        "Você é solteiro?",
        "Pergunta eliminatória. Responda com responsabilidade."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sim, solteiríssimo"):
            st.session_state.etapa = "idade"
            st.rerun()

    with col2:
        if st.button("Não"):
            st.session_state.motivo = "Infelizmente candidatos comprometidos não podem prosseguir. Requisito básico não atendido."
            st.session_state.etapa = "loading_reprovado"
            st.rerun()

# =========================
# PERGUNTA 2
# =========================
elif st.session_state.etapa == "idade":
    st.progress(66)

    cabecalho(
        "ETAPA 2 DE 3",
        "Você tem quantos anos?",
        "Faixa aceita pela comissão: entre 25 e 35 anos."
    )

    idade = st.number_input(
        "Digite sua idade",
        min_value=0,
        max_value=120,
        step=1
    )

    if st.button("Próximo"):
        if idade == 0:
            st.warning("Digite sua idade para continuar.")

        elif idade < 25:
            st.session_state.motivo = "Infelizmente você não passou. Candidato ainda está em fase de desenvolvimento emocional."
            st.session_state.etapa = "loading_reprovado"
            st.rerun()

        elif idade > 35:
            st.session_state.motivo = "Vixi... perdeu a chance. Volte no tempo e tente novamente."
            st.session_state.etapa = "loading_reprovado"
            st.rerun()

        else:
            st.session_state.idade = idade
            st.session_state.etapa = "preparado"
            st.rerun()

# =========================
# PERGUNTA 3
# =========================
elif st.session_state.etapa == "preparado":
    st.progress(100)

    cabecalho(
        "ETAPA 3 DE 3",
        "Está 100% preparado?",
        "Essa etapa mede coragem, maturidade e ausência de trauma não resolvido."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sim, nasci preparado"):
            st.session_state.etapa = "loading_aprovado"
            st.rerun()

    with col2:
        if st.button("Não sei se estou pronto"):
            st.session_state.motivo = "Processo encerrado. A candidata procura guerreiros preparados psicologicamente."
            st.session_state.etapa = "loading_reprovado"
            st.rerun()

# =========================
# LOADING
# =========================
elif st.session_state.etapa == "loading_reprovado":
    loading("reprovado")

elif st.session_state.etapa == "loading_aprovado":
    loading("formulario")

# =========================
# REPROVADO
# =========================
elif st.session_state.etapa == "reprovado":
    abrir_box()
    st.markdown('<div class="icon">❌</div>', unsafe_allow_html=True)
    st.markdown('<div class="error-title">Infelizmente você não passou</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{st.session_state.motivo}</div>', unsafe_allow_html=True)
    fechar_box()

    if st.button("Tentar novamente"):
        resetar()
        st.rerun()

# =========================
# FORMULÁRIO
# =========================
elif st.session_state.etapa == "formulario":
    abrir_box()
    st.markdown('<div class="icon">🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-title">Aprovado na triagem!</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Você desbloqueou o formulário oficial de candidatura sentimental.</div>',
        unsafe_allow_html=True
    )
    fechar_box()

    nome = st.text_input("Seu nome")
    instagram = st.text_input("Instagram")

    if st.button("Enviar candidatura"):
        if not nome.strip():
            st.warning("Digite seu nome para entrar no ranking.")
        else:
            score = random.randint(70, 100)

            salvar_candidato(
                nome.strip(),
                st.session_state.idade,
                instagram.strip(),
                score
            )

            st.session_state.score = score
            st.session_state.nome = nome.strip()
            st.session_state.etapa = "ranking"
            st.rerun()

# =========================
# RANKING
# =========================
elif st.session_state.etapa == "ranking":
    abrir_box()
    st.markdown('<div class="icon">🏆</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-title">Candidatura enviada!</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="subtitle">Score emocional de <b>{st.session_state.score}</b> pontos detectado.</div>',
        unsafe_allow_html=True
    )
    fechar_box()

    st.subheader("🏆 Ranking dos Pretendentes")

    ranking = buscar_ranking()

    if not ranking:
        st.info("Ainda não há candidatos no ranking.")
    else:
        for i, pessoa in enumerate(ranking, start=1):
            nome = pessoa.get("nome", "Candidato misterioso")
            score = pessoa.get("score", 0)
            instagram = pessoa.get("instagram", "")

            st.markdown(
                f"""
                <div class="mini-card">
                    <h3>{i}º lugar — {nome}</h3>
                    <p>
                        Score: <b>{score}</b><br>
                        Instagram: @{instagram}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    if st.button("Voltar ao início"):
        resetar()
        st.rerun()
