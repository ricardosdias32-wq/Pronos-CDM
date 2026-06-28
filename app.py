import streamlit as st
import unicodedata

# --- CONFIGURATION ---
st.set_page_config(page_title="Prono Mondial 2026", page_icon="🏆", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0a1128; color: #e2e8f0; }
    .match-box { background: #131c33; padding: 15px; border-radius: 12px; border-left: 4px solid #e8c34a; margin-bottom: 10px; }
    .hero { text-align: center; padding: 20px; color: #e8c34a; }
    </style>
""", unsafe_allow_html=True)

# --- FONCTION BANDEIRAS ---
def get_flag(name):
    d = {"allemagne":"🇩🇪", "france":"🇫🇷", "portugal":"🇵🇹", "bresil":"🇧🇷", "espagne":"🇪🇸", "angleterre":"🏴󠁧󠁢󠁥󠁮󠁧󠁿", "argentine":"🇦🇷", "belgique":"🇧🇪", "suisse":"🇨🇭", "colombie":"🇨🇴", "mexique":"🇲🇽", "canada":"🇨🇦", "pays-bas":"🇳🇱", "maroc":"🇲🇦", "croatie":"🇭🇷", "autriche":"🇦🇹", "usa":"🇺🇸", "bosnie":"🇧🇦", "senegal":"🇸🇳", "japon":"🇯🇵", "cote d'ivoire":"🇨🇮", "norvege":"🇳🇴", "equateur":"🇪🇨", "rd congo":"🇨🇩", "cap-vert":"🇨🇻", "australie":"🇦🇺", "egypte":"🇪🇬", "algerie":"🇩🇿", "ghana":"🇬🇭", "suede":"🇸🇪", "paraguay":"🇵🇾", "afrique du sud":"🇿🇦"}
    return d.get("".join(c for c in unicodedata.normalize('NFD', str(name).lower()) if unicodedata.category(c) != 'Mn'), "🏳️")

# --- INITIALISATION ---
if "pronos" not in st.session_state: st.session_state.pronos = {}
if "matchs" not in st.session_state:
    st.session_state.matchs = {
        f"Match {i+1}": {"t1": t1, "t2": t2, "r1": None, "r2": None}
        for i, (t1, t2) in enumerate([("Allemagne", "Paraguay"), ("France", "Suède"), ("Afrique du Sud", "Canada"), ("Pays-Bas", "Maroc"), 
        ("Portugal", "Croatie"), ("Espagne", "Autriche"), ("USA", "Bosnie"), ("Belgique", "Sénégal"), ("Brésil", "Japon"), 
        ("Côte d'Ivoire", "Norvège"), ("Mexique", "Équateur"), ("Angleterre", "RD Congo"), ("Argentine", "Cap-Vert"), 
        ("Australie", "Égypte"), ("Suisse", "Algérie"), ("Colombie", "Ghana")])
    }

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["⚽ Mes Pronostics", "🌳 Arbre des Résultats", "🛠️ Admin"])

# --- LOGIQUE ---
if menu == "⚽ Mes Pronostics":
    st.title("⚽ Mes Pronostics")
    for mid, m in st.session_state.matchs.items():
        cols = st.columns([2, 1, 1, 1])
        cols[0].write(f"{mid}: {get_flag(m['t1'])} {m['t1']} vs {get_flag(m['t2'])} {m['t2']}")
        p1 = cols[1].number_input(f"G1_{mid}", 0, key=f"p1_{mid}")
        p2 = cols[2].number_input(f"G2_{mid}", 0, key=f"p2_{mid}")
        if cols[3].button("Valider", key=f"v_{mid}"):
            st.session_state.pronos[mid] = (p1, p2)
            st.success("Sauvegardé!")

elif menu == "🌳 Arbre des Résultats":
    st.title("🌳 Arbre des Résultats")
    for mid, m in st.session_state.matchs.items():
        if m["r1"] is not None:
            st.markdown(f"<div class='match-box'>{mid} | {m['t1']} {m['r1']} - {m['r2']} {m['t2']}</div>", unsafe_allow_html=True)
            # Cálculo de pontos para o utilizador
            if mid in st.session_state.pronos:
                p1, p2 = st.session_state.pronos[mid]
                pts = 3 if (p1==m['r1'] and p2==m['r2']) else (1 if (p1>p2 and m['r1']>m['r2']) or (p1<p2 and m['r1']<m['r2']) or (p1==p2 and m['r1']==m['r2']) else 0)
                st.write(f"Ton pronostic ({p1}-{p2}) -> {pts} pts")
        else:
            st.write(f"{mid}: {m['t1']} vs {m['t2']} (En attente...)")

elif menu == "🛠️ Admin":
    st.title("🛠️ Admin")
    mid = st.selectbox("Match", list(st.session_state.matchs.keys()))
    r1 = st.number_input("Score Réel 1", 0)
    r2 = st.number_input("Score Réel 2", 0)
    if st.button("Publier"):
        st.session_state.matchs[mid].update({"r1": r1, "r2": r2})
        st.rerun()
