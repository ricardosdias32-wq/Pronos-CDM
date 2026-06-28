import streamlit as st
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Prono Mondial - Pro Edition", page_icon="🏆", layout="wide")

# --- STYLES VISUELS PERSONNALISÉS (CSS PREMIUM) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    .kpi-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #4c1d95;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .match-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #3b82f6;
        margin-bottom: 20px;
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
        font-size: 22px;
        font-weight: bold;
        color: #94a3b8;
        text-align: center;
        margin-top: 15px;
    }
    .badge-status {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION SESSION STATE ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.user_email = ""
    st.session_state.user_nickname = ""
    st.session_state.is_admin = False

# --- DÉTECTEUR DE DRAPEAUX ---
def get_flag(team_name):
    if not team_name or team_name in ["À Définir", "À Espera de Vencedor"]:
        return "🏳️"
    drapeaux = {
        "mexique": "🇲🇽", "mexico": "🇲🇽", "afrique du sud": "🇿🇦", "afrika du sul": "🇿🇦", 
        "africa du sul": "🇿🇦", "africa do sul": "🇿🇦", "coree du sud": "🇰🇷", "coreia do sul": "🇰🇷", 
        "south korea": "🇰🇷", "tchequie": "🇨🇿", "republique cheque": "🇨🇿", "republica checa": "🇨🇿", 
        "canada": "🇨🇦", "suisse": "🇨🇭", "suica": "🇨🇭", "qatar": "🇶🇦", "catar": "🇶🇦",
        "bosnie": "🇧🇦", "bosnia": "🇧🇦", "bresil": "🇧🇷", "brasil": "🇧🇷", "brazil": "🇧🇷",
        "maroc": "🇲🇦", "marrocos": "🇲🇦", "morocco": "🇲🇦", "usa": "🇺🇸", "etats-unis": "🇺🇸", 
        "eua": "🇺🇸", "paraguay": "🇵🇾", "paraguai": "🇵🇾", "australie": "🇦🇺", "australia": "🇦🇺", 
        "allemagne": "🇩🇪", "alemanha": "🇩🇪", "germany": "🇩🇪", "equateur": "🇪🇨", "equador": "🇪🇨",
        "cote d'ivoire": "🇨🇮", "costa do marfim": "🇨🇮", "pays-bas": "🇳🇱", "paises baixos": "🇳🇱",
        "japon": "🇯🇵", "japao": "🇯🇵", "suede": "🇸🇪", "suecia": "🇸🇪", "tunisie": "🇹🇳",
        "belgique": "🇧🇪", "belgica": "🇧🇪", "egypte": "🇪🇬", "egito": "🇪🇬", "iran": "🇮🇷",
        "nouvelle-zelande": "🇳🇿", "nova zelandia": "🇳🇿", "espagne": "🇪🇸", "espanha": "🇪🇸",
        "uruguay": "🇺🇾", "uruguai": "🇺🇾", "arabie saoudite": "🇸🇦", "arabia saudita": "🇸🇦",
        "france": "🇫🇷", "franca": "🇫🇷", "senegal": "🇸🇳", "norvege": "🇳🇴", "noruega": "🇳🇴",
        "argentine": "🇦🇷", "argentina": "🇦🇷", "autriche": "🇦🇹", "algerie": "🇩🇿",
        "portugal": "🇵🇹", "colombie": "🇨🇴", "colombia": "🇨🇴", "angleterre": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "england": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "croatie": "🇭🇷", "croacia": "🇭🇷",
        "ghana": "🇬🇭", "gana": "🇬🇭", "panama": "🇵🇦", "cap-vert": "🇨🇻", "cabo verde": "🇨🇻"
    }
    text = str(team_name).strip().lower()
    text = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return drapeaux.get(text, "🏳️")

# --- BASE DE DONNÉES COMPLÈTE (DU 16es À LA FINALE) ---
if "matchs" not in st.session_state:
    st.session_state.matchs = {
        # 16es de Finale
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
        "16es - Match 12": {"team1": "Angleterre", "flag1": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 13": {"team1": "Argentine", "flag1": "🇦🇷", "team2": "Cap-Vert", "flag2": "🇨🇻", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 14": {"team1": "Australie", "flag1": "🇦🇺", "team2": "Égypte", "flag2": "🇪🇬", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 15": {"team1": "Suisse", "flag1": "🇨🇭", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 16": {"team1": "À Définir (K1)", "flag1": "🏳️", "team2": "Ghana", "flag2": "🇬🇭", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        
        # Huitièmes de Finale
        "8es - Match 1": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "8es - Match 2": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "8es - Match 3": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "8es - Match 4": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "8es - Match 5": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "8es - Match 6": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "8es - Match 7": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "8es - Match 8": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        
        # Quarts de Finale
        "Quarts - Match 1": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "Quarts - Match 2": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "Quarts - Match 3": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "Quarts - Match 4": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        
        # Demis-Finales
        "Demis - Match 1": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "Demis - Match 2": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        
        # Petite Finale (3ème Place)
        "3ème Place": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        
        # Finale
        "Finale": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
    }

if "pronos" not in st.session_state: 
    st.session_state.pronos = {}

# --- FONCTION DE CALCUL DES BRACKETS AUTOMATIQUES (LOGIQUE DE CASCADE) ---
def actualiser_arbre_dynamique():
    m = st.session_state.matchs
    
    # 1. Alimentar Oitavos com base nos vencedores dos 16-avos
    mapping_8es = {
        "8es - Match 1": ("16es - Match 1", "16es - Match 2"),
        "8es - Match 2": ("16es - Match 3", "16es - Match 4"),
        "8es - Match 3": ("16es - Match 5", "16es - Match 6"),
        "8es - Match 4": ("16es - Match 7", "16es - Match 8"),
        "8es - Match 5": ("16es - Match 9", "16es - Match 10"),
        "8es - Match 6": ("16es - Match 11", "16es - Match 12"),
        "8es - Match 7": ("16es - Match 13", "16es - Match 14"),
        "8es - Match 8": ("16es - Match 15", "16es - Match 16"),
    }
    for alvo, (origem1, origem2) in mapping_8es.items():
        if m[origem1]["termine"]:
            m[alvo]["team1"] = m[origem1]["qualifie_reel"]
            m[alvo]["flag1"] = get_flag(m[alvo]["team1"])
        if m[origem2]["termine"]:
            m[alvo]["team2"] = m[origem2]["qualifie_reel"]
            m[alvo]["flag2"] = get_flag(m[alvo]["team2"])

    # 2. Alimentar Quartos com base nos Oitavos
    mapping_quarts = {
        "Quarts - Match 1": ("8es - Match 1", "8es - Match 2"),
        "Quarts - Match 2": ("8es - Match 3", "8es - Match 4"),
        "Quarts - Match 3": ("8es - Match 5", "8es - Match 6"),
        "Quarts - Match 4": ("8es - Match 7", "8es - Match 8"),
    }
    for alvo, (origem1, origem2) in mapping_quarts.items():
        if m[origem1]["termine"]:
            m[alvo]["team1"] = m[origem1]["qualifie_reel"]
            m[alvo]["flag1"] = get_flag(m[alvo]["team1"])
        if m[origem2]["termine"]:
            m[alvo]["team2"] = m[origem2]["qualifie_reel"]
            m[alvo]["flag2"] = get_flag(m[alvo]["team2"])

    # 3. Alimentar Meias com base nos Quartos
    mapping_demis = {
        "Demis - Match 1": ("Quarts - Match 1", "Quarts - Match 2"),
        "Demis - Match 2": ("Quarts - Match 3", "Quarts - Match 4"),
    }
    for alvo, (origem1, origem2) in mapping_demis.items():
        if m[origem1]["termine"]:
            m[alvo]["team1"] = m[origem1]["qualifie_reel"]
            m[alvo]["flag1"] = get_flag(m[alvo]["team1"])
        if m[origem2]["termine"]:
            m[alvo]["team2"] = m[origem2]["qualifie_reel"]
            m[alvo]["flag2"] = get_flag(m[alvo]["team2"])

    # 4. Alimentar Final e 3º Lugar com base nas Meias
    if m["Demis - Match 1"]["termine"] and m["Demis - Match 2"]["termine"]:
        # Finalistas (Vencedores das meias)
        m["Finale"]["team1"] = m["Demis - Match 1"]["qualifie_reel"]
        m["Finale"]["flag1"] = get_flag(m["Finale"]["team1"])
        m["Finale"]["team2"] = m["Demis - Match 2"]["qualifie_reel"]
        m["Finale"]["flag2"] = get_flag(m["Finale"]["team2"])
        
        # 3º Lugar (Derrotados das meias)
        d1 = m["Demis - Match 1"]["team2"] if m["Demis - Match 1"]["qualifie_reel"] == m["Demis - Match 1"]["team1"] else m["Demis - Match 1"]["team1"]
        d2 = m["Demis - Match 2"]["team2"] if m["Demis - Match 2"]["qualifie_reel"] == m["Demis - Match 2"]["team1"] else m["Demis - Match 2"]["team1"]
        m["3ème Place"]["team1"] = d1
        m["3ème Place"]["flag1"] = get_flag(d1)
        m["3ème Place"]["team2"] = d2
        m["3ème Place"]["flag2"] = get_flag(d2)

# Chamar a função para atualizar os encadeamentos reais sempre que o script rodar
actualiser_arbre_dynamique()

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

# --- CONNEXION ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🏆 LOBBY DES PRONOSTICS 🏆</h1>", unsafe_allow_html=True)
    st.subheader("🔑 Accéder à la Salle")
    email = st.text_input("Adresse Email").strip()
    nickname = st.text_input("Nickname (Nom affiché)").strip()
    code_salle = st.text_input("Code de la Salle", type="password")
    
    if st.button("🌟 Entrer", use_container_width=True):
        if code_salle == "LoungeCDM" and email and nickname:
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            st.session_state.user_nickname = nickname
            st.session_state.is_admin = (email.lower() == "ricardosdias32@gmail.com")
            if email not in st.session_state.pronos: st.session_state.pronos[email] = {}
            st.session_state.pronos[email]["nickname_profile"] = nickname
            st.rerun()
        else: st.error("Champs incorrects.")
else:
    # --- BARRE LATÉRALE ---
    st.sidebar.markdown(f"### 👤 **{st.session_state.user_nickname}**")
    if st.session_state.is_admin: st.sidebar.error("👑 MODE ADMIN")
    
    options_menu = ["⚽ Mes Pronostics", "👀 Palpites do Grupo", "🌳 Arbre des Playoffs", "📊 Classement"]
    if st.session_state.is_admin: options_menu.append("🛠️ Zone Admin")
    choix_menu = st.sidebar.radio("Menu :", options_menu)
    
    if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.user_authenticated = False
        st.rerun()

    # --- MES PRONOSTICS ---
    if choix_menu == "⚽ Mes Pronostics":
        classement = calcular_classement()
        meu_score = classement.get(st.session_state.user_nickname, 0)
        meus_jogos = st.session_state.pronos.get(st.session_state.user_email, {})
        total_trancados = sum(1 for m, v in meus_jogos.items() if isinstance(v, dict) and v.get("valide"))
        
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1: st.markdown(f"<div class='kpi-box'><span style='color:#a855f7;'>🔒 Apostas Trancadas</span><h2>{total_trancados}</h2></div>", unsafe_allow_html=True)
        with col_kpi2: st.markdown(f"<div class='kpi-box'><span style='color:#f59e0b;'>⭐ Teus Pontos</span><h2>{meu_score} pts</h2></div>", unsafe_allow_html=True)
        with col_kpi3: st.markdown(f"<div class='kpi-box'><span style='color:#10b981;'>📈 Posição Atual</span><h2>#{list(classement.keys()).index(st.session_state.user_nickname)+1 if st.session_state.user_nickname in classement else '-'}</h2></div>", unsafe_allow_html=True)
        
        fase_sel = st.selectbox("Escolher Fase da Competição:", ["16es de Finale", "8es de Finale", "Quarts de Finale", "Demis / Finales"])
        st.markdown(f"<br><h2 style='color: #3b82f6;'>⚽ Teus Prognósticos - {fase_sel}</h2>", unsafe_allow_html=True)
        user = st.session_state.user_email

        for match_id, info in st.session_state.matchs.items():
            if (fase_sel == "16es de Finale" and "16es" not in match_id) or \
               (fase_sel == "8es de Finale" and "8es" not in match_id) or \
               (fase_sel == "Quarts de Finale" and "Quarts" not in match_id) or \
               (fase_sel == "Demis / Finales" and "Demis" not in match_id and "Place" not in match_id and "Finale" not in match_id):
                continue
                
            st.markdown(f"<div class='match-box'>", unsafe_allow_html=True)
            deja_valide = st.session_state.pronos[user].get(match_id, {}).get("valide", False) if isinstance(st.session_state.pronos[user].get(match_id), dict) else False
            
            if info["termine"]:
                prono = st.session_state.pronos[user].get(match_id, {})
                if prono.get("score1") == info["score1_reel"] and prono.get("score2") == info["score2_reel"]:
                    st.markdown(f"<span style='float:right;' class='badge-status'>🟢 EXATO (+3) | Fim: {info['score1_reel']}-{info['score2_reel']}</span>", unsafe_allow_html=True)
                elif prono.get("qualifie") == info["qualifie_reel"]:
                    st.markdown(f"<span style='float:right;' class='badge-status'>🟡 QUALIFICADO (+1) | Fim: {info['score1_reel']}-{info['score2_reel']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='float:right;' class='badge-status'>🔴 FALHADO | Fim: {info['score1_reel']}-{info['score2_reel']}</span>", unsafe_allow_html=True)
            elif deja_valide:
                st.markdown("<span style='color: #10b981; float: right; font-weight: bold;'>🔒 Submetido</span>", unsafe_allow_html=True)
                
            st.markdown(f"<span style='color: #3b82f6; font-weight: bold;'>{match_id}</span>", unsafe_allow_html=True)
            
            col1, col_vs, col2 = st.columns([3, 2, 3])
            with col1:
                st.markdown(f"<h3 style='text-align: center;'>{info['flag1']}<br>{info['team1']}</h3>", unsafe_allow_html=True)
                if not deja_valide: s1_in = st.number_input("Golos", min_value=0, step=1, key=f"s1_{match_id}")
                else: st.markdown(f"<p style='text-align: center; font-size: 24px;'><b>{st.session_state.pronos[user][match_id]['score1']}</b></p>", unsafe_allow_html=True)
            with col_vs: st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<h3 style='text-align: center;'>{info['flag2']}<br>{info['team2']}</h3>", unsafe_allow_html=True)
                if not deja_valide: s2_in = st.number_input("Golos", min_value=0, step=1, key=f"s2_{match_id}")
                else: st.markdown(f"<p style='text-align: center; font-size: 24px;'><b>{st.session_state.pronos[user][match_id]['score2']}</b></p>", unsafe_allow_html=True)
            
            if not deja_valide:
                q_in = st.radio("Quem passa de fase?", [info['team1'], info['team2']], key=f"q_{match_id}", horizontal=True)
                if st.button(f"🔒 Trancar Palpite ({match_id})", key=f"btn_{match_id}", use_container_width=True):
                    st.session_state.pronos[user][match_id] = {"score1": s1_in, "score2": s2_in, "qualifie": q_in, "valide": True}
                    st.rerun()
            else:
                st.markdown(f"<p style='text-align:center; color:#94a3b8;'>Avança para ti: <b>{st.session_state.pronos[user][match_id]['qualifie']}</b></p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- PALPITES DO GRUPO ---
    elif choix_menu == "👀 Palpites do Grupo":
        st.markdown("<h1 style='color: #a855f7;'>👀 Espreitar os Palpites</h1>", unsafe_allow_html=True)
        modo_vista = st.radio("Como queres espreitar?", ["Por Amigo 👤", "Por Jogo ⚽"], horizontal=True)
        lista_jogadores = {dados.get("nickname_profile", e): e for e, dados in st.session_state.pronos.items()}
        
        if modo_vista == "Por Amigo 👤":
            jogador_sel = st.selectbox("Escolher Amigo:", list(lista_jogadores.keys()))
            email_sel = lista_jogadores[jogador_sel]
            
            for m_id, info in st.session_state.matchs.items():
                p_amigo = st.session_state.pronos[email_sel].get(m_id)
                if isinstance(p_amigo, dict) and p_amigo.get("valide"):
                    st.markdown(f"""
                    <div style='background-color: #1e1b4b; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #a855f7;'>
                        <b>{m_id}</b> | {info['flag1']} {info['team1']} <b>{p_amigo['score1']} - {p_amigo['score2']}</b> {info['flag2']} {info['team2']}<br>
                        🏆 Passa: <b>{p_amigo['qualifie']}</b>
                    </div>
                    """, unsafe_allow_html=True)
                    
        elif modo_vista == "Por Jogo ⚽":
            jogo_sel = st.selectbox("Escolher um Jogo do Calendário:", list(st.session_state.matchs.keys()))
            info_jogo = st.session_state.matchs[jogo_sel]
            st.markdown(f"#### Palpites de todos para: {info_jogo['flag1']} {info_jogo['team1']} vs {info_jogo['flag2']} {info_jogo['team2']}")
            
            tabela_dados = []
            for nick, email_key in lista_jogadores.items():
                p_user = st.session_state.pronos[email_key].get(jogo_sel)
                if isinstance(p_user, dict) and p_user.get("valide"):
                    tabela_dados.append({"Jogador": nick, "Palpite": f"{p_user['score1']} - {p_user['score2']}", "Quem Avança": p_user['qualifie']})
            if tabela_dados: st.table(tabela_dados)
            else: st.info("Ninguém trancou palpites para este jogo ainda.")

    # --- 🌳 ARBRE DES PLAYOFFS 100% DINÂMICA ATÉ À FINAL 🌳 ---
    elif choix_menu == "🌳 Arbre des Playoffs":
        st.markdown("<h1 style='color: #10b981;'>🌳 Árvore Oficial e Real do Torneio</h1>", unsafe_allow_html=True)
        st.write("Acompanha o progresso real das equipas. Os vencedores sobem de fase automaticamente assim que o admin fecha o jogo.")
        
        fase_arv = st.radio("Filtrar Árvore por Ronda:", ["16es de Final", "Oitavos e Quartos", "Meias e Finais"], horizontal=True)
        m_ctx = st.session_state.matchs
        
        if fase_arv == "16es de Final":
            st.subheader("📋 Dezasseis-avos de Final")
            colA, colB = st.columns(2)
            for idx, (m_id, data) in enumerate(m_ctx.items()):
                if "16es" in m_id:
                    vencedor_txt = f"🏆 {data['qualifie_reel']}" if data['termine'] else "⏳ Em jogo..."
                    box_html = f"""
                    <div class='tree-box'>
                        <span style='color:#3b82f6; font-weight:bold;'>{m_id}</span><br>
                        {data['flag1']} {data['team1']} <b>{data['score1_reel'] if data['termine'] else ''}</b> vs 
                        <b>{data['score2_reel'] if data['termine'] else ''}</b> {data['flag2']} {data['team2']}<br>
                        <small style='color:#10b981;'>Qualificado: {vencedor_txt}</small>
                    </div>"""
                    if idx % 2 == 0: colA.markdown(box_html, unsafe_allow_html=True)
                    else: colB.markdown(box_html, unsafe_allow_html=True)
                    
        elif fase_arv == "Oitavos e Quartos":
            col8, col4 = st.columns(2)
            with col8:
                st.subheader("⚡ Oitavos de Final")
                for m_id, data in m_ctx.items():
                    if "8es" in m_id:
                        vencedor_txt = f"➡️ {data['qualifie_reel']}" if data['termine'] else "⏳ Aberto"
                        st.markdown(f"""
                        <div class='tree-box'>
                            <b>{m_id}</b><br>
                            {data['flag1']} {data['team1']} vs {data['flag2']} {data['team2']}<br>
                            <small style='color:#f59e0b;'>{vencedor_txt}</small>
                        </div>""", unsafe_allow_html=True)
            with col4:
                st.subheader("⚔️ Quartos de Final")
                for m_id, data in m_ctx.items():
                    if "Quarts" in m_id:
                        vencedor_txt = f"➡️ {data['qualifie_reel']}" if data['termine'] else "⏳ Aberto"
                        st.markdown(f"""
                        <div class='tree-box' style='margin-bottom:50px;'>
                            <b>{m_id}</b><br>
                            {data['flag1']} {data['team1']} vs {data['flag2']} {data['team2']}<br>
                            <small style='color:#a855f7;'>{vencedor_txt}</small>
                        </div>""", unsafe_allow_html=True)
                        
        elif fase_arv == "Meias e Finais":
            col_demi, col_final = st.columns(2)
            with col_demi:
                st.subheader("🔥 Meias-Finais")
                for m_id, data in m_ctx.items():
                    if "Demis" in m_id:
                        st.markdown(f"""
                        <div class='tree-box' style='margin-bottom:30px;'>
                            <b>{m_id}</b><br>
                            {data['flag1']} {data['team1']} vs {data['flag2']} {data['team2']}<br>
                            <small style='color:#f59e0b;'>Fim: {'Fechado' if data['termine'] else 'Aguardando'}</small>
                        </div>""", unsafe_allow_html=True)
            with col_final:
                st.subheader("👑 Decisões Finais")
                # 3º Lugar
                p3 = m_ctx["3ème Place"]
                st.markdown(f"""
                <div class='tree-box' style='border-color: #64748b;'>
                    <b>🥉 Jogo do 3º Lugar</b><br>
                    {p3['flag1']} {p3['team1']} vs {p3['flag2']} {p3['team2']}<br>
                    <b style='color:#cd7f32;'>Vencedor: {p3['qualifie_reel'] if p3['termine'] else '⏳'}</b>
                </div>""", unsafe_allow_html=True)
                
                # Grande Final
                fin = m_ctx["Finale"]
                st.markdown(f"""
                <div class='tree-box' style='background: linear-gradient(135deg, #1e1b4b 0%, #1e293b 100%); border: 2px solid #f59e0b;'>
                    <b style='color:#f59e0b;'>👑 GRANDE FINAL</b><br>
                    {fin['flag1']} {fin['team1']} vs {fin['flag2']} {fin['team2']}<br>
                    <h4 style='color:#10b981; margin-top:5px;'>🏆 CAMPEÃO: {fin['qualifie_reel'] if fin['termine'] else '🥇 À Espera...'}</h4>
                </div>""", unsafe_allow_html=True)

    # --- CLASSEMENT ---
    elif choix_menu == "📊 Classement":
        st.markdown("<h1 style='color: #f59e0b;'>📊 Classement Général</h1>", unsafe_allow_html=True)
        classement_data = calculer_classement()
        if not classement_data: st.info("Nenhum jogo concluído ainda.")
        else:
            st.markdown("<table style='width:100%; text-align:left;'><tr><th>Pos</th><th>Jogador</th><th>Pontos Totais</th></tr>", unsafe_allow_html=True)
            for i, (nick, pts) in enumerate(classement_data.items(), start=1):
                st.markdown(f"<tr><td><b>#{i}</b></td><td>{nick}</td><td><b>{pts} pts</b></td></tr>", unsafe_allow_html=True)
            st.markdown("</table>", unsafe_allow_html=True)

    # --- ZONE ADMIN ---
    elif choix_menu == "🛠️ Zone Admin" and st.session_state.is_admin:
        st.title("🛠️ Panneau Admin")
        match_to_mod = st.selectbox("Escolher Jogo para Configurar/Fechar:", list(st.session_state.matchs.keys()))
        
        st.markdown("### 1. Atualizar Equipas do Jogo (Avançar as chaves)")
        eq1 = st.text_input("Nome Equipa 1", st.session_state.matchs[match_to_mod]["team1"])
        eq2 = st.text_input("Nome Equipa 2", st.session_state.matchs[match_to_mod]["team2"])
        
        st.markdown("### 2. Lançar Resultado Oficial")
        res1 = st.number_input("Golos Reais Equipa 1", min_value=0, step=1, value=int(st.session_state.matchs[match_to_mod]["score1_reel"]))
        res2 = st.number_input("Golos Reais Equipa 2", min_value=0, step=1, value=int(st.session_state.matchs[match_to_mod]["score2_reel"]))
        q_r = st.radio("Quem se qualificou oficialmente?", [eq1, eq2])
        term = st.checkbox("Fechar jogo e Distribuir Pontos", value=st.session_state.matchs[match_to_mod]["termine"])
        
        if st.button("💾 Salvar Tudo para este Jogo"):
            st.session_state.matchs[match_to_mod]["team1"] = eq1
            st.session_state.matchs[match_to_mod]["flag1"] = get_flag(eq1)
            st.session_state.matchs[match_to_mod]["team2"] = eq2
            st.session_state.matchs[match_to_mod]["flag2"] = get_flag(eq2)
            st.session_state.matchs[match_to_mod]["score1_reel"] = res1
            st.session_state.matchs[match_to_mod]["score2_reel"] = res2
            st.session_state.matchs[match_to_mod]["qualifie_reel"] = q_r
            st.session_state.matchs[match_to_mod]["termine"] = term
            st.success("Dados guardados! O ranking foi recalculado.")
            st.rerun()
