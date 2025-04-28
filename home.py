import streamlit as st

def main():
    st.set_page_config(page_title="Portal de Programas", layout="wide")
    st.title("🛠️ Portal de Programas")

    # Carregar o CSS externo
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("<div class='tile-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.markdown("<div class='tile' onclick=\"window.location.href='?page=udemy'\">📚 Udemy Practice Test</div>", unsafe_allow_html=True):
            pass

    with col2:
        if st.markdown("<div class='tile' onclick=\"window.location.href='?page=financeiro'\">💰 Planejamento Financeiro</div>", unsafe_allow_html=True):
            pass

    st.markdown("</div>", unsafe_allow_html=True)

    # Controle de navegação simulada
    if st.experimental_get_query_params().get("page") == ["udemy"]:
        import udemy_practice_test
        udemy_practice_test.main()
    elif st.experimental_get_query_params().get("page") == ["financeiro"]:
        import planejamento_financeiro
        planejamento_financeiro.main()

if __name__ == "__main__":
    main()
