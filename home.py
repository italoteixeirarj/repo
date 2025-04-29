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
