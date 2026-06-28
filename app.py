import streamlit as st
import unicodedata

# --- CONFIGURAÇÃO E DESIGN ---
st.set_page_config(page_title="Mundial 2026 PRO", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-left: 5px solid #ffcc00; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .title-text { color: #ffcc00; font-weight: 800; font-size: 2.5rem; text-align: center; }
    .btn-desistir { background-color: #ff4b4b !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- DADOS ---
LISTA_SELECOES = [
    "Mexico", "Africa do Sul", "Coreia do Sul", "Republica Checa", "Suica", "Canada", "Bosnia", "Qatar",
    "Brasil", "Marrocos", "Escocia", "Haiti", "EUA", "Australia", "Turquia", "Paraguai",
    "Alemanha", "Costa do Marfim", "Ecuador", "Curacao", "Paises Baixos", "Japao", "Suecia", "Tunisia",
    "Belgica", "Egipto", "Irao", "Nova Zelandia", "Espanha", "Cabo Verde", "Uruguai", "Arabia Saudita",
    "Franca", "Noruega", "Senegal", "Iraque", "Argentina", "Austria", "Argelia", "Jordania",
    "Colombia", "Portugal", "Congo", "Uzbequistao", "Inglaterra", "Croacia", "Gana", "Panama"
]

def get_flag(team_name):
    drapeaux = {
        "mexico": "🇲🇽", "africa do sul": "🇿🇦", "coreia do sul": "🇰🇷", "republica checa": "🇨🇿",
        "suica": "🇨🇭", "canada": "🇨🇦", "bosnia": "🇧🇦", "qatar": "🇶🇦",
        "brasil": "🇧🇷", "marrocos": "🇲🇦", "escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "haiti": "🇭🇹",
        "eua": "🇺🇸", "australia": "🇦🇺", "turquia": "🇹🇷", "paraguai": "🇵🇾",
        "alemanha": "🇩🇪", "costa do marfim": "🇨🇮", "ecuador": "🇪🇨", "curacao": "🇨🇼",
        "paises baixos": "🇳🇱", "japao": "🇯🇵", "suecia": "🇸🇪", "tunisia": "🇹🇳",
        "belgica": "🇧🇪", "egipto": "🇪🇬", "irao": "🇮🇷", "nova zelandia": "🇳🇿",
        "espanha": "🇪🇸", "cabo verde": "🇨🇻", "uruguai": "🇺🇾", "arabia saudita": "🇸🇦",
        "franca": "🇫🇷", "noruega": "🇳🇴", "senegal": "🇸🇳", "iraque": "🇮🇶",
        "argentina": "🇦🇷", "austria": "🇦🇹", "argelia": "🇩🇿", "jordania": "🇯🇴",
        "colombia": "🇨🇴", "portugal": "🇵🇹", "congo": "🇨🇬", "uzbequistao": "🇺🇿",
        "inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "croacia": "🇭🇷", "gana": "🇬🇭", "panama": "🇵🇦"
    }
    key = "".join(c for c in unicodedata.normalize('NFD', str(team_name).strip().lower()) if unicodedata.category(c) != 'Mn')
    return drapeaux.get(key, "🏳️")

# --- ESTADO ---
if "user" not in st.session_state: st.session_state.user = None
if "matchs" not in st.session_state:
    st.session_state.matchs = {f"16es - Match {i}": {"team1": "Mexico", "team2": "Brasil"} for i in range(1, 17)}

# --- INTERFACE ---
if not st.session_state.user:
    st.markdown("<h1 class='title-text'>🏆 MUNDIAL 2026</h1>", unsafe_allow_html=True)
    nickname = st.text_input("Escolhe o teu Nickname")
    if st.button("ENTRAR NO TORNEIO"):
        if nickname:
            st.session_state.user = nickname
            st.rerun()
else:
    # Sidebar com botão de desistência estilo "Delete"
    st.sidebar.title(f"Bem-vindo, {st.session_state.user}")
    if st.sidebar.button("❌ DESISTIR DO GRUPO", type="primary"):
        st.session_state.user = None
        st.rerun()

    tab1, tab2 = st.tabs(["⚽ JOGOS 16-AVOS", "🛠️ CONFIGURAR"])
    
    with tab1:
        st.header("📋 Calendário Oficial")
        for m_id, data in st.session_state.matchs.items():
            st.markdown(f"""
            <div class='card'>
                <h3 style='color:#ffcc00;'>{m_id}</h3>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span>{get_flag(data['team1'])} {data['team1']}</span>
                    <b>VS</b>
                    <span>{get_flag(data['team2'])} {data['team2']}</span>
                </div>
            </div>""", unsafe_html=True)
            
    with tab2:
        if st.session_state.user: # Apenas admin teria acesso real, aqui simplificado
            st.header("⚙️ Editor de Jogos")
            m_sel = st.selectbox("Escolher Jogo", list(st.session_state.matchs.keys()))
            t1 = st.selectbox("Equipa 1", LISTA_SELECOES, index=LISTA_SELECOES.index(st.session_state.matchs[m_sel]['team1']))
            t2 = st.selectbox("Equipa 2", LISTA_SELECOES, index=LISTA_SELECOES.index(st.session_state.matchs[m_sel]['team2']))
            if st.button("Guardar Alterações"):
                st.session_state.matchs[m_sel] = {"team1": t1, "team2": t2}
                st.rerun()
