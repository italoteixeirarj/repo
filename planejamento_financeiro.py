import streamlit as st

def main():
    st.title("💰 Planejamento Financeiro")

    st.markdown("""
    Bem-vindo ao módulo de Planejamento Financeiro! 📈
    
    Aqui você poderá:
    - Criar e gerenciar seu orçamento mensal
    - Simular metas financeiras
    - Acompanhar evolução patrimonial
    - E muito mais!
    """)

    st.subheader("O que você gostaria de fazer?")
    opcao = st.selectbox("Selecione uma opção:", [
        "Criar Orçamento Mensal",
        "Simular Metas de Investimento",
        "Acompanhar Evolução Patrimonial",
        "Analisar Despesas Fixas e Variáveis"
    ])

    if opcao == "Criar Orçamento Mensal":
        st.info("🚀 Em breve: Função para criar um orçamento mensal detalhado.")
    elif opcao == "Simular Metas de Investimento":
        st.info("🚀 Em breve: Simulador para atingir metas financeiras.")
    elif opcao == "Acompanhar Evolução Patrimonial":
        st.info("🚀 Em breve: Controle de crescimento do seu patrimônio.")
    elif opcao == "Analisar Despesas Fixas e Variáveis":
        st.info("🚀 Em breve: Relatórios de despesas.")
    
    st.success("⚙️ Funcionalidades em desenvolvimento... Fique ligado!")

if __name__ == "__main__":
    main()
