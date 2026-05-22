import streamlit as st
import time

st.set_page_config(
    page_title="Projeto Desencalha",
    page_icon="💘",
    layout="centered"
)

# CSS simples para deixar com cara de site e não só app padrão
st.markdown("""
<style>
    .main {
        background: radial-gradient(circle at top, #3b0764, #111827 55%, #020617);
    }

    .block-container {
        max-width: 650px;
        padding-top: 3rem;
    }

    .card {
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.45);
        text-align: center;
    }

    .badge {
        display: inline-block;
        background: rgba(236, 72, 153, 0.16);
        color: #f9a8d4;
        border: 1px solid rgba(236, 72, 153, 0.45);
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
        font-size: 17px;
        line-height: 1.5;
        margin-bottom: 22px;
    }

    .success-title {
        color: #86efac;
        font-size: 34px;
        font-weight: 900;
    }

    .error-title {
        color: #fca5a5;
        font-size: 34px;
        font-weight: 900;
    }

    .mini-card {
        background: rgba(255, 255, 255, 0.08);
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
""", unsafe_allow_html=True)


def init_state():
    if "etapa" not in st.session_state:
        st.session_state.etapa = "inicio"
    if "motivo_reprovacao" not in st.session_state:
        st.session_state.motivo_reprovacao = ""


def resetar():
    st.session_state.etapa = "inicio"
    st.session_state.motivo_reprovacao = ""


def reprovar(mensagem):
    st.session_state.motivo_reprovacao = mensagem
    st.session_state.etapa = "loading_reprovado"
    st.rerun()


def aprovar():
    st.session_state.etapa = "loading_aprovado"
    st.rerun()


def loading(destino):
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="badge">ANÁLISE EM ANDAMENTO</div>
            <div class="title">Analisando candidato...</div>
            <div class="subtitle">
                Consultando histórico emocional, capacidade de resposta e risco de sumiço repentino.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

    st.session_state.etapa = destino
    st.rerun()


init_state()

# INÍCIO
if st.session_state.etapa == "inicio":
    st.markdown("""
    <div class="card">
        <div class="badge">PROCESSO SELETIVO AFETIVO 2026</div>
        <div class="title">Projeto Desencalha</div>
        <div class="subtitle">
            Bem-vindo ao processo oficial de triagem amorosa.<br>
            Responda com sinceridade. Mentiras emocionais serão detectadas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("💘 Iniciar candidatura"):
        st.session_state.etapa = "solteiro"
        st.rerun()

# PERGUNTA 1
elif st.session_state.etapa == "solteiro":
    st.progress(33)
    st.markdown("""
    <div class="card">
        <div class="badge">ETAPA 1 DE 3</div>
        <div class="title">Você é solteiro?</div>
        <div class="subtitle">Pergunta eliminatória. Responda com responsabilidade.</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sim, solteiríssimo"):
            st.session_state.etapa = "idade"
            st.rerun()

    with col2:
        if st.button("Não"):
            reprovar("Infelizmente candidatos comprometidos não podem prosseguir. Requisito básico não atendido.")

# PERGUNTA 2
elif st.session_state.etapa == "idade":
    st.progress(66)
    st.markdown("""
    <div class="card">
        <div class="badge">ETAPA 2 DE 3</div>
        <div class="title">Você tem quantos anos?</div>
        <div class="subtitle">Faixa aceita pela comissão: desconhecida (não sabemos, nem ela sabe)</div>
    </div>
    """, unsafe_allow_html=True)

    idade = st.number_input("Digite sua idade", min_value=0, max_value=120, step=1)

    if st.button("Próximo"):
        if idade == 0:
            st.warning("Digite sua idade para continuar.")
        elif idade < 28:
            reprovar("Infelizmente você não passou. Candidato ainda está em fase de desenvolvimento emocional.")
        elif idade > 35:
            reprovar("Vixi... perdeu a chance. Volte no tempo e tente novamente.")
        else:
            st.session_state.etapa = "preparado"
            st.rerun()

# PERGUNTA 3
elif st.session_state.etapa == "preparado":
    st.progress(100)
    st.markdown("""
    <div class="card">
        <div class="badge">ETAPA 3 DE 3</div>
        <div class="title">Está 100% preparado?</div>
        <div class="subtitle">
            Essa etapa mede coragem, maturidade e ausência de trauma não resolvido.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sim, nasci preparado"):
            aprovar()

    with col2:
        if st.button("Não sei se estou pronto"):
            reprovar("Processo encerrado. A candidata procura guerreiros preparados psicologicamente.")

# LOADING
elif st.session_state.etapa == "loading_reprovado":
    loading("reprovado")

elif st.session_state.etapa == "loading_aprovado":
    loading("home")

# REPROVADO
elif st.session_state.etapa == "reprovado":
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 58px;">❌</div>
        <div class="error-title">Infelizmente você não passou</div>
        <div class="subtitle">{st.session_state.motivo_reprovacao}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("Tentar novamente"):
        resetar()
        st.rerun()

# HOME FINAL
elif st.session_state.etapa == "home":
    st.markdown("""
    <div class="card">
        <div style="font-size: 58px;">🎉</div>
        <div class="success-title">Aprovado na triagem!</div>
        <div class="subtitle">
            Parabéns, candidato. Você desbloqueou o perfil oficial da solteira mais disputada do grupo.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mini-card">
        <h3>Sobre a candidata</h3>
        <p>Linda, gente boa, levemente surtada e oficialmente disponível para uma proposta minimamente decente.</p>
    </div>

    <div class="mini-card">
        <h3>Requisitos mínimos</h3>
        <ul>
            <li>Responder mensagem sem desaparecer por 3 dias</li>
            <li>Ter maturidade emocional básica</li>
            <li>Gostar de sair para comer</li>
            <li>Não usar “deixa acontecer naturalmente” como plano de vida</li>
        </ul>
    </div>

    <div class="mini-card">
        <h3>Benefícios</h3>
        <ul>
            <li>Carinho sob demanda</li>
            <li>Memes ilimitados</li>
            <li>Fofoca premium</li>
            <li>Possibilidade real de desencalhe</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Quero me candidatar"):
        st.info("Formulário em breve! O RH sentimental ainda está configurando essa etapa.")

    if st.button("Voltar ao início"):
        resetar()
        st.rerun()
