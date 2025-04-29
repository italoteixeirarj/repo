import streamlit as st

# Configuração inicial
st.set_page_config(page_title="Portal de Programas", layout="wide")

# Detectar a página
page = st.query_params.get("page")

# Carregar o CSS externo
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Se tem parâmetro de página, carrega o app correto
if page == "udemy":
    import udemy_practice_test
    udemy_practice_test.main()

elif page == "financeiro":
    import planejamento_financeiro
    planejamento_financeiro.main()

else:
    # Portal Principal
    st.title("🛠️ Portal de Programas")

    st.markdown("<div class='tile-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<div class='tile' onclick=\"window.location.search='?page=udemy'\">📚 Udemy Practice Test</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div class='tile' onclick=\"window.location.search='?page=financeiro'\">💰 Planejamento Financeiro</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
