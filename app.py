import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Prono Mondial - Playoffs", page_icon="⚽", layout="wide")

# --- INITIALISATION CODES & JOUEURS ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# --- SYSTEME DE DRAPEAUX AUTOMATIQUE ---
def get_flag(team_name):
    drapeaux = {
        "france": "🇫🇷", "france ": "🇫🇷",
        "portugal": "🇵🇹", "portugal ": "🇵🇹",
        "angleterre": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "angleterre ": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "espagne": "🇪🇸", "espagne ": "🇪🇸",
        "allemagne": "🇩🇪", "allemagne ": "🇩🇪",
        "italie": "🇮🇹", "italie ": "🇮🇹",
        "argentine": "🇦🇷", "argentine ": "🇦🇷",
        "bresil": "🇧🇷", "brésil": "🇧🇷",
        "belgique": "🇧🇪", "pays-bas": "🇳🇱",
        "maroc": "🇲🇦", "croatie": "🇭🇷",
        "uruguay": "🇺🇾", "suisse": "🇨🇭",
        "senegal": "🇸🇳", "sénégal": "🇸🇳",
        "japon": "🇯🇵", "usa": "🇺🇸",
        "etats-unis": "🇺🇸", "mexique": "🇲🇽"
    }
    cleaned = str(team_name).strip().lower()
    return drapeaux.get(cleaned, "🏳️")

