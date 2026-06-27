import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Prono Mondial - Playoffs", page_icon="⚽", layout="wide")

# --- SIMULATION DE BASE DE DONNÉES (Session State) ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Structure des matchs (Exemple standard des 8émes de finale)
if "matchs" not in st.session_state:
    st.session_state.matchs = {
        "Huitième 1": {"team1": "France", "flag1": "🇫🇷", "team2": "Roumanie", "flag2": "🇷🇴", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "etape": "8emes"},
        "Huitième 2": {"team1": "Portugal", "flag1": "🇵🇹", "team2": "Italie", "flag2": "🇮🇹", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "etape": "8emes"},
        "Huitième 3": {"team1": "Espagne", "flag1": "🇪🇸", "team2": "Écosse", "flag2": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "etape": "8emes"},
        "Huitième 4": {"team1": "Allemagne", "flag1": "🇩🇪", "team2": "Danemark", "flag2": "🇩🇰", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "etape": "8emes"},
    }

if "pronos" not in st.session_state:
    st.session_state.pronos = {} # Stockage: {email: {match_id: {score1, score2, qualifie, valide}}}

# --- SYSTEME DE CONNEXION (LOGIN / SALLE) ---
st.title("⚽ Application de Pronostics - Playoffs")

if not st.session_state.user_authenticated:
    st.subheader("Connexion à la Salle de Jeu")
    
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Adresse Email")
        password = st.text_input("Mot de passe", type="password")
    with col2:
        code_salle = st.text_input("Code de la Salle (Ex: MONDIAL2026)")
    
    if st.button("Se connecter / Rejoindre"):
        if code_salle == "MONDIAL2026" and email: # Code unique pour éviter de relancer à chaque fois
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            # Définition de l'admin
            if email == "admin@admin.com": # Altere para o seu email de administrador
                st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("Code de salle ou email invalide.")
else:
    st.sidebar.write(f"👤 Connecté en tant que: **{st.session_state.user_email}**")
    if st.session_state.is_admin:
        st.sidebar.success("👑 Mode Administrateur Actif")
    
    if st.sidebar.button("Se déconnecter"):
        st.session_state.user_authenticated = False
        st.rerun()

    # --- ESPACE ADMINISTRATEUR ---
    if st.session_state.is_admin:
        st.header("🛠️ Panneau Administrateur (Entrée des scores)")
        match_A_entrer = st.selectbox("Choisir le match à mettre à jour", list(st.session_state.matchs.keys()))
        m_data = st.session_state.matchs[match_A_entrer]
        
        if not m_data["termine"]:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                sc1 = st.number_input(f"Score {m_data['team1']}", min_value=0, step=1, key="admin_sc1")
            with col_b:
                sc2 = st.number_input(f"Score {m_data['team2']}", min_value=0, step=1, key="admin_sc2")
            with col_c:
                # En cas d'égalité sur 90 min, il faut choisir qui passe
                qualif = st.selectbox("Qui se qualifie ?", [m_data['team1'], m_data['team2']])
                
            if st.button("Valider le résultat officiel"):
                st.session_state.matchs[match_A_entrer]["score1_reel"] = sc1
                st.session_state.matchs[match_A_entrer]["score2_reel"] = sc2
                st.session_state.matchs[match_A_entrer]["qualifie_reel"] = qualif
                st.session_state.matchs[match_A_entrer]["termine"] = True
                
                # --- LOGIQUE DE PROGRESSION AUTOMATIQUE ---
                # Exemple de logique pour générer le quart de finale automatiquement
                if match_A_entrer == "Huitième 1" or match_A_entrer == "Huitième 2":
                    q_nom = "Quart de Finale 1"
                    if q_nom not in st.session_state.matchs:
                        st.session_state.matchs[q_nom] = {"team1": "À Déterminer", "flag1": "🏳️", "team2": "À Déterminer", "flag2": "🏳️", "score1_reel": None, "score2_reel": None, "qualifie_reel": None, "termine": False, "etape": "quarts"}
                    
                    if match_A_entrer == "Huitième 1":
                        st.session_state.matchs[q_nom]["team1"] = qualif
                        st.session_state.matchs[q_nom]["flag1"] = m_data["flag1"] if qualif == m_data["team1"] else m_data["flag2"]
                    else:
                        st.session_state.matchs[q_nom]["team2"] = qualif
                        st.session_state.matchs[q_nom]["flag2"] = m_data["flag1"] if qualif == m_data["team1"] else m_data["flag2"]
                
                st.success("Résultat enregistré et tableau mis à jour !")
                st.rerun()
        else:
            st.info("Ce match est déjà terminé.")
        st.write("---")

    # --- ESPACE JOUEUR (PRONOSTICS) ---
    st.header("📝 Vos Pronostics (Temps Réglementaire 90' + Qualifié)")
    st.caption("Règles : 1pt si bon résultat (1N2), 3pts si Score Exact. Vous devez aussi choisir qui se qualifie.")

    user = st.session_state.user_email
    if user not in st.session_state.pronos:
        st.session_state.pronos[user] = {}

    for match_id, info in st.session_state.matchs.items():
        st.subheader(f"➔ {match_id} ({info['etape'].upper()})")
        
        # Vérifier si l'utilisateur a déjà validé ce prono
        deja_valide = st.session_state.pronos[user].get(match_id, {}).get("valide", False)
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        
        with col1:
            st.markdown(f"### {info['flag1']} {info['team1']}")
        with col2:
            if deja_valide:
                st.write(f"Score: **{st.session_state.pronos[user][match_id]['score1']}**")
            else:
                score1_input = st.number_input("Score", min_value=0, step=1, key=f"s1_{match_id}", label_visibility="collapsed")
        with col3:
            if deja_valide:
                st.write(f"Score: **{st.session_state.pronos[user][match_id]['score2']}**")
            else:
                score2_input = st.number_input("Score", min_value=0, step=1, key=f"s2_{match_id}", label_visibility="collapsed")
        with col4:
            st.markdown(f"### {info['team2']} {info['flag2']}")
            
        # Choix de l'équipe qui passe (Obligatoire même si match nul sur 90')
        options_qualif = [info['team1'], info['team2']]
        
        if deja_valide:
            st.write(f"Qualifié choisi: **{st.session_state.pronos[user][match_id]['qualifie']}**")
            st.warning("⚠️ Ce pronostic est verrouillé, vous ne pouvez plus le modifier (Pas de triche !)")
        else:
            qualif_input = st.radio(f"Qui va passer au tour suivant ?", options_qualif, key=f"q_{match_id}", horizontal=True)
            if st.button("Valider définitivement", key=f"btn_{match_id}"):
                st.session_state.pronos[user][match_id] = {
                    "score1": score1_input,
                    "score2": score2_input,
                    "qualifie": qualif_input,
                    "valide": True
                }
                st.success("Pronostic enregistré avec succès !")
                st.rerun()
        st.write("---")

    # --- CLASSEMENT DES AMIS ---
    st.header("🏆 Classement de la Salle")
    # Logique de calcul des points à afficher ici en comparant st.session_state.pronos et st.session_state.matchs
    st.info("Le classement se mettra à jour dès que l'administrateur aura entré les scores officiels.")
