import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Prono Mundial - Playoffs", page_icon="⚽", layout="wide")

# --- ESTILOS VISUAIS PERSONALIZADOS (CSS) ---
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

# --- DETECTOR AUTOMÁTICO DE BANDEIRAS ---
def get_flag(team_name):
    drapeaux = {
        "alemanha": "🇩🇪", "paraguai": "🇵🇾", "frança": "🇫🇷", "suécia": "🇸🇪", "suecia": "🇸🇪",
        "áfrica do sul": "🇿🇦", "africa do sul": "🇿🇦", "canadá": "🇨🇦", "canada": "🇨🇦",
        "países baixos": "🇳🇱", "paises baixos": "🇳🇱", "marrocos": "🇲🇦", "croácia": "🇭🇷", "croacia": "🇭🇷",
        "espanha": "🇪🇸", "eua": "🇺🇸", "estados unidos": "🇺🇸", "bósnia e herzegovina": "🇧🇦", "bosnia e herzegovina": "🇧🇦",
        "bélgica": "🇧🇪", "belgica": "🇧🇪", "brasil": "🇧🇷", "japão": "🇯🇵", "japao": "🇯🇵",
        "costa do marfim": "🇨🇮", "noruega": "🇳🇴", "méxico": "🇲🇽", "mexico": "🇲🇽", "equador": "🇪🇨",
        "inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "argentina": "🇦🇷", "cabo verde": "🇨🇻", "austrália": "🇦🇺", "australia": "🇦🇺",
        "egipto": "🇪🇬", "egito": "🇪🇬", "suiça": "🇨🇭", "suiça": "🇨🇭", "gana": "🇬🇭",
        "colômbia": "🇨🇴", "colombia": "🇨🇴", "portugal": "🇵🇹", "uzbequistão": "🇺🇿", "uzbequistao": "🇺🇿"
    }
    cleaned = str(team_name).strip().lower()
    return drapeaux.get(cleaned, "🏳️")

if "matchs" not in st.session_state:
    st.session_state.matchs = {
        "16avos - Jogo 1": {"team1": "Alemanha", "flag1": "🇩🇪", "team2": "Paraguai", "flag2": "🇵🇾"},
        "16avos - Jogo 2": {"team1": "França", "flag1": "🇫🇷", "team2": "Suécia", "flag2": "🇸🇪"},
        "16avos - Jogo 3": {"team1": "África do Sul", "flag1": "🇿🇦", "team2": "Canadá", "flag2": "🇨🇦"},
        "16avos - Jogo 4": {"team1": "Países Baixos", "flag1": "🇳🇱", "team2": "Marrocos", "flag2": "🇲🇦"},
        "16avos - Jogo 5": {"team1": "Por Definir (K2)", "flag1": "🏳️", "team2": "Croácia", "flag2": "🇭🇷"},
        "16avos - Jogo 6": {"team1": "Espanha", "flag1": "🇪🇸", "team2": "Por Definir (J2)", "flag2": "🏳️"},
        "16avos - Jogo 7": {"team1": "EUA", "flag1": "🇺🇸", "team2": "Bósnia e Herzegovina", "flag2": "🇧🇦"},
        "16avos - Jogo 8": {"team1": "Bélgica", "flag1": "🇧🇪", "team2": "Por Definir (Repescagem)", "flag2": "🏳️"},
        "16avos - Jogo 9": {"team1": "Brasil", "flag1": "🇧🇷", "team2": "Japão", "flag2": "🇯🇵"},
        "16avos - Jogo 10": {"team1": "Costa do Marfim", "flag1": "🇨🇮", "team2": "Noruega", "flag2": "🇳🇴"},
        "16avos - Jogo 11": {"team1": "México", "flag1": "🇲🇽", "team2": "Equador", "flag2": "🇪🇨"},
        "16avos - Jogo 12": {"team1": "Inglaterra", "flag1": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "team2": "Por Definir (Repescagem)", "flag2": "🏳️"},
        "16avos - Jogo 13": {"team1": "Argentina", "flag1": "🇦🇷", "team2": "Cabo Verde", "flag2": "🇨🇻"},
        "16avos - Jogo 14": {"team1": "Austrália", "flag1": "🇦🇺", "team2": "Egipto", "flag2": "🇪🇬"},
        "16avos - Jogo 15": {"team1": "Suiça", "flag1": "🇨🇭", "team2": "Por Definir (Repescagem)", "flag2": "🏳️"},
        "16avos - Jogo 16": {"team1": "Por Definir (K1)", "flag1": "🏳️", "team2": "Gana", "flag2": "🇬🇭"},
    }

if "pronos" not in st.session_state: 
    st.session_state.pronos = {}

# --- CABEÇALHO DO SITE ---
st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🏆 LOBBY DE PRONÓSTICOS 🏆</h1>", unsafe_allow_html=True)