# --- STRUCTURE DES MATCHS (PRÉ-REMPLIE ET AUTOMATIQUE) ---
if "matchs" not in st.session_state:
    st.session_state.matchs = {
        # --- 8ÈMES DE FINALE ---
        "8ème 1": {"team1": "1er Groupe A", "flag1": "🏳️", "team2": "2ème Groupe B", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 1", "position_suivant": "team1"},
        "8ème 2": {"team1": "1er Groupe C", "flag1": "🏳️", "team2": "2ème Groupe D", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 1", "position_suivant": "team2"},
        "8ème 3": {"team1": "1er Groupe E", "flag1": "🏳️", "team2": "2ème Groupe F", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 2", "position_suivant": "team1"},
        "8ème 4": {"team1": "1er Groupe G", "flag1": "🏳️", "team2": "2ème Groupe H", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 2", "position_suivant": "team2"},
        "8ème 5": {"team1": "1er Groupe B", "flag1": "🏳️", "team2": "2ème Groupe A", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 3", "position_suivant": "team1"},
        "8ème 6": {"team1": "1er Groupe D", "flag1": "🏳️", "team2": "2ème Groupe C", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 3", "position_suivant": "team2"},
        "8ème 7": {"team1": "1er Groupe F", "flag1": "🏳️", "team2": "2ème Groupe E", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 4", "position_suivant": "team1"},
        "8ème 8": {"team1": "1er Groupe H", "flag1": "🏳️", "team2": "2ème Groupe G", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Quart 4", "position_suivant": "team2"},
        
        # --- QUARTS DE FINALE ---
        "Quart 1": {"team1": "Vainqueur 8ème 1", "flag1": "🏳️", "team2": "Vainqueur 8ème 2", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Demie 1", "position_suivant": "team1"},
        "Quart 2": {"team1": "Vainqueur 8ème 3", "flag1": "🏳️", "team2": "Vainqueur 8ème 4", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Demie 1", "position_suivant": "team2"},
        "Quart 3": {"team1": "Vainqueur 8ème 5", "flag1": "🏳️", "team2": "Vainqueur 8ème 6", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Demie 2", "position_suivant": "team1"},
        "Quart 4": {"team1": "Vainqueur 8ème 7", "flag1": "🏳️", "team2": "Vainqueur 8ème 8", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Demie 2", "position_suivant": "team2"},
        
        # --- DEMI-FINALES ---
        "Demie 1": {"team1": "Vainqueur Quart 1", "flag1": "🏳️", "team2": "Vainqueur Quart 2", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Finale", "position_suivant": "team1"},
        "Demie 2": {"team1": "Vainqueur Quart 3", "flag1": "🏳️", "team2": "Vainqueur Quart 4", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": "Finale", "position_suivant": "team2"},
        
        # --- FINALE ---
        "Finale": {"team1": "Vainqueur Demie 1", "flag1": "🏳️", "team2": "Vainqueur Demie 2", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "suivant": None, "position_suivant": None},
    }

if "pronos" not in st.session_state:
    st.session_state.pronos = {}

st.title("⚽ Application de Pronostics - Playoffs")

if not st.session_state.user_authenticated:
    st.subheader("Connexion à la Salle de Jeu")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Adresse Email")
        password = st.text_input("Mot de passe", type="password")
    with col2:
        code_salle = st.text_input("Code de la Salle (Ex: LoungeCDM)")
    
    if st.button("Se connecter / Rejoindre"):
        if code_salle == "LoungeCDM" and email: 
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            if email.lower() == "ricardosdias32@gmail.com": 
                st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("Code de salle ou email invalide.")
else:
    st.sidebar.write(f"👤 Connecté: **{st.session_state.user_email}**")
    if st.session_state.is_admin:
        st.sidebar.success("👑 Mode Admin Actif")
    
    if st.sidebar.button("Se déconnecter"):
        st.session_state.user_authenticated = False
        st.rerun()

    # --- PANNEAU ADMIN ---
    if st.session_state.is_admin:
        st.header("🛠️ Panneau Administrateur")
        
        st.subheader("1. Définir les vraies équipes (Les Drapeaux sont automatiques !)")
        match_to_mod = st.selectbox("Sélectionner le match des 8èmes à actualiser", [m for m in st.session_state.matchs.keys() if "8ème" in m])
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            t1 = st.text_input("Nom Équipe 1", st.session_state.matchs[match_to_mod]["team1"])
        with col_m2:
            t2 = st.text_input("Nom Équipe 2", st.session_state.matchs[match_to_mod]["team2"])
            
        if st.button("Enregistrer les équipes"):
            st.session_state.matchs[match_to_mod]["team1"] = t1
            st.session_state.matchs[match_to_mod]["flag1"] = get_flag(t1)
            st.session_state.matchs[match_to_mod]["team2"] = t2
            st.session_state.matchs[match_to_mod]["flag2"] = get_flag(t2)
            st.success(f"Équipes enregistrées ! Drapeaux générés automatiquement.")
            st.rerun()

        st.write("---")
        
        st.subheader("2. Entrer le score officiel de la rencontre")
        match_to_score = st.selectbox("Sélectionner le match joué", list(st.session_state.matchs.keys()), key="score_box")
        m_data = st.session_state.matchs[match_to_score]
        
        if not m_data["termine"]:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                sc1 = st.number_input(f"Score {m_data['team1']}", min_value=0, step=1, key="sc1_admin")
            with col_b:
                sc2 = st.number_input(f"Score {m_data['team2']}", min_value=0, step=1, key="sc2_admin")
            with col_c:
                qualif_officiel = st.selectbox("Qui passe au tour suivant ?", [m_data['team1'], m_data['team2']])
                
            if st.button("Valider le résultat final"):
                st.session_state.matchs[match_to_score]["score1_reel"] = sc1
                st.session_state.matchs[match_to_score]["score2_reel"] = sc2
                st.session_state.matchs[match_to_score]["qualifie_reel"] = qualif_officiel
                st.session_state.matchs[match_to_score]["termine"] = True
                
                suiv = m_data["suivant"]
                pos = m_data["position_suivant"]
                if suiv and suiv in st.session_state.matchs:
                    st.session_state.matchs[suiv][pos] = qualif_officiel
                    if qualif_officiel == m_data["team1"]:
                        st.session_state.matchs[suiv]["flag" + pos[-1]] = m_data["flag1"]
                    else:
                        st.session_state.matchs[suiv]["flag" + pos[-1]] = m_data["flag2"]
                
                st.success("Match validé ! L'équipe avance dans l'arbre.")
                st.rerun()
        st.write("---")

    # --- ESPACE JOUEUR ---
    st.header("📝 Vos Pronostics (Playoffs)")
    user = st.session_state.user_email
    if user not in st.session_state.pronos:
        st.session_state.pronos[user] = {}

    for match_id, info in st.session_state.matchs.items():
        st.subheader(f"➔ {match_id}")
        deja_valide = st.session_state.pronos[user].get(match_id, {}).get("valide", False)
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.markdown(f"### {info['flag1']} {info['team1']}")
        with col2:
            if deja_valide: st.write(f"Score: **{st.session_state.pronos[user][match_id]['score1']}**")
            else: score1_input = st.number_input("Score 1", min_value=0, step=1, key=f"s1_{match_id}", label_visibility="collapsed")
        with col3:
            if deja_valide: st.write(f"Score: **{st.session_state.pronos[user][match_id]['score2']}**")
            else: score2_input = st.number_input("Score 2", min_value=0, step=1, key=f"s2_{match_id}", label_visibility="collapsed")
        with col4:
            st.markdown(f"### {info['team2']} {info['flag2']}")
            
        options_qualif = [info['team1'], info['team2']]
        if deja_valide:
            st.write(f"Qualifié choisi: **{st.session_state.pronos[user][match_id]['qualifie']}**")
            st.warning("🔒 Verrouillé")
        else:
            qualif_input = st.radio("Qui se qualifie ?", options_qualif, key=f"q_{match_id}", horizontal=True)
            if st.button("Valider le prono", key=f"btn_{match_id}"):
                st.session_state.pronos[user][match_id] = {"score1": score1_input, "score2": score2_input, "qualifie": qualif_input, "valide": True}
                st.rerun()
        st.write("---")
