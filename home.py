import streamlit as st
from streamlit_option_menu import option_menu

def main():
    st.set_page_config(page_title="Portal de Programas", layout="wide")
    st.title("🛠️ Portal de Programas")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📚 Udemy Practice Test", use_container_width=True):
            import udemy_practice_test
            udemy_practice_test.main()

    with col2:
        if st.button("💰 Planejamento Financeiro", use_container_width=True):
            import planejamento_financeiro
            planejamento_financeiro.main()

if __name__ == "__main__":
    main()
