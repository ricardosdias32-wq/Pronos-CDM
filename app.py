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

# --- DÉTECTEUR DE DRAPEAUX (ANTI-ERREUR) ---
def get_flag(team_name):
    drapeaux = {
        "mexique": "🇲🇽", "mexico": "🇲🇽",
        "afrique du sud": "🇿🇦", "afrika du sul": "🇿🇦", "africa du sul": "🇿🇦", "africa do sul": "🇿🇦",
        "coree du sud": "🇰🇷", "coreia do sul": "🇰🇷", "south korea": "🇰🇷",
        "tchequie": "🇨🇿", "republique cheque": "🇨🇿", "republica checa": "🇨🇿", "czechia": "🇨🇿",
        "canada": "🇨🇦", "suisse": "🇨🇭", "suica": "🇨🇭", "qatar": "🇶🇦", "catar": "🇶🇦",
        "bosnie": "🇧🇦", "bosnia": "🇧🇦", "bresil": "🇧🇷", "brasil": "🇧🇷", "brazil": "🇧🇷",
        "maroc": "🇲🇦", "marrocos": "🇲🇦", "morocco": "🇲🇦", "ecosse": "🏴 ^", "escocia": "🏴 ^",
        "usa": "🇺🇸", "etats-unis": "🇺🇸", "eua": "🇺🇸", "paraguay": "🇵🇾", "paraguai": "🇵🇾",
        "australie": "🇦🇺", "australia": "🇦🇺", "turquie": "🇹🇷", "turquia": "🇹🇷", "turkey": "🇹🇷",
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
    return flags.get(text, "🏳️") if 'flags' in locals() else drapeaux.get(text, "🏳️")

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
        "16es - Match 12": {"team1": "Angleterre", "flag1": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 13": {"team1": "Argentine", "flag1": "🇦🇷", "team2": "Cap-Vert", "flag2": "🇨🇻", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 14": {"team1": "Australie", "flag1": "🇦🇺", "team2": "Égypte", "flag2": "🇪🇬", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 15": {"team1": "Suisse", "flag1": "🇨🇭", "team2": "À Définir (Repêchage)", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "16es - Match 16": {"team1": "À Définir (K1)", "flag1": "🏳️", "team2": "Ghana", "flag2": "🇬🇭", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
    }

if "pronos" not in st.session_state: 
    st.session_state.pronos = {}

# --- CALCUL DU CLASSEMENT ---
def calcular_classement():
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

    # --- SÉLECTION 1: MES PRONOSTICS ---
    if choix_menu == "⚽ Mes Pronostics":
        # KPIs de resumo no topo
        classement = calcular_classement()
        meu_score = classement.get(st.session_state.user_nickname, 0)
        meus_jogos = st.session_state.pronos.get(st.session_state.user_email, {})
        total_trancados = sum(1 for m, v in meus_jogos.items() if isinstance(v, dict) and v.get("valide"))
        
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1: st.markdown(f"<div class='kpi-box'><span style='color:#a855f7;'>🔒 Apostas Trancadas</span><h2>{total_trancados} / 16</h2></div>", unsafe_allow_html=True)
        with col_kpi2: st.markdown(f"<div class='kpi-box'><span style='color:#f59e0b;'>⭐ Teus Pontos</span><h2>{meu_score} pts</h2></div>", unsafe_allow_html=True)
        with col_kpi3: st.markdown(f"<div class='kpi-box'><span style='color:#10b981;'>📈 Posição Atual</span><h2>#{list(classement.keys()).index(st.session_state.user_nickname)+1 if st.session_state.user_nickname in classement else '-'}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<br><h2 style='color: #3b82f6;'>⚽ Teus Prognósticos</h2>", unsafe_allow_html=True)
        user = st.session_state.user_email

        for match_id, info in st.session_state.matchs.items():
            st.markdown(f"<div class='match-box'>", unsafe_allow_html=True)
            deja_valide = st.session_state.pronos[user].get(match_id, {}).get("valide", False) if isinstance(st.session_state.pronos[user].get(match_id), dict) else False
            
            # Header do Card
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

    # --- SÉLECTION 2: PALPITES DO GRUPO (AGORA COM FILTRO DUPLO!) ---
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
                    tabela_dados.append({
                        "Jogador": nick,
                        "Palpite": f"{p_user['score1']} - {p_user['score2']}",
                        "Quem Avança": p_user['qualifie']
                    })
            if tabela_dados: st.table(tabela_dados)
            else: st.info("Ninguém trancou palpites para este jogo ainda.")

    # --- O RESTO DO CÓDIGO (ÁRVORE, CLASSEMENT, ADMIN) MANTÉM-SE IGUAL ---
    elif choix_menu == "🌳 Arbre des Playoffs":
        st.markdown("<h1 style='color: #10b981;'>🌳 Arbre Réel des Playoffs</h1>", unsafe_allow_html=True)
        col_16, col_8 = st.columns(2)
        with col_16:
            st.subheader("📋 16es de Finale")
            for m_id, data in st.session_state.matchs.items():
                st.markdown(f"<div class='tree-box'><b>{m_id}</b><br>{data['flag1']} {data['team1']} vs {data['flag2']} {data['team2']}<br>➔ Vencedor: {data['qualifie_reel']}</div>", unsafe_allow_html=True)
        with col_8:
            st.subheader("⚡ Quart de Finale (Exemplo)")
            st.info("Os Oitavos e Quartos são calculados automaticamente consoante o Admin fecha os jogos anteriores.")

    elif choix_menu == "📊 Classement":
        st.markdown("<h1 style='color: #f59e0b;'>📊 Classement Général</h1>", unsafe_allow_html=True)
        classement_data = calculer_classement()
        if not classement_data: st.info("Nenhum jogo concluído ainda.")
        else:
            for i, (nick, pts) in enumerate(classement_data.items(), start=1):
                st.markdown(f"**#{i} {nick}** - {pts} pts")

    elif choix_menu == "🛠️ Zone Admin" and st.session_state.is_admin:
        st.title("🛠️ Panneau Admin")
        match_to_mod = st.selectbox("Match :", list(st.session_state.matchs.keys()))
        res1 = st.number_input("Golos Equipa 1", min_value=0, step=1)
        res2 = st.number_input("Golos Equipa 2", min_value=0, step=1)
        q_r = st.radio("Qualificado Real", [st.session_state.matchs[match_to_mod]['team1'], st.session_state.matchs[match_to_mod]['team2']])
        term = st.checkbox("Fechar jogo")
        if st.button("Gravar Resultado Real"):
            st.session_state.matchs[match_to_mod]["score1_reel"] = res1
            st.session_state.matchs[match_to_mod]["score2_reel"] = res2
            st.session_state.matchs[match_to_mod]["qualifie_reel"] = q_r
            st.session_state.matchs[match_to_mod]["termine"] = term
            st.success("Gravado!")
            st.rerun()
