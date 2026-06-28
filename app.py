import streamlit as st
import unicodedata

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Prono Mondial 2026", page_icon="🏆", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0a1128; color: #e2e8f0; }
    .hero-banner { background: linear-gradient(135deg, #0a1128, #1b2f5e); padding: 30px; border-radius: 18px; text-align: center; border: 1px solid #2a3b6e; }
    .match-box { background: #131c33; padding: 15px; border-radius: 12px; border-left: 4px solid #e8c34a; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO BANDEIRAS ---
def get_flag(name):
    drapeaux = {"allemagne":"🇩🇪", "france":"🇫🇷", "portugal":"🇵🇹", "bresil":"🇧🇷", "espagne":"🇪🇸", "angleterre":"🏴󠁧󠁢󠁥󠁮󠁧󠁿", "argentine":"🇦🇷", "belgique":"🇧🇪", "suisse":"🇨🇭", "colombie":"🇨🇴", "mexique":"🇲🇽", "canada":"🇨🇦", "pays-bas":"🇳🇱", "maroc":"🇲🇦", "croatie":"🇭🇷", "autriche":"🇦🇹", "usa":"🇺🇸", "bosnie":"🇧🇦", "senegal":"🇸🇳", "japon":"🇯🇵", "cote d'ivoire":"🇨🇮", "norvege":"🇳🇴", "equateur":"🇪🇨", "rd congo":"🇨🇩", "cap-vert":"🇨🇻", "australie":"🇦🇺", "egypte":"🇪🇬", "algerie":"🇩🇿", "ghana":"🇬🇭", "suede":"🇸🇪", "paraguay":"🇵🇾", "afrique du sud":"🇿🇦"}
    return drapeaux.get("".join(c for c in unicodedata.normalize('NFD', str(name).lower()) if unicodedata.category(c) != 'Mn'), "🏳️")

# --- INICIALIZAÇÃO ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.pronos = {}
    st.session_state.matchs = {
        f"16es - Match {i+1}": {"team1": t1, "team2": t2, "score1": 0, "score2": 0, "termine": False}
        for i, (t1, t2) in enumerate([("Allemagne", "Paraguay"), ("France", "Suède"), ("Afrique du Sud", "Canada"), ("Pays-Bas", "Maroc"), 
        ("Portugal", "Croatie"), ("Espagne", "Autriche"), ("USA", "Bosnie"), ("Belgique", "Sénégal"), ("Brésil", "Japon"), 
        ("Côte d'Ivoire", "Norvège"), ("Mexique", "Équateur"), ("Angleterre", "RD Congo"), ("Argentine", "Cap-Vert"), 
        ("Australie", "Égypte"), ("Suisse", "Algérie"), ("Colombie", "Ghana")])
    }

# --- LOGIN ---
if not st.session_state.user_authenticated:
    st.markdown("<div class='hero-banner'><h1>🏆 COUPE DU MONDE 2026</h1></div>", unsafe_allow_html=True)
    email = st.text_input("Email")
    nick = st.text_input("Pseudo")
    code = st.text_input("Código", type="password")
    if st.button("Entrar"):
        if code == "LoungeCDM":
            st.session_state.user_authenticated = True
            st.session_state.user_email = email
            st.session_state.user_nickname = nick
            st.rerun()
else:
    st.sidebar.title(f"👤 {st.session_state.user_nickname}")
    menu = st.sidebar.radio("Navegação", ["⚽ Pronósticos", "📊 Classificação", "🌳 Playoffs", "🛠️ Admin", "⚙️ Sair"])

    if menu == "⚽ Pronósticos":
        st.title("⚽ Meus Pronósticos")
        for mid, info in st.session_state.matchs.items():
            st.markdown(f"<div class='match-box'><b>{mid}</b> | {get_flag(info['team1'])} {info['team1']} vs {get_flag(info['team2'])} {info['team2']}</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.number_input(f"Golos {info['team1']}", 0, key=f"s1_{mid}")
            c2.number_input(f"Golos {info['team2']}", 0, key=f"s2_{mid}")

    elif menu == "📊 Classificação":
        st.title("📊 Classificação")
        st.info("A tabela será preenchida conforme os resultados forem inseridos.")

    elif menu == "🌳 Playoffs":
        st.title("🌳 Árvore do Torneio")
        st.write("Acompanhamento das fases até à final.")

    elif menu == "🛠️ Admin":
        # ALTERA AQUI O TEU EMAIL
        if st.session_state.user_email == "teu-email@exemplo.com":
            st.title("🛠️ Painel Admin")
            mid = st.selectbox("Escolher jogo", list(st.session_state.matchs.keys()))
            res1 = st.number_input("Resultado Real E1", 0)
            res2 = st.number_input("Resultado Real E2", 0)
            if st.button("Atualizar Resultado"):
                st.success(f"Resultado de {mid} atualizado!")
        else:
            st.error("Acesso negado.")

    elif menu == "⚙️ Sair":
        if st.checkbox("Confirmo que quero apagar os meus dados e sair"):
            if st.button("Apagar e Sair"):
                st.session_state.user_authenticated = False
                st.rerun()
