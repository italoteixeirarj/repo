import streamlit as st

# Configuração inicial
def main():
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

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📚 Udemy Practice Test", key="udemy_tile", use_container_width=True):
                st.query_params.update({"page": "udemy"})

        with col2:
            if st.button("💰 Planejamento Financeiro", key="financeiro_tile", use_container_width=True):
                st.query_params.update({"page": "financeiro"})

