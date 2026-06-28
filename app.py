import streamlit as st
import unicodedata

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Mundial 2026 PRO", page_icon="🏆", layout="wide")

def get_flag(team_name):
    # Dicionário expandido com todas as seleções do torneio
    drapeaux = {
        "alemanha": "🇩🇪", "paraguai": "🇵🇾", "franca": "🇫🇷", "suecia": "🇸🇪",
        "africa do sul": "🇿🇦", "canada": "🇨🇦", "paises baixos": "🇳🇱", "marrocos": "🇲🇦",
        "portugal": "🇵🇹", "croacia": "🇭🇷", "espanha": "🇪🇸", "austria": "🇦🇹",
        "eua": "🇺🇸", "bosnia e herzegovina": "🇧🇦", "belgica": "🇧🇪", "senegal": "🇸🇳",
        "brasil": "🇧🇷", "japao": "🇯🇵", "costa do marfim": "🇨🇮", "noruega": "🇳🇴",
        "mexico": "🇲🇽", "equador": "🇪🇨", "inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "dr congo": "🇨🇩",
        "argentina": "🇦🇷", "cabo verde": "🇨🇻", "australia": "🇦🇺", "egipto": "🇪🇬",
        "suica": "🇨🇭", "argelia": "🇩🇿", "colombia": "🇨🇴", "gana": "🇬🇭"
    }
    text = "".join(c for c in unicodedata.normalize('NFD', str(team_name).lower()) if unicodedata.category(c) != 'Mn')
    return drapeaux.get(text, "🏳️")

# --- ESTADO DO TORNEIO ---
if "matchs" not in st.session_state:
    # 16-avos iniciais baseados em 41212.jpg e 41214.jpg
    st.session_state.matchs = {
        "16es - M1": {"t1": "Alemanha", "t2": "Paraguai", "vencedor": None},
        "16es - M2": {"t1": "França", "t2": "Suécia", "vencedor": None},
        # ... (adiciona os outros 16 jogos aqui seguindo o padrão)
        "8es - M1": {"t1": "Venc. M1", "t2": "Venc. M2", "vencedor": None},
        "Quartos - M1": {"t1": "Venc. 8es M1", "t2": "Venc. 8es M2", "vencedor": None},
        "Final": {"t1": "Venc. Semi M1", "t2": "Venc. Semi M2", "vencedor": None}
    }

# --- INTERFACE ---
st.title("🏆 Painel do Mundial 2026")

tab1, tab2 = st.tabs(["⚽ Ver Árvore", "🛠️ Admin (Atualizar Vencedor)"])

with tab1:
    for m_id, data in st.session_state.matchs.items():
        st.markdown(f"""
        <div style='background:#111; padding:10px; border-radius:8px; margin-bottom:5px;'>
            <b>{m_id}</b>: {get_flag(data['t1'])} {data['t1']} vs {get_flag(data['t2'])} {data['t2']} | <b>Vencedor: {data['vencedor'] or 'Pendente'}</b>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.subheader("Atualizar Resultados")
    m_sel = st.selectbox("Escolher Jogo", list(st.session_state.matchs.keys()))
    vencedor = st.text_input("Nome do Vencedor que avança:")
    
    if st.button("Confirmar Vencedor"):
        st.session_state.matchs[m_sel]['vencedor'] = vencedor
        # Aqui podes adicionar lógica para o nome do vencedor passar automaticamente para o "t1" ou "t2" do jogo seguinte
        st.success(f"{vencedor} avançou na árvore!")
        st.rerun()

if st.sidebar.button("🚪 Sair"):
    st.session_state.clear()
    st.rerun()
