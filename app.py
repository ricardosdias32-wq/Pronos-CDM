import streamlit as st
import unicodedata

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Prono Mondial", page_icon="🏆", layout="wide")

# --- FUNÇÃO PARA CRIAR DADOS DE JOGO NOVOS ---
def get_default_matchs():
    return {
        "16es - Match 1": {"team1": "Allemagne", "flag1": "🇩🇪", "team2": "Paraguay", "flag2": "🇵🇾", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        "Finale": {"team1": "À Définir", "flag1": "🏳️", "team2": "À Définir", "flag2": "🏳️", "score1_reel": 0, "score2_reel": 0, "qualifie_reel": "À Définir", "termine": False},
        # ... (podes adicionar aqui todos os outros jogos como no modelo anterior)
    }

# --- INITIALISATION ---
if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "Sala_Principal": {"matchs": get_default_matchs(), "pronos": {}},
        "Sala_Teste": {"matchs": get_default_matchs(), "pronos": {}}
    }

if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.room_id = None

# --- LOGIN ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align: center;'>🏆 Bem-vindo ao Prono Mondial</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    nickname = st.text_input("Nickname")
    code = st.text_input("Código de Acesso", type="password")
    
    if st.button("🌟 Entrar"):
        if code == "LoungeCDM":
            st.session_state.room_id = "Sala_Principal"
            st.session_state.user_authenticated = True
        elif code == "TesteSecreto123": # O TEU CÓDIGO PRIVADO
            st.session_state.room_id = "Sala_Teste"
            st.session_state.user_authenticated = True
        else:
            st.error("Código incorreto.")
            st.stop()
        
        st.session_state.user_email = email
        st.session_state.user_nickname = nickname
        st.session_state.is_admin = (email.lower() == "ricardosdias32@gmail.com")
        st.rerun()

else:
    # --- ACESSO AOS DADOS DA SALA ---
    room_id = st.session_state.room_id
    # Shortcut para facilitar o código restante
    matchs = st.session_state.rooms[room_id]["matchs"]
    pronos = st.session_state.rooms[room_id]["pronos"]
    
    # Exemplo de uso:
    st.sidebar.info(f"📍 Estás na: {room_id.replace('_', ' ')}")
    
    # AQUI CONTINUAS O TEU CÓDIGO NORMAL (menus, lógica, admin)
    # Sempre que quiseres aceder aos jogos, usas a variável 'matchs'
    # Sempre que quiseres aceder às apostas, usas a variável 'pronos'
    
    if st.sidebar.button("🚪 Sair"):
        st.session_state.user_authenticated = False
        st.rerun()
        
    st.write(f"Bem-vindo {st.session_state.user_nickname}!")
    st.write(f"Aqui podes ver e editar os jogos da **{room_id}**.")