if not st.session_state.user_authenticated:
    st.subheader("🔑 Entrar na Sala")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Teu endereço de Email", key="login_email_unique")
    with col2: 
        code_salle = st.text_input("Código da Sala (Ex: LoungeCDM)", key="login_sala_unique")
    
    if st.button("🌟 Entrar e Apostar", key="btn_login_submit", use_container_width=True):
        if code_salle == "LoungeCDM" and email: 
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            if email.lower() == "ricardosdias32@gmail.com": 
                st.session_state.is_admin = True
            st.success("Autenticado com sucesso! A carregar...")
            st.rerun()
        else: 
            st.error("Código da sala ou email incorreto.")
else:
    # --- SIDEBAR (PERFIL DO JOGADOR) ---
    st.sidebar.markdown(f"### 👤 Jogador:\n**{st.session_state.user_email}**")
    if st.session_state.is_admin: 
        st.sidebar.markdown("---")
        st.sidebar.error("👑 MODO ADMINISTRADOR ATIVO")
    
    if st.sidebar.button("🚪 Terminar Sessão", key="btn_logout_sidebar", use_container_width=True):
        st.session_state.user_authenticated = False
        st.session_state.user_email = ""
        st.session_state.is_admin = False
        st.rerun()

    # --- CONTROLO ADMIN ---
    if st.session_state.is_admin:
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
        st.subheader("🛠️ Painel de Controlo do Administrador")
        match_to_mod = st.selectbox("Escolha o Jogo para Atualizar Seleções:", list(st.session_state.matchs.keys()), key="admin_select_match")
        col_m1, col_m2 = st.columns(2)
        with col_m1: t1 = st.text_input("Nova Seleção 1", st.session_state.matchs[match_to_mod]["team1"], key="admin_t1")
        with col_m2: t2 = st.text_input("Nova Seleção 2", st.session_state.matchs[match_to_mod]["team2"], key="admin_t2")
            
        if st.button("💾 Atualizar Equipas e Gerar Bandeiras", key="btn_admin_save", use_container_width=True):
            st.session_state.matchs[match_to_mod]["team1"] = t1
            st.session_state.matchs[match_to_mod]["flag1"] = get_flag(t1)
            st.session_state.matchs[match_to_mod]["team2"] = t2
            st.session_state.matchs[match_to_mod]["flag2"] = get_flag(t2)
            st.success("Sucesso! Equipas atualizadas.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- LISTA DE EVENTOS ---
    st.markdown("<h2 style='color: #f59e0b;'>⚽ Teu Boletim de Apostas</h2>", unsafe_allow_html=True)
    user = st.session_state.user_email
    if user not in st.session_state.pronos: 
        st.session_state.pronos[user] = {}

    for match_id, info in st.session_state.matchs.items():
        st.markdown(f"<div class='match-box'>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: #3b82f6; font-weight: bold;'>{match_id}</span>", unsafe_allow_html=True)
        
        deja_valide = st.session_state.pronos[user].get(match_id, {}).get("valide", False)
        col1, col_vs, col2 = st.columns([3, 2, 3])
        
        with col1:
            st.markdown(f"<h3 style='text-align: center;'>{info['flag1']}<br>{info['team1']}</h3>", unsafe_allow_html=True)
            if not deja_valide: s1_in = st.number_input("Golos", min_value=0, step=1, key=f"s1_{match_id}")
            else: st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>{st.session_state.pronos[user][match_id]['score1']}</b></p>", unsafe_allow_html=True)
                
        with col_vs: st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"<h3 style='text-align: center;'>{info['flag2']}<br>{info['team2']}</h3>", unsafe_allow_html=True)
            if not deja_valide: s2_in = st.number_input("Golos", min_value=0, step=1, key=f"s2_{match_id}")
            else: st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>{st.session_state.pronos[user][match_id]['score2']}</b></p>", unsafe_allow_html=True)
        
        st.markdown("<p style='margin-top: 15px; color: #94a3b8;'>🎯 Quem se qualifica?</p>", unsafe_allow_html=True)
        options_q = [info['team1'], info['team2']]
        
        if not deja_valide:
            q_in = st.radio("Qualificado", options_q, key=f"q_{match_id}", horizontal=True, label_visibility="collapsed")
            if st.button(f"🔒 Validar Aposta de {match_id}", key=f"btn_{match_id}", use_container_width=True):
                st.session_state.pronos[user][match_id] = {"score1": s1_in, "score2": s2_in, "qualifie": q_in, "valide": True}
                st.toast("Aposta Registada! 🔥")
                st.rerun()
        else:
            st.markdown(f"<p style='color: #10b981;'><b>✓ Escolha:</b> {st.session_state.pronos[user][match_id]['qualifie']}</p>", unsafe_allow_html=True)
            st.markdown("<span style='color: #64748b;'>🔒 Bloqueada</span>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
