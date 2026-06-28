import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Prono Mondial 2026", page_icon="🏆", layout="wide")

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .card { background: #1e293b; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# --- DICIONÁRIO DE BANDEIRAS E SELEÇÕES ---
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
    return drapeaux.get(team_name.lower().strip(), "🏳️")

# --- ESTADO DA SESSÃO ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.user_nickname = ""

# --- LÓGICA DE LOGIN ---
if not st.session_state.user_authenticated:
    st.title("🏆 Login - Mundial 2026")
    email = st.text_input("Email")
    nickname = st.text_input("Nickname")
    if st.button("Entrar no Jogo"):
        if email and nickname:
            st.session_state.user_authenticated = True
            st.session_state.user_nickname = nickname
            st.rerun()
else:
    # --- INTERFACE PRINCIPAL ---
    st.sidebar.markdown(f"### 👤 {st.session_state.user_nickname}")
    
    # Botão de Desistir
    if st.sidebar.button("⚠️ Desistir / Sair"):
        st.session_state.user_authenticated = False
        st.rerun()
    
    st.title("⚽ Mundial 2026 - Painel")
    
    # Exemplo de listagem dos grupos conforme definiste
    grupos = {
        "Grupo 1": ["Mexico", "Africa do Sul", "Coreia do Sul", "Republica Checa"],
        "Grupo 2": ["Suica", "Canada", "Bosnia", "Qatar"],
        "Grupo 3": ["Brasil", "Marrocos", "Escocia", "Haiti"],
        "Grupo 4": ["EUA", "Australia", "Turquia", "Paraguai"],
        "Grupo 5": ["Alemanha", "Costa do Marfim", "Ecuador", "Curacao"],
        "Grupo 6": ["Paises Baixos", "Japao", "Suecia", "Tunisia"],
        "Grupo 7": ["Belgica", "Egipto", "Irao", "Nova Zelandia"],
        "Grupo 8": ["Espanha", "Cabo Verde", "Uruguai", "Arabia Saudita"],
        "Grupo 9": ["Franca", "Noruega", "Senegal", "Iraque"],
        "Grupo 10": ["Argentina", "Austria", "Argelia", "Jordania"],
        "Grupo 11": ["Colombia", "Portugal", "Congo", "Uzbequistao"],
        "Grupo 12": ["Inglaterra", "Croacia", "Gana", "Panama"]
    }
    
    for nome_grupo, equipas in grupos.items():
        with st.expander(f"🔹 {nome_grupo}"):
            cols = st.columns(4)
            for i, equipa in enumerate(equipas):
                cols[i].markdown(f"<div class='card'>{get_flag(equipa)} {equipa}</div>", unsafe_allow_html=True)
