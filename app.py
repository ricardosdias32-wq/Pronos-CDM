import streamlit as st
import unicodedata

# --- CONFIGURATION ---
st.set_page_config(page_title="Prono Mondial 2026", page_icon="🏆", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0a1128; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    .hero-banner { background: linear-gradient(135deg, #0a1128, #1b2f5e); padding: 30px; border-radius: 18px; text-align: center; border: 1px solid #2a3b6e; }
    .match-box { background: #131c33; padding: 15px; border-radius: 12px; border-left: 4px solid #e8c34a; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- FONCTION BANDEIRAS ---
def get_flag(name):
    drapeaux = {"allemagne":"🇩🇪", "france":"🇫🇷", "portugal":"🇵🇹", "bresil":"🇧🇷", "espagne":"🇪🇸", "angleterre":"🏴󠁧󠁢󠁥󠁮󠁧󠁿", "argentine":"🇦🇷", "belgique":"🇧🇪", "suisse":"🇨🇭", "colombie":"🇨🇴", "mexique":"🇲🇽", "canada":"🇨🇦", "pays-bas":"🇳🇱", "maroc":"🇲🇦", "croatie":"🇭🇷", "autriche":"🇦🇹", "usa":"🇺🇸", "bosnie":"🇧🇦", "senegal":"🇸🇳", "japon":"🇯🇵", "cote d'ivoire":"🇨🇮", "norvege":"🇳🇴", "equateur":"🇪🇨", "rd congo":"🇨🇩", "cap-vert":"🇨🇻", "australie":"🇦🇺", "egypte":"🇪🇬", "algerie":"🇩🇿", "ghana":"🇬🇭", "suede":"🇸🇪", "paraguay":"🇵🇾", "afrique du sud":"🇿🇦"}
    return drapeaux.get("".join(c for c in unicodedata.normalize('NFD', str(name).lower()) if unicodedata.category(c) != 'Mn'), "🏳️")

# --- INITIALISATION ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.pronos = {}
    # Structure complète des matchs
    st.session_state.matchs = {
        f"16es - Match {i+1}": {"team1": t1, "team2": t2, "score1_reel": 0, "score2_reel": 0, "termine": False}
        for i, (t1, t2) in enumerate([("Allemagne", "Paraguay"), ("France", "Suède"), ("Afrique du Sud", "Canada"), ("Pays-Bas", "Maroc"), 
        ("Portugal", "Croatie"), ("Espagne", "Autriche"), ("USA", "Bosnie"), ("Belgique", "Sénégal"), ("Brésil", "Japon"), 
        ("Côte d'Ivoire", "Norvège"), ("Mexique", "Équateur"), ("Angleterre", "RD Congo"), ("Argentine", "Cap-Vert"), 
        ("Australie", "Égypte"), ("Suisse", "Algérie"), ("Colombie", "Ghana")])
    }

# --- LOGIN ---
if not st.session_state.user_authenticated:
    st.markdown("<div class='hero-banner'><h1>🏆 COUPE DU MONDE 2026</h1><p>Pronostics & Classement</p></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Adresse Email")
        nick = st.text_input("Pseudo")
        code = st.text_input("Code de la Salle", type="password")
        if st.button("Entrer"):
            if code == "LoungeCDM":
                st.session_state.user_authenticated = True
                st.session_state.user_email = email
                st.session_state.user_nickname = nick
                st.rerun()
else:
    st.sidebar.title(f"👤 {st.session_state.user_nickname}")
    menu = st.sidebar.radio("Navigation", ["⚽ Mes Pronostics", "🌳 Arbre des Playoffs", "🛠️ Administration", "🚪 Déconnexion"])

    if menu == "⚽ Mes Pronostics":
        st.title("⚽ Mes Pronostics")
        for mid, info in st.session_state.matchs.items():
            st.markdown(f"<div class='match-box'><b>{mid}</b> | {get_flag(info['team1'])} {info['team1']} vs {get_flag(info['team2'])} {info['team2']}</div>", unsafe_allow_html=True)

    elif menu == "🌳 Arbre des Playoffs":
        st.title("🌳 Arbre des Playoffs")
        st.write("Résultats officiels des matchs :")
        for mid, info in st.session_state.matchs.items():
            if info["termine"]:
                st.write(f"✅ {mid} : {info['team1']} {info['score1_reel']} - {info['score2_reel']} {info['team2']}")
            else:
                st.write(f"⏳ {mid} : {info['team1']} vs {info['team2']} (En attente)")

    elif menu == "🛠️ Administration":
        # ALTERE AQUI O TEU EMAIL
        if st.session_state.user_email == "ricardosdias32@gmail.com":
            st.title("🛠️ Panneau Administrateur")
            mid = st.selectbox("Sélectionner un match à mettre à jour :", list(st.session_state.matchs.keys()))
            res1 = st.number_input(f"Score {st.session_state.matchs[mid]['team1']}", 0)
            res2 = st.number_input(f"Score {st.session_state.matchs[mid]['team2']}", 0)
            if st.button("Valider résultat"):
                st.session_state.matchs[mid]["score1_reel"] = res1
                st.session_state.matchs[mid]["score2_reel"] = res2
                st.session_state.matchs[mid]["termine"] = True
                st.success("Résultat enregistré avec succès !")
        else:
            st.error("Accès refusé.")

    elif menu == "🚪 Déconnexion":
        st.session_state.user_authenticated = False
        st.rerun()
