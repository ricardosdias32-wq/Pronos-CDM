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
    .badge-status { padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION SESSION STATE ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.user_email = ""
    st.session_state.user_nickname = ""
    st.session_state.is_admin = False

def get_flag(team_name):
    drapeaux = {
        "mexique": "🇲🇽", "bresil": "🇧🇷", "france": "🇫🇷", "angleterre": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "portugal": "🇵🇹",
        "espagne": "🇪🇸", "allemagne": "🇩🇪", "argentine": "🇦🇷", "belgique": "🇧🇪", "croatie": "🇭🇷",
        "pays-bas": "🇳🇱", "japon": "🇯🇵", "suisse": "🇨🇭", "uruguay": "🇺🇾", "canada": "🇨🇦",
        "maroc": "🇲🇦", "senegal": "🇸🇳", "usa": "🇺🇸", "australie": "🇦🇺", "equateur": "🇪🇨",
        "ghana": "🇬🇭", "tunisie": "🇹🇳", "cameroun": "🇨🇲", "pologne": "🇵🇱", "danemark": "🇩🇰",
        "serbie": "🇷🇸", "coree du sud": "🇰🇷", "arabie saoudite": "🇸🇦", "iran": "🇮🇷", "mexico": "🇲🇽",
        "brasil": "🇧🇷", "england": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "germany": "🇩🇪", "argentina": "🇦🇷", "belgium": "🇧🇪"
    }
    return drapeaux.get(str(team_name).strip().lower(), "🏳️")

if "matchs" not in st.session_state:
    st.session_state.matchs = {
        "16es - Match 1": {"team1": "Allemagne", "flag1": "🇩🇪", "team2": "Paraguay", "flag2": "🇵🇾", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 2": {"team1": "France", "flag1": "🇫🇷", "team2": "Suède", "flag2": "🇸🇪", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 3": {"team1": "Afrique du Sud", "flag1": "🇿🇦", "team2": "Canada", "flag2": "🇨🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 4": {"team1": "Pays-Bas", "flag1": "🇳🇱", "team2": "Maroc", "flag2": "🇲🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 5": {"team1": "Brésil", "flag1": "🇧🇷", "team2": "Croatie", "flag2": "🇭🇷", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 6": {"team1": "Espagne", "flag1": "🇪🇸", "team2": "Japon", "flag2": "🇯🇵", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 7": {"team1": "USA", "flag1": "🇺🇸", "team2": "Bosnie", "flag2": "🇧🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 8": {"team1": "Belgique", "flag1": "🇧🇪", "team2": "Australie", "flag2": "🇦🇺", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 9": {"team1": "Mexique", "flag1": "🇲🇽", "team2": "Équateur", "flag2": "🇪🇨", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 10": {"team1": "Côte d'Ivoire", "flag1": "🇨🇮", "team2": "Norvège", "flag2": "🇳🇴", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 11": {"team1": "Argentine", "flag1": "🇦🇷", "team2": "Cap-Vert", "flag2": "🇨🇻", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 12": {"team1": "Angleterre", "flag1": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "team2": "Égypte", "flag2": "🇪🇬", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 13": {"team1": "Suisse", "flag1": "🇨🇭", "team2": "Portugal", "flag2": "🇵🇹", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 14": {"team1": "Uruguay", "flag1": "🇺🇾", "team2": "Ghana", "flag2": "🇬🇭", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 15": {"team1": "Sénégal", "flag1": "🇸🇳", "team2": "Tunisie", "flag2": "🇹🇳", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 16": {"team1": "Danemark", "flag1": "🇩🇰", "team2": "Corée du Sud", "flag2": "🇰🇷", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False}
    }

if "pronos" not in st.session_state: st.session_state.pronos = {}

# --- LÓGICA DE LOGIN ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align: center;'>🏆 LOBBY DES PRONOSTICS</h1>", unsafe_allow_html=True)
    email = st.text_input("Email").strip()
    nickname = st.text_input("Nickname").strip()
    code_salle = st.text_input("Código de Acesso", type="password")
    
    if st.button("🌟 Entrar", use_container_width=True):
        if code_salle == "LoungeCDM" and email and nickname:
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            st.session_state.user_nickname = nickname
            st.session_state.is_admin = (email.lower() == "ricardosdias32@gmail.com")
            if email not in st.session_state.pronos: st.session_state.pronos[email] = {"nickname_profile": nickname}
            st.rerun()
        else:
            st.error("Código incorreto ou campos vazios.")
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.user_nickname}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user_authenticated = False
        st.rerun()
    st.write("Bem-vindo! O sistema está pronto.")
