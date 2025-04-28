import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def main():
    st.set_page_config(page_title="Portal de Programas", layout="wide")
    st.title("🛠️ Portal de Programas")

    # Carregar o CSS externo
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with stylable_container("tile", key="udemy_practice_test"):
            if st.button("📚 Udemy Practice Test", use_container_width=True):
                import udemy_practice_test
                udemy_practice_test.main()

    with col2:
        with stylable_container("tile", key="planejamento_financeiro"):
            if st.button("💰 Planejamento Financeiro", use_container_width=True):
                import planejamento_financeiro
                planejamento_financeiro.main()

if __name__ == "__main__":
    main()
