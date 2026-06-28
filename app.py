# --- LOGO APÓS O LOGIN ---
if not st.session_state.user_authenticated:
    st.markdown("<h1 style='text-align: center;'>🏆 Login Privado</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    nickname = st.text_input("Nickname")
    code_salle = st.text_input("Código de Acesso", type="password")
    
    if st.button("🌟 Entrar"):
        # Se for o código principal
        if code_salle == "LoungeCDM":
            st.session_state.room_id = "Sala_Principal"
            st.session_state.user_authenticated = True
        # Se for o teu código secreto de teste
        elif code_salle == "MeuCodigoSecreto123":
            st.session_state.room_id = "Sala_Teste"
            st.session_state.user_authenticated = True
        else:
            st.error("Código incorreto.")
            st.stop()
            
        # Inicializa a estrutura se for a primeira vez que a sala é usada
        if "rooms" not in st.session_state:
            st.session_state.rooms = {
                "Sala_Principal": {"matchs": get_default_matchs(), "pronos": {}},
                "Sala_Teste": {"matchs": get_default_matchs(), "pronos": {}}
            }
            
        st.session_state.user_email = email
        st.session_state.user_nickname = nickname
        st.session_state.is_admin = (email.lower() == "ricardosdias32@gmail.com")
        st.rerun()
