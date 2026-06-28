import streamlit as st
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Prono Mondial - Pro Edition", page_icon="🏆", layout="wide")

# --- STYLES VISUELS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    .kpi-box { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #4c1d95; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .match-box { background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 6px solid #3b82f6; margin-bottom: 20px; }
    .tree-box { background-color: #0f172a; padding: 12px; border-radius: 8px; border: 1px solid #334155; color: #e2e8f0; margin-bottom: 15px; font-size: 14px; }
    .vs-text { font-size: 22px; font-weight: bold; color: #94a3b8; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION SESSION STATE ---
if "user_authenticated" not in st.session_state:
    st.session_state.update({"user_authenticated": False, "user_email": "", "user_nickname": "", "is_admin": False})

if "pronos" not in st.session_state: st.session_state.pronos = {}

# --- FUNÇÕES ---
def get_flag(team_name):
    drapeaux = {
        "mexique": "🇲🇽", "mexico": "🇲🇽", "afrique du sud": "🇿🇦", "brasil": "🇧🇷", "portugal": "🇵🇹",
        "france": "🇫🇷", "suede": "🇸🇪", "allemagne": "🇩🇪", "paraguay": "🇵🇾", "canada": "🇨🇦",
        "pays-bas": "🇳🇱", "maroc": "🇲🇦", "croatie": "🇭🇷", "espagne": "🇪🇸", "usa": "🇺🇸",
        "bosnie": "🇧🇦", "belgique": "🇧🇪", "japon": "🇯🇵", "cote d'ivoire": "🇨🇮", "norvege": "🇳🇴",
        "equateur": "🇪🇨", "angleterre": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "argentine": "🇦🇷", "cap-vert": "🇨🇻",
        "australie": "🇦🇺", "egypte": "🇪🇬", "suisse": "🇨🇭", "ghana": "🇬🇭", "colombie": "🇨🇴", "autriche": "🇦🇹"
    }
    text = "".join(c for c in unicodedata.normalize('NFD', str(team_name).lower()) if unicodedata.category(c) != 'Mn')
    return drapeaux.get(text, "🏳️")

def calculer_classement():
    scores = {}
    for user_email, user_pronos in st.session_state.pronos.items():
        nickname = user_pronos.get("nickname_profile", user_email)
        total_points = 0
        for match_id, info in st.session_state.matchs.items():
            if info.get("termine") and match_id in user_pronos:
                prono = user_pronos[match_id]
                if isinstance(prono, dict) and prono.get("valide"):
                    if prono["score1"] == info["score1_reel"] and prono["score2"] == info["score2_reel"]: total_points += 3
                    elif prono["qualifie"] == info["qualifie_reel"]: total_points += 1
        scores[nickname] = total_points
    return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

# --- GESTÃO DE MATCHS (LOGICA OMITIDA PARA BREVIDADE, INSERIR A TUA ORIGINAL AQUI) ---
if "matchs" not in st.session_state:
    st.session_state.matchs = {f"16es - Match {i}": {"team1": "À Définir", "team2": "À Définir", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False} for i in range(1, 17)}

# --- INTERFACE ---
if not st.session_state.user_authenticated:
    st.title("🏆 LOBBY")
    email = st.text_input("Email")
    nickname = st.text_input("Nickname")
    if st.button("Entrar"):
        st.session_state.update({"user_authenticated": True, "user_email": email, "user_nickname": nickname, "is_admin": (email == "ricardosdias32@gmail.com")})
        st.rerun()
else:
    menu = st.sidebar.radio("Menu", ["⚽ Mes Pronostics", "📊 Classement", "🛠️ Zone Admin"])
    if st.sidebar.button("🚪 Déconnexion"):
        st.session_state.clear()
        st.rerun()

    if menu == "⚽ Mes Pronostics":
        st.write(f"Bem-vindo {st.session_state.user_nickname}")
        # Lógica dos teus jogos aqui...
        
    elif menu == "📊 Classement":
        st.header("📊 Classement")
        classement = calculer_classement() # AQUI ESTÁ A CORREÇÃO
        st.table(classement)

    elif menu == "🛠️ Zone Admin" and st.session_state.is_admin:
        st.header("Admin")
        # Lógica de admin...
