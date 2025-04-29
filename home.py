import streamlit as st

# Configuração inicial
def main():
    st.set_page_config(page_title="Portal de Programas", layout="wide")

    # Detectar a página
    page = st.query_params.get("page")

    # Carregar o CSS externo
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Se está dentro de um app, mostra botão para voltar
    if page in ["udemy", "financeiro"]:
        if st.button("⬅️ Voltar ao Portal"):
            st.query_params.clear()
            st.experimental_rerun()

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
            if st.button("📚 Udemy Practice Test", key="udemy_button", use_container_width=True):
                st.query_params.update({"page": "udemy"})
                st.experimental_rerun()

        with col2:
            if st.button("💰 Planejamento Financeiro", key="financeiro_button", use_container_width=True):
                st.query_params.update({"page": "financeiro"})
                st.experimental_rerun()

if __name__ == "__main__":
    main()
