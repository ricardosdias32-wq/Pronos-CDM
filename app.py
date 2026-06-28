import streamlit as st
import unicodedata

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
    .tree-box {
        background-color: #0f172a;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #334155;
        font-family: sans-serif;
        color: #e2e8f0;
        margin-bottom: 15px;
        font-size: 14px;
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
    st.session_state.user_nickname = ""
    st.session_state.is_admin = False

# --- DÉTECTEUR DE DRAPEAUX (ANTI-ERREUR ET SANS ACCENTS) ---
def get_flag(team_name):
    drapeaux = {
        # GRUPO A
        "mexique": "🇲🇽", "mexico": "🇲🇽",
        "afrique du sud": "🇿🇦", "afrika du sul": "🇿🇦", "africa du sul": "🇿🇦", "africa do sul": "🇿🇦",
        "coree du sud": "🇰🇷", "coreia do sul": "🇰🇷", "south korea": "🇰🇷",
        "tchequie": "🇨🇿", "republique cheque": "🇨🇿", "republica checa": "🇨🇿", "czechia": "🇨🇿",

        # GRUPO B
        "canada": "🇨🇦",
        "suisse": "🇨🇭", "suica": "🇨🇭",
        "qatar": "🇶🇦", "catar": "🇶🇦",
        "bosnie": "🇧🇦", "bosnia": "🇧🇦", "bosnie et herzegovine": "🇧🇦", "bosnia and herzegovina": "🇧🇦",

        # GRUPO C
        "bresil": "🇧🇷", "brasil": "🇧🇷", "brazil": "🇧🇷",
        "maroc": "🇲🇦", "marrocos": "🇲🇦", "morocco": "🇲🇦",
        "ecosse": "🏴󠁧󠁢󠁳󠁿", "escoscia": "🏴󠁧󠁢󠁳󠁿", "escocia": "🏴󠁧󠁢󠁳󠁿", "scotland": "🏴󠁧󠁢󠁳󠁿",
        "haiti": "🇭🇹",

        # GRUPO D
        "usa": "🇺🇸", "etats-unis": "🇺🇸", "eua": "🇺🇸", "united states": "🇺🇸",
        "paraguay": "🇵🇾", "paraguai": "🇵🇾",
        "australie": "🇦🇺", "australia": "🇦🇺",
        "turquie": "🇹🇷", "turquia": "🇹🇷", "turkey": "🇹🇷",

        # GRUPO E
        "allemagne": "🇩🇪", "alemanha": "🇩🇪", "germany": "🇩🇪",
        "equateur": "🇪🇨", "equador": "🇪🇨", "ecuador": "🇪🇨",
        "cote d'ivoire": "🇨🇮", "costa do marfim": "🇨🇮", "ivory coast": "🇨🇮",
        "curacao": "🇨🇼",

        # GRUPO F
        "pays-bas": "🇳🇱", "paises baixos": "🇳🇱", "netherlands": "🇳🇱",
        "japon": "🇯🇵", "japao": "🇯🇵", "japan": "🇯🇵",
        "suede": "🇸🇪", "suecia": "🇸🇪", "sweden": "🇸🇪",
        "tunisie": "🇹🇳", "tunisia": "🇹🇳",

        # GRUPO G
        "belgique": "🇧🇪", "belgica": "🇧🇪", "belgium": "🇧🇪",
        "egypte": "🇪🇬", "egito": "🇪🇬", "egypt": "🇪🇬",
        "iran": "🇮🇷", "irao": "🇮🇷",
        "nouvelle-zelande": "🇳🇿", "nova zelandia": "🇳🇿", "new zealand": "🇳🇿",

        # GRUPO H
        "espagne": "🇪🇸", "espanha": "🇪🇸", "spain": "🇪🇸",
        "uruguay": "🇺🇾", "uruguaio": "🇺🇾", "uruguai": "🇺🇾",
        "arabie saoudite": "🇸🇦", "arabia saudita": "🇸🇦", "saudi arabia": "🇸🇦",
        "cap-vert": "🇨🇻", "cabo verde": "🇨🇻",

        # GRUPO I
        "france": "🇫🇷", "franca": "🇫🇷",
        "senegal": "🇸🇳",
        "norvege": "🇳🇴", "noruega": "🇳🇴", "norway": "🇳🇴",
        "iraq": "🇮🇶", "iraque": "🇮🇶",

        # GRUPO J
        "argentine": "🇦🇷", "argentina": "🇦🇷",
        "autriche": "🇦🇹", "austria": "🇦🇹",
        "algerie": "🇩🇿", "algeria": "🇩🇿",
        "jordanie": "🇯🇴", "jordania": "🇯🇴", "jordan": "🇯🇴",

        # GRUPO K
        "portugal": "🇵🇹",
        "colombie": "🇨🇴", "colombia": "🇨🇴",
        "rd congo": "🇨🇩", "congo dr": "🇨🇩", "dr congo": "🇨🇩", "congo drc": "🇨🇩",
        "ouzbekistan": "🇺🇿", "uzbequistao": "🇺🇿", "uzbekistan": "🇺🇿",

        # GRUPO L
        "angleterre": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "england": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "croatie": "🇭🇷", "croacia": "🇭🇷", "croatia": "🇭🇷",
        "ghana": "🇬🇭", "gana": "🇬🇭",
        "panama": "🇵🇦"
    }
    
    # Remove acentos, passa para minúsculas e limpa espaços extras
    text = str(team_name).strip().lower()
    text = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    
    return drapeaux.get(text, "🏳️")

# --- BASE DE DONNÉES DES MATCHS ---
if "matchs" not in st.session_state:
    st.session_state.matchs = {
        "16es - Match 1": {"team1": "Allemagne", "flag1": "🇩🇪", "team2": "Paraguay", "flag2": "🇵🇾", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 2": {"team1": "France", "flag1": "🇫🇷", "team2": "Suède", "flag2": "🇸🇪", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 3": {"team1": "Afrique du Sud", "flag1": "🇿🇦", "team2": "Canada", "flag2": "🇨🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 4": {"team1": "Pays-Bas", "flag1": "🇳🇱", "team2": "Maroc", "flag2": "🇲🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 5": {"team1": "À Définir (K2)", "flag1": "🏳️", "team2": "Croatie", "flag2": "🇭🇷", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 6": {"team1": "Espagne", "flag1": "🇪🇸", "team2": "À Définir (J2)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 7": {"team1": "USA", "flag1": "🇺🇸", "team2": "Bosnie", "flag2": "🇧🇦", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 8": {"team1": "Belgique", "flag1": "🇧🇪", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 9": {"team1": "Brésil", "flag1": "🇧🇷", "team2": "Japon", "flag2": "🇯🇵", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 10": {"team1": "Côte d'Ivoire", "flag1": "🇨🇮", "team2": "Norvège", "flag2": "🇳🇴", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 11": {"team1": "Mexique", "flag1": "🇲🇽", "team2": "Équateur", "flag2": "🇪🇨", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 12": {"team1": "Angleterre", "flag1": "🏴󠁧󠁢󠁥󠁮ッグ󠁿", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 13": {"team1": "Argentine", "flag1": "🇦🇷", "team2": "Cap-Vert", "flag2": "🇨🇻", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 14": {"team1": "Australie", "flag1": "🇦🇺", "team2": "Égypte", "flag2": "🇪🇬", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 15": {"team1": "Suisse", "flag1": "🇨🇭", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 16": {"team1": "À Définir (K1)", "flag1": "🏳️", "team2": "Ghana", "flag2": "🇬🇭", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
    }

if "pronos" not in st.session_state: 
    st.session_state.pronos = {}

# --- DÉDUCTION DYNAMIQUE DES HUITIÈMES ---
m_data = st.session_state.matchs
huitiemes = {
    "H8 - Match 1": {"t1": m_data["16es - Match 1"]["qualifie_reel"], "t2": m_data["16es - Match 2"]["qualifie_reel"]},
    "H8 - Match 2": {"t1": m_data["16es - Match 3"]["qualifie_reel"], "t2": m_data["16es - Match 4"]["qualifie_reel"]},
    "H8 - Match 3": {"t1": m_data["16es - Match 5"]["qualifie_reel"], "t2": m_data["16es - Match 6"]["qualifie_reel"]},
    "H8 - Match 4": {"t1": m_data["16es - Match 7"]["qualifie_reel"], "t2": m_data["16es - Match 8"]["qualifie_reel"]},
    "H8 - Match 5": {"t1": m_data["16es - Match 9"]["qualifie_reel"], "t2": m_data["16es - Match 10"]["qualifie_reel"]},
    "H8 - Match 6": {"t1": m_data["16es - Match 11"]["qualifie_reel"], "t2": m_data["16es - Match 12"]["qualifie_reel"]},
    "H8 - Match 7": {"t1": m_data["16es - Match 13"]["qualifie_reel"], "t2": m_data["16es - Match 14"]["qualifie_reel"]},
    "H8 - Match 8": {"t1": m_data["16es - Match 15"]["qualifie_reel"], "t2": m_data["16es - Match 16"]["qualifie_reel"]},
}

# --- CALCUL DU CLASSEMENT ---
def calculer_classement():
    scores = {}
    for user_email, user_pronos in st.session_state.pronos.items():
        nickname = user_pronos.get("nickname_profile", user_email)
        total_points = 0
        for match_id, info in st.session_state.matchs.items():
            if info["termine"] and match_id in user_pronos:
                prono = user_pronos[match_id]
                if isinstance(prono, dict) and prono.get("valide", False):
                    if prono["score1"] == info["score1_reel"] and prono["score2"] == info["score2_reel"]:
                        total_points += 3
                    elif prono["qualifie"] == info["qualifie_reel"]:
                        total_points += 1
        scores[nickname] = total_points
    return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

# --- ÉCRAN DE CONNEXION ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🏆 LOBBY DES PRONOSTICS 🏆</h1>", unsafe_allow_html=True)
    st.subheader("🔑 Accéder à la Salle")
    
    email = st.text_input("Votre adresse Email", key="login_email_unique")
    nickname = st.text_input("Votre Nickname (Nom affiché)", key="login_nick_unique")
    code_salle = st.text_input("Code de la Salle (Ex: LoungeCDM)", key="login_sala_unique", type="password")
    
    if st.button("🌟 Entrer", key="btn_login_submit", use_container_width=True):
        if code_salle == "LoungeCDM" and email and nickname: 
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            st.session_state.user_nickname = nickname
            if email.lower() == "ricardosdias32@gmail.com": 
                st.session_state.is_admin = True
            
            if email not in st.session_state.pronos:
                st.session_state.pronos[email] = {}
            st.session_state.pronos[email]["nickname_profile"] = nickname
                
            st.success(f"Bienvenue {nickname} !")
            st.rerun()
        else: 
            st.error("Veuillez remplir tous les champs correctement.")
else:
    # --- BARRE LATÉRALE ---
    st.sidebar.markdown(f"### 👤 Joueur:\n**{st.session_state.user_nickname}**")
    st.sidebar.markdown(f"<span style='color: #64748b; font-size:12px;'>({st.session_state.user_email})</span>", unsafe_allow_html=True)
    if st.session_state.is_admin: 
        st.sidebar.error("👑 MODE ADMIN ACTIF")
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Menu")
    
    options_menu = ["⚽ Mes Pronostics", "🌳 Arbre des Playoffs", "📊 Classement"]
    if st.session_state.is_admin:
        options_menu.append("🛠️ Zone Admin (Résultats)")
        
    choix_menu = st.sidebar.radio("Aller vers :", options_menu, key="menu_navigation")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.user_authenticated = False
        st.session_state.user_email = ""
        st.session_state.user_nickname = ""
        st.session_state.is_admin = False
        st.rerun()

    # --- SECTION 1: PRONOSTICS ---
    if choix_menu == "⚽ Mes Pronostics":
        st.markdown("<h1 style='color: #3b82f6;'>⚽ Vos Pronostics (16es de Finale)</h1>", unsafe_allow_html=True)
        user = st.session_state.user_email
        if user not in st.session_state.pronos: st.session_state.pronos[user] = {}

        for match_id, info in st.session_state.matchs.items():
            st.markdown(f"<div class='match-box'>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: #3b82f6; font-weight: bold;'>{match_id}</span>", unsafe_allow_html=True)
            
            if info["termine"]:
                st.markdown(f"<span style='color: #10b981; float: right; font-weight: bold;'>🔴 MATCH TERMINÉ ({info['score1_reel']} - {info['score2_reel']}) ➔ {info['qualifie_reel']} 🏆</span>", unsafe_allow_html=True)
                deja_valide = True
            else:
                deja_valide = st.session_state.pronos[user].get(match_id, {}).get("valide", False) if isinstance(st.session_state.pronos[user].get(match_id), dict) else False
                
            col1, col_vs, col2 = st.columns([3, 2, 3])
            
            with col1:
                st.markdown(f"<h3 style='text-align: center;'>{info['flag1']}<br>{info['team1']}</h3>", unsafe_allow_html=True)
                if not deja_valide: s1_in = st.number_input("Buts", min_value=0, step=1, key=f"s1_{match_id}")
                else: 
                    user_score1 = st.session_state.pronos[user].get(match_id, {}).get("score1", 0) if isinstance(st.session_state.pronos[user].get(match_id), dict) else 0
                    st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>{user_score1}</b></p>", unsafe_allow_html=True)
                    
            with col_vs: st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"<h3 style='text-align: center;'>{info['flag2']}<br>{info['team2']}</h3>", unsafe_allow_html=True)
                if not deja_valide: s2_in = st.number_input("Buts", min_value=0, step=1, key=f"s2_{match_id}")
                else: 
                    user_score2 = st.session_state.pronos[user].get(match_id, {}).get("score2", 0) if isinstance(st.session_state.pronos[user].get(match_id), dict) else 0
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
                user_q = st.session_state.pronos[user].get(match_id, {}).get("qualifie", "Aucun") if isinstance(st.session_state.pronos[user].get(match_id), dict) else "Aucun"
                if info["termine"]:
                    st.markdown(f"<p style='color: #64748b;'><b>Votre choix :</b> {user_q}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: #10b981;'><b>✓ Votre choix :</b> {user_q}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- SECTION 2: ARBRE DES PLAYOFFS ---
    elif choix_menu == "🌳 Arbre des Playoffs":
        st.markdown("<h1 style='color: #10b981;'>🌳 Arbre Réel des Playoffs</h1>", unsafe_allow_html=True)
        
        col_16, col_8, col_4 = st.columns(3)
        
        with col_16:
            st.subheader("📋 16es de Finale")
            for m_id, data in st.session_state.matchs.items():
                st.markdown(f"""
                <div class='tree-box'>
                    <b>{m_id}</b><br>
                    {data['flag1']} {data['team1']} vs {data['flag2']} {data['team2']}<br>
                    ➔ Qualifié: <span style='color:#10b981; font-weight:bold;'>{data['qualifie_reel']}</span>
                </div>
                """, unsafe_allow_html=True)

        with col_8:
            st.subheader("⚡ Huitièmes de Finale")
            for h_id, teams in huitiemes.items():
                flag_t1 = get_flag(teams["t1"]) if teams["t1"] != "À Définir" else "🏳️"
                flag_t2 = get_flag(teams["t2"]) if teams["t2"] != "À Définir" else "🏳️"
                st.markdown(f"""
                <div class='tree-box' style='margin-bottom:42px;'>
                    <b>{h_id}</b><br>
                    {flag_t1} {teams['t1']}<br>
                    vs<br>
                    {flag_t2} {teams['t2']}
                </div>
                """, unsafe_allow_html=True)

        with col_4:
            st.subheader("🏆 Quarts et suite")
            st.markdown("<div class='tree-box'><b>Quart de Finale 1:</b><br>Gagnant H8-M1 vs Gagnant H8-M2</div>", unsafe_allow_html=True)
            st.markdown("<div class='tree-box'><b>Quart de Finale 2:</b><br>Gagnant H8-M3 vs Gagnant H8-M4</div>", unsafe_allow_html=True)
            st.markdown("<div class='tree-box'><b>Quart de Finale 3:</b><br>Gagnant H8-M5 vs Gagnant H8-M6</div>", unsafe_allow_html=True)
            st.markdown("<div class='tree-box'><b>Quart de Finale 4:</b><br>Gagnant H8-M7 vs Gagnant H8-M8</div>", unsafe_allow_html=True)

    # --- SECTION 3: CLASSEMENT ---
    elif choix_menu == "📊 Classement":
        st.markdown("<h1 style='color: #f59e0b;'>📊 Classement Général</h1>", unsafe_allow_html=True)
        classement_data = calculer_classement()
        
        if not classement_data:
            st.info("Aucun point n'a encore été distribué. Les matchs doivent être terminés par l'Admin.")
        else:
            st.markdown("<table style='width:100%; border-collapse: collapse; text-align:left;'>", unsafe_allow_html=True)
            st.markdown("<tr style='background-color:#1e293b; color:white;'><th>Rang</th><th>Joueur (Nickname)</th><th>Points</th></tr>", unsafe_allow_html=True)
            for index, (player_nick, points) in enumerate(classement_data.items(), start=1):
                bg_color = "#0f172a" if index % 2 == 0 else "#1e293b"
                badge = "🥇 " if index == 1 else "🥈 " if index == 2 else "🥉 " if index == 3 else f"{index} "
                st.markdown(f"<tr style='background-color:{bg_color}; color:white;'><td><b>{badge}</b></td><td>{player_nick}</td><td><b>{points} pts</b></td></tr>", unsafe_allow_html=True)
            st.markdown("</table>", unsafe_allow_html=True)

    # --- SECTION 4: ZONE ADMIN ---
    elif choix_menu == "🛠️ Zone Admin (Résultats)" and st.session_state.is_admin:
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
        st.title("🛠️ Panneau Admin")
        
        opcao_admin = st.radio("Action :", ["Modifier l'affiche d'un match", "Enregistrer un Résultat Réel"], horizontal=True)
        match_to_mod = st.selectbox("Sélectionner le Match :", list(st.session_state.matchs.keys()))
        
        if opcao_admin == "Modifier l'affiche d'un match":
            col_m1, col_m2 = st.columns(2)
            with col_m1: t1 = st.text_input("Nouvelle Équipe 1", st.session_state.matchs[match_to_mod]["team1"])
            with col_m2: t2 = st.text_input("Nouvelle Équipe 2", st.session_state.matchs[match_to_mod]["team2"])
                
            if st.button("💾 Mettre à jour l'affiche", use_container_width=True):
                st.session_state.matchs[match_to_mod]["team1"] = t1
                st.session_state.matchs[match_to_mod]["flag1"] = get_flag(t1)
                st.session_state.matchs[match_to_mod]["team2"] = t2
                st.session_state.matchs[match_to_mod]["flag2"] = get_flag(t2)
                st.success("Match mis à jour !")
                st.rerun()
                
        elif opcao_admin == "Enregistrer un Résultat Réel":
            col_r1, col_r2 = st.columns(2)
            with col_r1: res1 = st.number_input(f"Buts {st.session_state.matchs[match_to_mod]['team1']}", min_value=0, step=1, value=int(st.session_state.matchs[match_to_mod]["score1_reel"]))
            with col_r2: res2 = st.number_input(f"Buts {st.session_state.matchs[match_to_mod]['team2']}", min_value=0, step=1, value=int(st.session_state.matchs[match_to_mod]["score2_reel"]))
            
            options_qualifie_reel = [st.session_state.matchs[match_to_mod]['team1'], st.session_state.matchs[match_to_mod]['team2']]
            qualifie_reel_input = st.radio("Qui s'est qualifié ?", options_qualifie_reel)
            terminar_jogo = st.checkbox("Clôturer le match", value=st.session_state.matchs[match_to_mod]["termine"])
            
            if st.button("🏆 Enregistrer le Résultat", use_container_width=True):
                st.session_state.matchs[match_to_mod]["score1_reel"] = res1
                st.session_state.matchs[match_to_mod]["score2_reel"] = res2
                st.session_state.matchs[match_to_mod]["qualifie_reel"] = qualifie_reel_input
                st.session_state.matchs[match_to_mod]["termine"] = terminar_jogo
                st.success("Résultat enregistré !")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
