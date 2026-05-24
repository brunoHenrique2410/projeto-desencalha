import streamlit as st
import random
import time
from datetime import datetime
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Projeto Desencalha",
    page_icon="💘",
    layout="centered"
)

ASSETS = Path("assets")


# =========================
# GOOGLE SHEETS
# =========================
@st.cache_resource
def conectar_planilha():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)
    return client.open("Projeto Desencalha - Ranking").sheet1


sheet = conectar_planilha()


# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #3b0764, #111827 55%, #020617);
    color: white;
}

.block-container {
    max-width: 820px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stMarkdownContainer"] {
    color: white;
}

.card {
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
    margin-bottom: 18px;
}

.badge {
    display: inline-block;
    background: rgba(236,72,153,0.16);
    color: #f9a8d4;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    border: 1px solid rgba(236,72,153,0.35);
    margin-bottom: 14px;
}

.title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    margin-bottom: 8px;
}

.subtitle {
    font-size: 17px;
    color: #cbd5e1;
    line-height: 1.6;
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

.center {
    text-align: center;
}

.small-muted {
    font-size: 13px;
    color: #94a3b8;
}

div.stButton > button {
    width: 100%;
    border-radius: 14px;
    padding: 0.75rem 1rem;
    font-weight: 800;
    border: none;
}

img {
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# PERGUNTAS DO TESTE
# =========================
PERGUNTAS = [
    {
        "pergunta": "O que fazer quando Vanessa ainda não comeu?",
        "opcoes": ["Discutir", "Ignorar", "Oferecer comida", "Perguntar 'tá brava?'"],
        "correta": "Oferecer comida",
        "erro": "Candidato não sobreviveria ao modo Vanessa em jejum."
    },
    {
        "pergunta": "O que NÃO pode falar sobre o Fluminense?",
        "opcoes": ["Time gigante", "Melhor torcida", "Time pequeno", "Tricolor"],
        "correta": "Time pequeno",
        "erro": "Detectada tentativa de caos emocional tricolor."
    },
    {
        "pergunta": "Qual ambiente Vanessa provavelmente escolheria?",
        "opcoes": ["Roda de pagode", "Retiro espiritual", "Campeonato de xadrez", "Seminário sobre silêncio"],
        "correta": "Roda de pagode",
        "erro": "Compatibilidade social extremamente baixa."
    },
    {
        "pergunta": "Se Vanessa disser: 'amor, comprei só uma coisinha', você:",
        "opcoes": ["Apoia emocionalmente", "Pergunta o valor", "Entra em desespero", "Cancela o cartão"],
        "correta": "Apoia emocionalmente",
        "erro": "Candidato não suportaria o lifestyle financeiro da Vanessa."
    },
    {
        "pergunta": "Melhor date possível:",
        "opcoes": ["Pagode + comida", "Reunião corporativa", "Fila do Detran", "Palestra motivacional"],
        "correta": "Pagode + comida",
        "erro": "Candidato apresenta risco elevado de date sem graça."
    },
    {
        "pergunta": "Qual habilidade é essencial?",
        "opcoes": ["Saber ouvir", "Dirigir caminhão", "Jogar FIFA", "Falar latim"],
        "correta": "Saber ouvir",
        "erro": "Nível crítico de falta de maturidade emocional."
    },
    {
        "pergunta": "Vanessa provavelmente escuta:",
        "opcoes": ["Heavy metal", "Podcast financeiro", "Pagode", "Sons da natureza"],
        "correta": "Pagode",
        "erro": "Compatibilidade musical inexistente."
    },
    {
        "pergunta": "O relacionamento dela com o banco é:",
        "opcoes": ["Saudável", "Profissional", "Extremamente íntimo", "Inexistente"],
        "correta": "Extremamente íntimo",
        "erro": "Candidato subestimou a situação financeira."
    },
    {
        "pergunta": "Experiência dela no sistema prisional significa:",
        "opcoes": ["Alta resistência emocional", "Ela é policial", "Ela luta MMA", "Ela é perigosa"],
        "correta": "Alta resistência emocional",
        "erro": "Candidato claramente não entendeu o lore."
    },
    {
        "pergunta": "Qual dessas frases ela provavelmente diria?",
        "opcoes": ["Eu mereço", "Vou economizar", "Não vou sair hoje", "Não gosto de pagode"],
        "correta": "Eu mereço",
        "erro": "Erro grave de interpretação comportamental."
    },
    {
        "pergunta": "Qual dessas atitudes é obrigatória?",
        "opcoes": ["Responder mensagem", "Sumir por 3 dias", "Visualizar e ignorar", "Responder só com 'kkkk'"],
        "correta": "Responder mensagem",
        "erro": "Candidato identificado como possível causador de trauma."
    },
    {
        "pergunta": "Vanessa é apaixonada por:",
        "opcoes": ["Fluminense", "Vasco", "Silêncio", "Economia"],
        "correta": "Fluminense",
        "erro": "Risco altíssimo de discussão esportiva."
    },
    {
        "pergunta": "O que NÃO fazer num date?",
        "opcoes": ["Chegar atrasado", "Conversar", "Pagar comida", "Escutar ela"],
        "correta": "Chegar atrasado",
        "erro": "Pontualidade emocional inexistente."
    },
    {
        "pergunta": "Qual o maior risco?",
        "opcoes": ["Ela sair comprando", "Ela virar coach", "Ela gostar de sertanejo", "Ela odiar futebol"],
        "correta": "Ela sair comprando",
        "erro": "Candidato ignorou o setor financeiro."
    },
    {
        "pergunta": "Como sobreviver ao estresse matinal?",
        "opcoes": ["Oferecendo café e comida", "Perguntando o motivo", "Discutindo", "Ignorando"],
        "correta": "Oferecendo café e comida",
        "erro": "Candidato não possui instinto de sobrevivência."
    },
    {
        "pergunta": "Qual dessas opções demonstra maturidade?",
        "opcoes": ["Conversar", "Sumir", "Postar indireta", "Dar ghost"],
        "correta": "Conversar",
        "erro": "Sistema detectou comportamento adolescente."
    },
    {
        "pergunta": "Qual dessas frases é perigosa?",
        "opcoes": ["Fluminense é pequeno", "Vamos sair", "Você tá certa", "Trouxe comida"],
        "correta": "Fluminense é pequeno",
        "erro": "Candidato provocou crise institucional."
    },
    {
        "pergunta": "Probabilidade de Vanessa comprar por impulso:",
        "opcoes": ["98%", "2%", "0%", "10%"],
        "correta": "98%",
        "erro": "Candidato claramente não leu a bio."
    },
    {
        "pergunta": "Qual dessas é uma green flag?",
        "opcoes": ["Gostar de sair", "Sumir por dias", "Não responder", "Falar mal de pagode"],
        "correta": "Gostar de sair",
        "erro": "Compatibilidade social rejeitada."
    },
    {
        "pergunta": "O que Vanessa provavelmente faria num domingo?",
        "opcoes": ["Pagode ou futebol", "Seminário financeiro", "Yoga silenciosa", "Caça ao tesouro"],
        "correta": "Pagode ou futebol",
        "erro": "Candidato desconhece totalmente a personalidade dela."
    },
    {
        "pergunta": "Qual dessas opções demonstra inteligência?",
        "opcoes": ["Levar ela pra comer", "Falar mal do Flu", "Responder 2 dias depois", "Ignorar mensagem"],
        "correta": "Levar ela pra comer",
        "erro": "Candidato não entende princípios básicos da felicidade."
    },
    {
        "pergunta": "Qual dessas opções reduz o risco de briga?",
        "opcoes": ["Comida", "Discussão", "Ciúmes", "Sumiço"],
        "correta": "Comida",
        "erro": "Sistema detectou ausência de estratégia emocional."
    },
    {
        "pergunta": "Qual dessas frases ela provavelmente odiaria?",
        "opcoes": ["Pagode é ruim", "Você merece", "Vamos sair", "Trouxe lanche"],
        "correta": "Pagode é ruim",
        "erro": "Crime cultural identificado."
    },
    {
        "pergunta": "Qual dessas opções demonstra preparo psicológico?",
        "opcoes": ["Aceitar o caos", "Entrar em pânico", "Correr", "Desinstalar WhatsApp"],
        "correta": "Aceitar o caos",
        "erro": "Candidato reprovado no teste de resistência."
    },
    {
        "pergunta": "Qual dessas atitudes é mais importante?",
        "opcoes": ["Presença", "Ghosting", "Indireta", "Ignorar"],
        "correta": "Presença",
        "erro": "Candidato apresenta maturidade emocional negativa."
    },
    {
        "pergunta": "O sistema detecta que Vanessa possui:",
        "opcoes": ["Personalidade forte", "Paciência infinita", "Calma absoluta", "Educação financeira avançada"],
        "correta": "Personalidade forte",
        "erro": "Candidato claramente ignorou todas as evidências."
    },
    {
        "pergunta": "Qual a maior mentira já contada pela Vanessa?",
        "opcoes": ["Vou economizar", "Vou dormir cedo", "Só uma cervejinha", "Não vou sair hoje"],
        "correta": "Vou economizar",
        "erro": "Candidato não conhece o histórico financeiro da Vanessa."
    },
    {
        "pergunta": "Qual a frase mais falada pela Vanessa?",
        "opcoes": ["Bom dia", "Ai meu Deus", "Porra", "Tá tranquilo"],
        "correta": "Porra",
        "erro": "Candidato claramente nunca conviveu com a Vanessa por mais de 5 minutos."
    },
    {
        "pergunta": "Vanessa faz aniversário em:",
        "opcoes": ["04/04", "10/10", "01/01", "31/12"],
        "correta": "04/04",
        "erro": "Erro grave: data comemorativa ignorada."
    },
    {
        "pergunta": "Qual área Vanessa estudou?",
        "opcoes": ["Nutrição", "Engenharia", "Direito", "TI"],
        "correta": "Nutrição",
        "erro": "Candidato não sabe nem o básico do currículo dela."
    },
]


PERGUNTAS_FLU = [
    {
        "texto": "Alguém disse: 'Fluminense é time pequeno'. O que você responde?",
        "opcoes": ["Concordo", "Respeita o gigante", "Nem ligo", "Prefiro Vasco"],
        "correta": "Respeita o gigante"
    },
    {
        "texto": "Vanessa pergunta se você assistiria jogo do Flu com ela.",
        "opcoes": ["Claro, com camisa tricolor", "Só se não tiver nada melhor", "Não gosto de futebol", "Vou dormir"],
        "correta": "Claro, com camisa tricolor"
    },
    {
        "texto": "Qual frase é mais segura perto dela?",
        "opcoes": ["Flu é gigante", "Flu não tem torcida", "Futebol é chato", "Prefiro não opinar"],
        "correta": "Flu é gigante"
    },
    {
        "texto": "O Fluminense faz gol. O que você faz?",
        "opcoes": ["Comemoro junto", "Fico mexendo no celular", "Pergunto se já acabou", "Falo que foi sorte"],
        "correta": "Comemoro junto"
    },
    {
        "texto": "Vanessa está vendo jogo decisivo do Flu. Você:",
        "opcoes": ["Fica junto e respeita o momento", "Pede pra trocar de canal", "Fala que futebol é besteira", "Dorme no sofá"],
        "correta": "Fica junto e respeita o momento"
    },
    {
        "texto": "Alguém zoou o Fluminense no grupo. Você:",
        "opcoes": ["Defende a instituição", "Ri junto", "Manda figurinha do rival", "Finge que não viu"],
        "correta": "Defende a instituição"
    },
]


# =========================
# SESSION
# =========================
def iniciar_estado():
    defaults = {
        "etapa": "inicio",
        "motivo": "",
        "idade": 0,
        "nome": "",
        "instagram": "",
        "score": 0,
        "respostas_erradas": [],
        "quiz_perguntas": [],
        "quiz_index": 0,
        "quiz_acertos": 0,
        "estresse": 70,
        "evento_comida": "",
        "pontos_flu": 0,
        "pergunta_flu": 0,
        "perguntas_flu_sorteadas": [],
        "resultado_salvo": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


iniciar_estado()


# =========================
# FUNÇÕES
# =========================
def card_html(conteudo):
    st.markdown(f'<div class="card">{conteudo}</div>', unsafe_allow_html=True)


def resetar_tudo():
    st.session_state.etapa = "inicio"
    st.session_state.motivo = ""
    st.session_state.idade = 0
    st.session_state.nome = ""
    st.session_state.instagram = ""
    st.session_state.score = 0
    st.session_state.respostas_erradas = []
    st.session_state.quiz_perguntas = []
    st.session_state.quiz_index = 0
    st.session_state.quiz_acertos = 0
    st.session_state.estresse = 70
    st.session_state.evento_comida = ""
    st.session_state.pontos_flu = 0
    st.session_state.pergunta_flu = 0
    st.session_state.perguntas_flu_sorteadas = []
    st.session_state.resultado_salvo = False


def loading(destino):
    card_html("""
        <div class="center">
            <div class="badge">ANÁLISE EM ANDAMENTO</div>
            <div class="title">Analisando candidato...</div>
            <div class="subtitle">
                Consultando histórico emocional, risco de sumiço e capacidade de assumir relacionamento sério.
            </div>
        </div>
    """)

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    st.session_state.etapa = destino
    st.rerun()


def salvar_candidato(nome, idade, instagram, score, status):
    sheet.append_row([
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        nome,
        idade,
        instagram,
        score,
        status
    ])


def buscar_ranking():
    dados = sheet.get_all_records()

    if not dados:
        return []

    return sorted(
        dados,
        key=lambda x: int(x.get("score", 0)),
        reverse=True
    )[:10]


def iniciar_quiz():
    st.session_state.quiz_perguntas = random.sample(PERGUNTAS, 10)
    st.session_state.quiz_index = 0
    st.session_state.quiz_acertos = 0
    st.session_state.respostas_erradas = []
    st.session_state.resultado_salvo = False
    st.session_state.etapa = "quiz"
    st.rerun()


def mostrar_fotos():
    fotos = [
        ASSETS / "vanessa1.jpg",
        ASSETS / "vanessa2.jpg",
        ASSETS / "vanessa3.jpg",
    ]

    existentes = [foto for foto in fotos if foto.exists()]

    if not existentes:
        st.info("📸 Coloque as fotos em: assets/vanessa1.jpg, assets/vanessa2.jpg e assets/vanessa3.jpg")
        return

    cols = st.columns(len(existentes))
    for col, foto in zip(cols, existentes):
        with col:
            st.image(str(foto), use_container_width=True)


def mensagem_chance(score):
    if score >= 90:
        return "💘 Vanessa provavelmente responderia rápido. Situação rara detectada."
    if score >= 70:
        return "🙂 Você tem potencial. Ainda precisa sobreviver ao pagode e ao Fluminense."
    if score >= 40:
        return "⚠️ Chance alta de virar só amigo. A comissão está preocupada."
    return "🚫 Sistema recomenda encaminhamento imediato para amizade."


# =========================
# TELA INICIAL
# =========================
if st.session_state.etapa == "inicio":
    card_html("""
        <div class="center">
            <div class="badge">PROCESSO SELETIVO AFETIVO 2026</div>
            <div class="title">Projeto Desencalha</div>
            <div class="subtitle">
                Bem-vindo ao processo oficial de triagem amorosa.<br>
                Responda com sinceridade.<br>
                Mentiras emocionais serão detectadas.
            </div>
        </div>
    """)

    if st.button("💘 Iniciar candidatura"):
        st.session_state.etapa = "solteiro"
        st.rerun()


# =========================
# TRIAGEM 1
# =========================
elif st.session_state.etapa == "solteiro":
    st.progress(33)

    card_html("""
        <div class="center">
            <div class="badge">ETAPA 1 DE 3</div>
            <div class="title">Você é solteiro?</div>
            <div class="subtitle">Pergunta eliminatória. Responda com responsabilidade.</div>
        </div>
    """)

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
# TRIAGEM 2
# =========================
elif st.session_state.etapa == "idade":
    st.progress(66)

    card_html("""
        <div class="center">
            <div class="badge">ETAPA 2 DE 3</div>
            <div class="title">Você tem quantos anos?</div>
            <div class="subtitle">Faixa aceita pela comissão: +28 anos.</div>
        </div>
    """)

    idade = st.number_input("Digite sua idade", min_value=0, max_value=120, step=1)

    if st.button("Próximo"):
        if idade == 0:
            st.warning("Digite sua idade para continuar.")
        elif idade < 27:
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
# TRIAGEM 3
# =========================
elif st.session_state.etapa == "preparado":
    st.progress(100)

    card_html("""
        <div class="center">
            <div class="badge">ETAPA 3 DE 3</div>
            <div class="title">Está 100% preparado?</div>
            <div class="subtitle">
                Essa etapa mede coragem, maturidade e ausência de trauma não resolvido.
            </div>
        </div>
    """)

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
    loading("home")


# =========================
# REPROVADO
# =========================
elif st.session_state.etapa == "reprovado":
    mensagens_reprovacao = [
        "A comissão identificou risco emocional elevado.",
        "Vanessa pediu revisão imediata da candidatura.",
        "Compatibilidade insuficiente para sobreviver ao pagode.",
        "Você não resistiria a um domingo de Fluminense.",
        "Sistema detectou ausência de preparo psicológico.",
    ]

    card_html(f"""
        <div class="center">
            <div style="font-size:58px;">❌</div>
            <div class="error-title">Infelizmente você não passou</div>
            <div class="subtitle">{st.session_state.motivo}</div>
            <br>
            <div class="subtitle"><b>{random.choice(mensagens_reprovacao)}</b></div>
        </div>
    """)

    if st.button("Tentar novamente"):
        resetar_tudo()
        st.rerun()


# =========================
# HOME
# =========================
elif st.session_state.etapa == "home":
    card_html("""
        <div class="center">
            <div class="badge">PERFIL DESBLOQUEADO</div>
            <div class="title">Vanessa Souza</div>
            <div class="subtitle">
                Carioca, pagodeira, nutricionista e torcedora completamente apaixonada pelo Fluminense.
            </div>
        </div>
    """)

    mostrar_fotos()

    st.markdown("""
    <div class="mini-card">
        <h3>💘 Sobre ela</h3>
        <p>
            📍 Carioca<br>
            🎂 Aniversário: 04/04<br>
            🎓 Nutricionista<br>
            ⚽ Fluminense acima de tudo<br>
            🎶 Pagodeira oficial<br>
            🍻 Ama sair<br>
            😡 Perigosa antes do café da manhã<br>
            🚔 Já sobreviveu ao sistema prisional brasileiro<br>
            🔥 Personalidade forte<br>
            ⚠️ Alta resistência emocional
        </p>
    </div>

    <div class="mini-card">
        <h3>📊 Estatísticas Financeiras</h3>
        <p>
            💸 Educação financeira: inexistente<br>
            🛒 Controle de gastos: em análise<br>
            📦 Probabilidade de comprar por impulso: 98%<br>
            💳 Frase mais usada: <b>“eu mereço”</b><br>
            🏦 Relacionamento com o banco: extremamente íntimo<br>
            📈 Planejamento financeiro: esperança e oração
        </p>
    </div>

    <div class="mini-card">
        <h3>✅ Green Flags</h3>
        <p>
            ✅ Gosta de sair<br>
            ✅ Conversa bem<br>
            ✅ Engraçada<br>
            ✅ Parceira<br>
            ✅ Pagode + futebol<br>
            ✅ Personalidade forte
        </p>
    </div>

    <div class="mini-card">
        <h3>🚨 Red Flags</h3>
        <p>
            🚨 Fome<br>
            🚨 Estresse matinal<br>
            🚨 Defesa automática do Fluminense<br>
            🚨 “Só vou dar uma olhadinha”<br>
            🚨 Risco financeiro elevado
        </p>
    </div>

    <div class="mini-card">
        <h3>👼 Cupidos Oficiais</h3>
        <p>
            Bruno<br>
            Amigas da Vanessa<br>
            Setor de fofoca<br>
            RH sentimental<br>
            Comissão anti-encalhe
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🍔 Alimentar Vanessa"):
            st.session_state.estresse = 70
            st.session_state.evento_comida = ""
            st.session_state.etapa = "game_comida"
            st.rerun()

    with col2:
        if st.button("⚽ Defender o Fluminense"):
            st.session_state.pontos_flu = 0
            st.session_state.pergunta_flu = 0
            st.session_state.perguntas_flu_sorteadas = random.sample(PERGUNTAS_FLU, 4)
            st.session_state.etapa = "game_flu"
            st.rerun()

    if st.button("💘 Quero me candidatar"):
        st.session_state.etapa = "formulario"
        st.rerun()

    if st.button("🏆 Ver ranking"):
        st.session_state.etapa = "ranking"
        st.rerun()


# =========================
# GAME COMIDA
# =========================
elif st.session_state.etapa == "game_comida":
    card_html("""
        <div class="center">
            <div class="badge">MINI GAME</div>
            <div class="title">🍔 Alimente Vanessa</div>
            <div class="subtitle">
                Vanessa acordou sem comer. Sua missão é reduzir o estresse antes que seja tarde demais.
            </div>
        </div>
    """)

    st.session_state.estresse = max(0, min(100, st.session_state.estresse))

    st.progress(st.session_state.estresse)
    st.subheader(f"😡 Estresse atual: {st.session_state.estresse}%")

    if st.session_state.evento_comida:
        st.info(st.session_state.evento_comida)

    eventos = [
        ("💸 Vanessa viu promoção na Shopee. Estresse +20.", 20),
        ("⚽ Alguém falou mal do Fluminense. Estresse +25.", 25),
        ("🎶 Começou um pagode bom. Estresse -15.", -15),
        ("🍟 Chegou o iFood. Estresse -30.", -30),
        ("💳 Nubank mandou notificação. Estresse +15.", 15),
        ("☕ Café entregue com sucesso. Estresse -20.", -20),
        ("🍔 Lanche criminoso detectado. Estresse -35.", -35),
    ]

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🍔 Dar lanche"):
            st.session_state.estresse -= random.randint(20, 35)
            st.session_state.evento_comida = "🍔 Lanche aplicado com sucesso."
            st.rerun()

        if st.button("☕ Dar café"):
            st.session_state.estresse -= random.randint(10, 25)
            st.session_state.evento_comida = "☕ Café reduziu o risco de guerra civil."
            st.rerun()

    with col2:
        if st.button("🍟 Pedir iFood"):
            st.session_state.estresse -= random.randint(25, 40)
            st.session_state.evento_comida = "🍟 iFood chegou. A paz foi temporariamente restaurada."
            st.rerun()

        if st.button("🎲 Evento aleatório"):
            texto, impacto = random.choice(eventos)
            st.session_state.estresse += impacto
            st.session_state.evento_comida = texto
            st.rerun()

    st.session_state.estresse = max(0, min(100, st.session_state.estresse))

    if st.session_state.estresse <= 0:
        st.success("✅ Parabéns! Você sobreviveu à Vanessa em jejum.")
    elif st.session_state.estresse >= 100:
        st.error("💀 Você falhou. Vanessa entrou em modo destruição.")

    if st.button("⬅️ Voltar para Home"):
        st.session_state.estresse = 70
        st.session_state.evento_comida = ""
        st.session_state.etapa = "home"
        st.rerun()


# =========================
# GAME FLUMINENSE
# =========================
elif st.session_state.etapa == "game_flu":
    card_html("""
        <div class="center">
            <div class="badge">MINI GAME</div>
            <div class="title">⚽ Defesa do Fluminense</div>
            <div class="subtitle">
                As perguntas são sorteadas. Prove que você respeita a instituição Fluminense Football Club.
            </div>
        </div>
    """)

    if not st.session_state.perguntas_flu_sorteadas:
        st.session_state.perguntas_flu_sorteadas = random.sample(PERGUNTAS_FLU, 4)

    pergunta = st.session_state.perguntas_flu_sorteadas[st.session_state.pergunta_flu]
    total_flu = len(st.session_state.perguntas_flu_sorteadas)

    st.progress((st.session_state.pergunta_flu + 1) / total_flu)
    st.subheader(pergunta["texto"])

    opcoes = pergunta["opcoes"].copy()
    random.shuffle(opcoes)

    for opcao in opcoes:
        if st.button(opcao):
            if opcao == pergunta["correta"]:
                st.session_state.pontos_flu += 1
            st.session_state.pergunta_flu += 1

            if st.session_state.pergunta_flu >= total_flu:
                st.session_state.etapa = "resultado_flu"

            st.rerun()

    if st.button("⬅️ Voltar"):
        st.session_state.pontos_flu = 0
        st.session_state.pergunta_flu = 0
        st.session_state.perguntas_flu_sorteadas = []
        st.session_state.etapa = "home"
        st.rerun()


# =========================
# RESULTADO FLUMINENSE
# =========================
elif st.session_state.etapa == "resultado_flu":
    total = len(st.session_state.perguntas_flu_sorteadas)

    card_html("""
        <div class="center">
            <div class="badge">RESULTADO</div>
            <div class="title">🏁 Resultado Tricolor</div>
        </div>
    """)

    if st.session_state.pontos_flu >= 3:
        st.success(f"✅ Aprovado! Você fez {st.session_state.pontos_flu}/{total}. Compatibilidade futebolística detectada.")
    else:
        st.error(f"❌ Reprovado. Você fez {st.session_state.pontos_flu}/{total}. Relacionamento encerrado por motivos esportivos.")

    if st.button("Voltar para Home"):
        st.session_state.pontos_flu = 0
        st.session_state.pergunta_flu = 0
        st.session_state.perguntas_flu_sorteadas = []
        st.session_state.etapa = "home"
        st.rerun()


# =========================
# FORMULÁRIO
# =========================
elif st.session_state.etapa == "formulario":
    card_html("""
        <div class="center">
            <div class="badge">CANDIDATURA OFICIAL</div>
            <div class="title">Formulário sentimental</div>
            <div class="subtitle">
                Antes do teste, informe seus dados para entrar no ranking.
            </div>
        </div>
    """)

    nome = st.text_input("Seu nome")
    instagram = st.text_input("Instagram")

    if st.button("Iniciar teste de compatibilidade"):
        if not nome.strip():
            st.warning("Digite seu nome para continuar.")
        else:
            st.session_state.nome = nome.strip()
            st.session_state.instagram = instagram.strip()
            iniciar_quiz()

    if st.button("⬅️ Voltar para Home"):
        st.session_state.etapa = "home"
        st.rerun()


# =========================
# QUIZ
# =========================
elif st.session_state.etapa == "quiz":
    perguntas = st.session_state.quiz_perguntas
    index = st.session_state.quiz_index
    pergunta = perguntas[index]

    st.progress((index + 1) / 10)

    card_html(f"""
        <div class="center">
            <div class="badge">TESTE DE COMPATIBILIDADE</div>
            <div class="title">Pergunta {index + 1}/10</div>
            <div class="subtitle">{pergunta["pergunta"]}</div>
        </div>
    """)

    opcoes_embaralhadas = pergunta["opcoes"].copy()
    random.shuffle(opcoes_embaralhadas)

    for opcao in opcoes_embaralhadas:
        if st.button(opcao):
            if opcao == pergunta["correta"]:
                st.session_state.quiz_acertos += 1
            else:
                st.session_state.respostas_erradas.append({
                    "pergunta": pergunta["pergunta"],
                    "resposta": opcao,
                    "correta": pergunta["correta"],
                    "erro": pergunta["erro"]
                })

            st.session_state.quiz_index += 1

            if st.session_state.quiz_index >= 10:
                st.session_state.etapa = "resultado_quiz"

            st.rerun()


# =========================
# RESULTADO QUIZ
# =========================
elif st.session_state.etapa == "resultado_quiz":
    acertos = st.session_state.quiz_acertos
    score = acertos * 10
    aprovado = acertos >= 7

    st.session_state.score = score
    status = "Aprovado" if aprovado else "Reprovado"

    if not st.session_state.resultado_salvo:
        salvar_candidato(
            st.session_state.nome,
            st.session_state.idade,
            st.session_state.instagram,
            score,
            status
        )
        st.session_state.resultado_salvo = True

    if aprovado:
        card_html(f"""
            <div class="center">
                <div style="font-size:58px;">🎉</div>
                <div class="success-title">Parabéns, candidato aprovado!</div>
                <div class="subtitle">
                    Você acertou <b>{acertos}/10</b>.<br>
                    Compatibilidade detectada: <b>{score}%</b>.<br>
                    {mensagem_chance(score)}
                </div>
            </div>
        """)
    else:
        card_html(f"""
            <div class="center">
                <div style="font-size:58px;">💀</div>
                <div class="error-title">Reprovado no teste sentimental</div>
                <div class="subtitle">
                    Você acertou apenas <b>{acertos}/10</b>.<br>
                    Compatibilidade detectada: <b>{score}%</b>.<br>
                    {mensagem_chance(score)}
                </div>
            </div>
        """)

        st.subheader("Relatório de vergonha")
        for erro in st.session_state.respostas_erradas:
            st.markdown(f"""
            <div class="mini-card">
                <h3>{erro["pergunta"]}</h3>
                <p>
                    Sua resposta: <b>{erro["resposta"]}</b><br>
                    Resposta ideal: <b>{erro["correta"]}</b><br>
                    🚨 {erro["erro"]}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.progress(score / 100)
    st.metric("Compatibilidade", f"{score}%")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏆 Ver ranking"):
            st.session_state.etapa = "ranking"
            st.rerun()

    with col2:
        if st.button("Voltar ao início"):
            resetar_tudo()
            st.rerun()


# =========================
# RANKING
# =========================
elif st.session_state.etapa == "ranking":
    card_html("""
        <div class="center">
            <div style="font-size:58px;">🏆</div>
            <div class="title">Ranking dos Pretendentes</div>
            <div class="subtitle">
                Classificação oficial do processo seletivo afetivo.
            </div>
        </div>
    """)

    ranking = buscar_ranking()
    medalhas = ["🥇", "🥈", "🥉"]

    if not ranking:
        st.info("Ainda não há candidatos no ranking.")
    else:
        for i, pessoa in enumerate(ranking, start=1):
            nome = pessoa.get("nome", "Candidato misterioso")
            score = pessoa.get("score", 0)
            instagram = pessoa.get("instagram", "")
            status = pessoa.get("status", "")

            if i <= 3:
                titulo = f"{medalhas[i - 1]} {nome}"
            else:
                titulo = f"{i}º lugar — {nome}"

            st.markdown(f"""
            <div class="mini-card">
                <h3>{titulo}</h3>
                <p>
                    Score: <b>{score}%</b><br>
                    Instagram: @{instagram}<br>
                    Status: <b>{status}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

    if st.button("⬅️ Voltar para Home"):
        st.session_state.etapa = "home"
        st.rerun()
