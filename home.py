import streamlit as st

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

    st.title("📚 Udemy Practice Test Manager")

    escolha = st.session_state.get("escolha", "Gerar Nova Planilha")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Gerar Nova Planilha", key="gerar_planilha"):
            st.session_state["escolha"] = "Gerar Nova Planilha"
            st.rerun()
    with col2:
        if st.button("➕ Agregar Planilhas", key="agregar_planilhas"):
            st.session_state["escolha"] = "Agregar Planilhas"
            st.rerun()

    escolha = st.session_state.get("escolha", "Gerar Nova Planilha")

    if escolha == "Gerar Nova Planilha":
        nome_arquivo = st.text_input("Nome do Practice Test (sem espaços):")
        texto = st.text_area("Cole o conteúdo das questões:")
        formato = st.radio("Escolha o formato de exportação:", ("XLSX (Organizado)", "CSV (Importação Udemy)"))

        if st.button("Gerar Arquivo"):
            if not texto or not nome_arquivo:
                st.warning("⚠️ Por favor, preencha todos os campos.")
            else:
                if formato == "XLSX (Organizado)":
                    questoes = udemy_practice_test.processar_questoes(texto, nome_arquivo)
                    udemy_practice_test.gerar_xlsx(questoes, nome_arquivo)
                else:
                    udemy_practice_test.gerar_csv_udemy(texto, nome_arquivo)

    elif escolha == "Agregar Planilhas":
        st.info("🚧 Função de agregação ainda será implementada...")

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
