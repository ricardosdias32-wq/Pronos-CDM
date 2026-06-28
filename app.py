import streamlit as st
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Prono Mondial - Pro Edition", page_icon="🏆", layout="wide")

# --- STYLES VISUELS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    .kpi-box { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #4c1d95; }
    .match-box { background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 6px solid #3b82f6; margin-bottom: 20px; }
    .tree-box { background-color: #0f172a; padding: 12px; border-radius: 8px; border: 1px solid #334155; color: #e2e8f0; margin-bottom: 15px; font-size: 14px; }
    .vs-text { font-size: 22px; font-weight: bold; color: #94a3b8; text-align: center; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION SESSION STATE ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.user_email = ""
    st.session_state.user_nickname = ""
    st.session_state.is_admin = False

if "matchs" not in st.session_state:
    st.session_state.matchs = {
        "16es - Match 1": {"team1": "Allemagne", "flag1": "🇩🇪", "team2": "Paraguay", "flag2": "🇵🇾", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 2": {"team1": "France", "flag1": "🇫🇷", "team2": "Suède", "flag2": "🇸🇪", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        # ... (podes manter a tua lista completa aqui)
    }

if "pronos" not in st.session_state: 
    st.session_state.pronos = {}

# --- LÓGICA DE ATUALIZAÇÃO ---
def actualiser_arbre_dynamique():
    m = st.session_state.matchs
    # (Logica da árvore aqui...)
    pass

actualiser_arbre_dynamique()

# --- LOGIN ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align: center;'>🏆 LOBBY DES PRONOSTICS</h1>", unsafe_allow_html=True)
    email = st.text_input("Email").strip()
    nickname = st.text_input("Nickname").strip()
    code_salle = st.text_input("Código", type="password")
    
    if st.button("Entrar"):
        if code_salle == "LoungeCDM" and email and nickname:
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            st.session_state.user_nickname = nickname
            st.session_state.is_admin = (email.lower() == "ricardosdias32@gmail.com")
            st.rerun()
        else:
            st.error("Dados incorretos.")
else:
    # --- INTERFACE ---
    st.sidebar.markdown(f"### 👤 {st.session_state.user_nickname}")
    if st.sidebar.button("Logout"):
        st.session_state.user_authenticated = False
        st.rerun()
    
    st.write("Bem-vindo ao sistema!")
    # O restante do código vai aqui...
