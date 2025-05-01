import streamlit as st
from udemy_gerador_arquivos import gerar_csv_udemy

# Configuração inicial
st.set_page_config(page_title="Portal de Programas", layout="wide")

# Carrega o CSS externo
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Detectar qual página
page = st.query_params.get("page")

# Botão de voltar (se estiver dentro de um app)
if page in ["udemy", "financeiro"]:
    if st.button("⬅️ Voltar ao Portal"):
        st.query_params.clear()
        st.rerun()

# Carregamento das aplicações
if page == "udemy":
    import udemy_practice_test
    udemy_practice_test.main()

elif page == "financeiro":
    import planejamento_financeiro
    planejamento_financeiro.main()

else:
    # Tela inicial do Portal
    st.title("🛠️ Portal de Programas")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📚 Udemy Practice Test", key="udemy_button", use_container_width=True):
            st.query_params.update({"page": "udemy"})
            st.rerun()

    with col2:
        if st.button("💰 Planejamento Financeiro", key="financeiro_button", use_container_width=True):
            st.query_params.update({"page": "financeiro"})
            st.rerun()
