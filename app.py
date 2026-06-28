import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Prono Mondial - Playoffs", page_icon="⚽", layout="wide")

# --- STYLES VISUELS PERSONNALISÉS (CSS) ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .match-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #3b82f6;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .admin-box {
        background-color: #0f172a;
        padding: 20px;
        border-radius: 12px;
        border: 2px dashed #ef4444;
        margin-bottom: 30px;
    }
    .vs-text {
        font-size: 20px;
        font-weight: bold;
        color: #94a3b8;
        text-align: center;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION SESSION STATE ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.user_email = ""
    st.session_state.is_admin = False

# --- DÉTECTEUR AUTOMATIQUE DE DRAPEAUX ---
def get_flag(team_name):
    drapeaux = {
        "allemagne": "🇩🇪", "alemanha": "🇩🇪", "paraguay": "🇵🇾", "france": "🇫🇷", "frança": "🇫🇷", 
        "suède": "🇸🇪", "suede": "🇸🇪", "suécia": "🇸🇪", "afrique du sud": "🇿🇦", "afrika do sul": "🇿🇦", 
        "canada": "🇨🇦", "canadá": "🇨🇦", "pays-bas": "🇳🇱", "paises baixos": "🇳🇱", "maroc": "🇲🇦", "marrocos": "🇲🇦",
        "croatie": "🇭🇷", "croácia": "🇭🇷", "espagne": "🇪🇸", "espanha": "🇪🇸", "usa": "🇺🇸", "états-unis": "🇺🇸", "eua": "🇺🇸",
        "bosnie": "🇧🇦", "bósnia": "🇧🇦", "belgique": "🇧🇪", "bélgica": "🇧🇪", "brésil": "🇧🇷", "brasil": "🇧🇷", 
        "japon": "🇯🇵", "japão": "🇯🇵", "côte d'ivoire": "🇨🇮", "norvège": "🇳🇴", "noruega": "🇳🇴", 
        "mexique": "🇲🇽", "méxico": "🇲🇽", "équateur": "🇪🇨", "equador": "🇪🇨", "angleterre": "🏴󠁧󠁢󠁥󠁮ッグ󠁿", "inglaterra": "🏴󠁧󠁢󠁥󠁮ッグ󠁿",
        "argentine": "🇦🇷", "argentina": "🇦🇷", "cap-vert": "🇨🇻", "cabo verde": "🇨🇻", "australie": "🇦🇺", "austrália": "🇦🇺",
        "égypte": "🇪🇬", "egito": "🇪🇬", "suisse": "🇨🇭", "suiça": "🇨🇭", "ghana": "🇬🇭", "gana": "🇬🇭",
        "colombie": "🇨🇴", "colômbia": "🇨🇴", "portugal": "🇵🇹"
    }
    cleaned = str(team_name).strip().lower()
    return drapeaux.get(cleaned, "🏳️")

if "matchs" not in st.session_state:
    st.session_state.matchs = {
        "16es - Match 1": {"team1": "Allemagne", "flag1": "🇩🇪", "team2": "Paraguay", "flag2": "🇵🇾", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 2": {"team1": "France", "flag1": "🇫🇷", "team2": "Suède", "flag2": "🇸🇪", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 3": {"team1": "Afrique du Sud", "flag1": "🇿🇦", "team2": "Canada", "flag2": "🇨🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 4": {"team1": "Pays-Bas", "flag1": "🇳🇱", "team2": "Maroc", "flag2": "🇲🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 5": {"team1": "À Définir (K2)", "flag1": "🏳️", "team2": "Croatie", "flag2": "🇭🇷", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 6": {"team1": "Espagne", "flag1": "🇪🇸", "team2": "À Définir (J2)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 7": {"team1": "USA", "flag1": "🇺🇸", "team2": "Bosnie", "flag2": "🇧🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 8": {"team1": "Belgique", "flag1": "🇧🇪", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 9": {"team1": "Brésil", "flag1": "🇧🇷", "team2": "Japon", "flag2": "🇯🇵", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 10": {"team1": "Côte d'Ivoire", "flag1": "🇨🇮", "team2": "Norvège", "flag2": "🇳🇴", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 11": {"team1": "Mexique", "flag1": "🇲🇽", "team2": "Équateur", "flag2": "🇪🇨", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 12": {"team1": "Angleterre", "flag1": "🏴󠁧󠁢󠁥󠁮ッグ󠁿", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 13": {"team1": "Argentine", "flag1": "🇦🇷", "team2": "Cap-Vert", "flag2": "🇨🇻", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 14": {"team1": "Australie", "flag1": "🇦🇺", "team2": "Égypte", "flag2": "🇪🇬", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 15": {"team1": "Suisse", "flag1": "🇨🇭", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
        "16es - Match 16": {"team1": "À Définir (K1)", "flag1": "🏳️", "team2": "Ghana", "flag2": "🇬🇭", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "", "termine": False},
    }

if "pronos" not in st.session_state: 
    st.session_state.pronos = {}

# --- FONCTION DE CALCUL DES POINTS DU CLASSEMENT ---
def calculer_classement():
    scores = {}
    for user, user_pronos in st.session_state.pronos.items():
        total_points = 0
        for match_id, info in st.session_state.matchs.items():
            if info["termine"] and match_id in user_pronos:
                prono = user_pronos[match_id]
                if prono.get("valide", False):
                    # 1. Score Exact -> 3 Points
                    if prono["score1"] == info["score1_reel"] and prono["score2"] == info["score2_reel"]:
                        total_points += 3
                    # 2. Seulement le bon qualifié -> 1 Point
                    elif prono["qualifie"] == info["qualifie_reel"]:
                        total_points += 1
        scores[user] = total_points
    return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))


# --- ÉCRAN DE CONNEXION (LOGIN) ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🏆 LOBBY DES PRONOSTICS 🏆</h1>", unsafe_allow_html=True)
    st.subheader("🔑 Accéder à la Salle")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Votre adresse Email", key="login_email_unique")
    with col2: 
        code_salle = st.text_input("Code de la Salle (Ex: LoungeCDM)", key="login_sala_unique")
    
    if st.button("🌟 Entrer", key="btn_login_submit", use_container_width=True):
        if code_salle == "LoungeCDM" and email: 
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            if email.lower() == "ricardosdias32@gmail.com": 
                st.session_state.is_admin = True
            st.success("Connexion réussie ! Chargement...")
            st.rerun()
        else: 
            st.error("Code de salle ou email incorrect.")
else:
    # --- BARRE LATÉRALE (NAVIGATION & PROFIL) ---
    st.sidebar.markdown(f"### 👤 Joueur:\n**{st.session_state.user_email}**")
    if st.session_state.is_admin: 
        st.sidebar.error("👑 MODE ADMIN ACTIF")
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Menu")
    
    # Menu de navigation principal
    options_menu = ["⚽ Mes Pronostics", "📊 Classement"]
    if st.session_state.is_admin:
        options_menu.append("🛠️ Zone Admin (Résultats)")
        
    choix_menu = st.sidebar.radio("Aller vers :", options_menu, key="menu_navigation")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Déconnexion", key="btn_logout_sidebar", use_container_width=True):
        st.session_state.user_authenticated = False
        st.session_state.user_email = ""
        st.session_state.is_admin = False
        st.rerun()

    # --- SECTION 1: PRONOSTICS ---
    if choix_menu == "⚽ Mes Pronostics":
        st.markdown("<h1 style='color: #3b82f6;'>⚽ Vos Pronostics</h1>", unsafe_allow_html=True)
        user = st.session_state.user_email
        if user not in st.session_state.pronos: 
            st.session_state.pronos[user] = {}

        for match_id, info in st.session_state.matchs.items():
            st.markdown(f"<div class='match-box'>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: #3b82f6; font-weight: bold;'>{match_id}</span>", unsafe_allow_html=True)
            
            if info["termine"]:
                st.markdown(f"<span style='color: #ef4444; float: right; font-weight: bold;'>🔴 MATCH TERMINÉ (Score Officiel: {info['score1_reel']} - {info['score2_reel']})</span>", unsafe_allow_html=True)
                deja_valide = True
            else:
                deja_valide = st.session_state.pronos[user].get(match_id, {}).get("valide", False)
                
            col1, col_vs, col2 = st.columns([3, 2, 3])
            
            with col1:
                st.markdown(f"<h3 style='text-align: center;'>{info['flag1']}<br>{info['team1']}</h3>", unsafe_allow_html=True)
                if not deja_valide: s1_in = st.number_input("Buts", min_value=0, step=1, key=f"s1_{match_id}")
                else: 
                    user_score1 = st.session_state.pronos[user].get(match_id, {}).get("score1", 0)
                    st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>{user_score1}</b></p>", unsafe_allow_html=True)
                    
            with col_vs: st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"<h3 style='text-align: center;'>{info['flag2']}<br>{info['team2']}</h3>", unsafe_allow_html=True)
                if not deja_valide: s2_in = st.number_input("Buts", min_value=0, step=1, key=f"s2_{match_id}")
                else: 
                    user_score2 = st.session_state.pronos[user].get(match_id, {}).get("score2", 0)
                    st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>{user_score2}</b></p>", unsafe_allow_html=True)
            
            st.markdown("<p style='margin-top: 15px; color: #94a3b8;'>🎯 Qui se qualifie ?</p>", unsafe_allow_html=True)
            options_q = [info['team1'], info['team2']]
            
            if not deja_valide:
                q_in = st.radio("Qualifié", options_q, key=f"q_{match_id}", horizontal=True, label_visibility="collapsed")
                if st.button(f"🔒 Valider mon prono ({match_id})", key=f"btn_{match_id}", use_container_width=True):
                    st.session_state.pronos[user][match_id] = {"score1": s1_in, "score2": s2_in, "qualifie": q_in, "valide": True}
                    st.toast("Prono enregistré ! 🔥")
                    st.rerun()
            else:
                user_q = st.session_state.pronos[user].get(match_id, {}).get("qualifie", "Aucun")
                if info["termine"]:
                    st.markdown(f"<p style='color: #64748b;'><b>Votre choix de qualifié :</b> {user_q}</p>", unsafe_allow_html=True)
                    st.markdown("<span style='color: #ef4444;'>🔒 Pronostics verrouillés par l'Admin</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: #10b981;'><b>✓ Votre choix :</b> {user_q}</p>", unsafe_allow_html=True)
                    st.markdown("<span style='color: #64748b;'>🔒 Verrouillé (En attente du résultat)</span>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

    # --- SECTION 2: CLASSEMENT ---
    elif choix_menu == "📊 Classement":
        st.markdown("<h1 style='color: #f59e0b;'>📊 Classement Général</h1>", unsafe_allow_html=True)
        st.write("Barème : **3 pts** pour le score exact | **1 pt** pour le bon qualifié trouvé.")
        
        classement_data = calculer_classement()
        
        if not classement_data:
            st.info("Aucun point n'a encore été distribué. Les matchs doivent être terminés par l'Admin.")
        else:
            st.markdown("<table style='width:100%; border-collapse: collapse; text-align:left;'>", unsafe_allow_html=True)
            st.markdown("<tr style='background-color:#1e293b; color:white;'><th>Rang</th><th>Joueur</th><th>Points Régalés</th></tr>", unsafe_allow_html=True)
            
            for index, (player, points) in enumerate(classement_data.items(), start=1):
                bg_color = "#0f172a" if index % 2 == 0 else "#1e293b"
                badge = "🥇 " if index == 1 else "🥈 " if index == 2 else "🥉 " if index == 3 else f"{index} "
                st.markdown(f"<tr style='background-color:{bg_color}; color:white;'><td><b>{badge}</b></td><td>{player}</td><td><b>{points} pts</b></td></tr>", unsafe_allow_html=True)
            
            st.markdown("</table>", unsafe_allow_html=True)

    # --- SECTION 3: ZONE ADMIN (CORRIGÉE CI-DESSOUS) ---
    elif choix_menu == "🛠️ Zone Admin (Résultats)" and st.session_state.is_admin:
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
        
        # CORREÇÃO DAQUI: st.title em vez de st.h1
        st.title("🛠️ Panneau de Contrôle Administrateur")
        
        opcao_admin = st.radio("Action à réaliser :", ["Modifier l'affiche d'un match", "Enregistrer un Résultat Réel"], horizontal=True, key="admin_mode_choice")
        
        match_to_mod = st.selectbox("Sélectionner le Match :", list(st.session_state.matchs.keys()), key="admin_select_match")
        
        if opcao_admin == "Modifier l'affiche d'un match":
            col_m1, col_m2 = st.columns(2)
            with col_m1: t1 = st.text_input("Nouvelle Équipe 1", st.session_state.matchs[match_to_mod]["team1"], key="admin_t1")
            with col_m2: t2 = st.text_input("Nouvelle Équipe 2", st.session_state.matchs[match_to_mod]["team2"], key="admin_t2")
                
            if st.button("💾 Mettre à jour l'affiche", key="btn_admin_save_teams", use_container_width=True):
                st.session_state.matchs[match_to_mod]["team1"] = t1
                st.session_state.matchs[match_to_mod]["flag1"] = get_flag(t1)
                st.session_state.matchs[match_to_mod]["team2"] = t2
                st.session_state.matchs[match_to_mod]["flag2"] = get_flag(t2)
                st.success("Match mis à jour avec succès !")
                st.rerun()
                
        elif opcao_admin == "Enregistrer un Résultat Réel":
            st.write(f"Entrez le score final officiel pour le match : **{st.session_state.matchs[match_to_mod]['team1']}** vs **{st.session_state.matchs[match_to_mod]['team2']}**")
            col_r1, col_r2 = st.columns(2)
            with col_r1: res1 = st.number_input(f"Buts pour {st.session_state.matchs[match_to_mod]['team1']}", min_value=0, step=1, value=int(st.session_state.matchs[match_to_mod]["score1_reel"]), key="admin_res1")
            with col_r2: res2 = st.number_input(f"Buts pour {st.session_state.matchs[match_to_mod]['team2']}", min_value=0, step=1, value=int(st.session_state.matchs[match_to_mod]["score2_reel"]), key="admin_res2")
            
            options_qualifie_reel = [st.session_state.matchs[match_to_mod]['team1'], st.session_state.matchs[match_to_mod]['team2']]
            index_defaut = 0 if st.session_state.matchs[match_to_mod]["qualifie_reel"] == options_qualifie_reel[0] else 1
            qualifie_reel_input = st.radio("Qui s'est officiellement qualifié ?", options_qualifie_reel, index=index_defaut, key="admin_qual_reel")
            
            terminar_jogo = st.checkbox("Clôturer le match (Calcule les points et bloque les pronos)", value=st.session_state.matchs[match_to_mod]["termine"], key="admin_close_match")
            
            if st.button("🏆 Enregistrer le Résultat Officiel", key="btn_admin_save_results", use_container_width=True):
                st.session_state.matchs[match_to_mod]["score1_reel"] = res1
                st.session_state.matchs[match_to_mod]["score2_reel"] = res2
                st.session_state.matchs[match_to_mod]["qualifie_reel"] = qualifie_reel_input
                st.session_state.matchs[match_to_mod]["termine"] = terminar_jogo
                st.success("Résultat enregistré ! Classement mis à jour.")
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)
