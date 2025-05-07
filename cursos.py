import streamlit as st
#from streamlit_extras.stylable_container import stylable_container

# Tópicos da trilha com descrições
TOPICOS = [
    {
        "titulo": "Fundamentos de Programação",
        "descricao": "Explore Python, Git, algoritmos e estruturas de dados essenciais para IA."
    },
    {
        "titulo": "Matemática para IA",
        "descricao": "Aprenda álgebra linear, cálculo, estatística e otimização aplicados à IA."
    },
    {
        "titulo": "Fundamentos de Machine Learning",
        "descricao": "Domine modelos supervisionados, avaliação, overfitting e feature engineering."
    },
    {
        "titulo": "Deep Learning",
        "descricao": "Estude redes neurais, CNNs, Transformers e os principais frameworks."
    },
    {
        "titulo": "Engenharia de Prompt e LLMs",
        "descricao": "Entenda técnicas de prompting, OpenAI, RAG e LangChain."
    },
    {
        "titulo": "Implantação e MLOps",
        "descricao": "Implemente projetos com Streamlit, FastAPI, CI/CD e monitore modelos em produção."
    },
    {
        "titulo": "Projetos Práticos",
        "descricao": "Aplique IA em projetos reais como classificadores, chatbots e sistemas de recomendação."
    },
]

ESTADOS = ["Pendente", "Em andamento", "Concluído"]


def exibir_trilha_interativa():
    st.header("🧠 Trilha Engenheiro AI")
    st.markdown("Bem-vindo à sua jornada para se tornar um especialista em Inteligência Artificial Aplicada!")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("📌 Tópicos")
        for i, topico in enumerate(TOPICOS):
            if st.button(topico["titulo"], key=f"botao_topico_{i}"):
                st.session_state.topico_selecionado = i

    with col2:
        if "topico_selecionado" in st.session_state:
            i = st.session_state.topico_selecionado
            topico = TOPICOS[i]
            st.subheader(f"📝 {topico['titulo']}")
            st.markdown(topico["descricao"])

            estado = st.selectbox("📍 Marcar progresso:", ESTADOS, key=f"estado_{i}")
            st.session_state[f"estado_topico_{i}"] = estado

            st.markdown(f"**Status atual:** `{estado}`")


def main():
    st.title("🚀 Cursos em Andamento")

    if "curso_ativo" not in st.session_state:
        st.session_state["curso_ativo"] = None

    if st.session_state["curso_ativo"] is None:
        st.markdown("Escolha um curso para explorar sua trilha de aprendizado.")
        if st.button("🧠 Engenheiro AI", use_container_width=True):
            st.session_state["curso_ativo"] = "engenheiro_ai"
            st.rerun()

    elif st.session_state["curso_ativo"] == "engenheiro_ai":
        if st.button("🔙 Voltar ao Portal"):
            st.query_params.clear()
            st.session_state["curso_ativo"] = None
            st.rerun()
        exibir_trilha_interativa()


if __name__ == "__main__":
    main()



#def main():

 #   st.title("🧠 Trilha Engenheiro AI")
 #   st.markdown("""
 #   Bem-vindo à sua jornada para se tornar um especialista em **Inteligência Artificial Aplicada**!

 #   Esta trilha irá guiá-lo do nível básico ao avançado, utilizando ferramentas, modelos prontos e integração com APIs para acelerar projetos reais.

    ### 📌 Tópicos sugeridos:
#    - Fundamentos de IA e Machine Learning
#    - Uso prático de APIs da OpenAI
#    - Automatização de fluxos com IA
#    - Projetos com visão computacional e NLP
#    - Engenharia de prompts e Assistants

#    👉 Escolha o próximo módulo no menu lateral para começar!
#    """)
#    st.title("🚀 Cursos em Andamento")
#    st.markdown("Escolha um curso para explorar sua trilha de aprendizado.")

