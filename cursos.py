import streamlit as st


def exibir_trilha_engenheiro_ai():
    st.header("🧠 Trilha: Engenheiro de Inteligência Artificial")
    st.markdown("Explore os caminhos essenciais para se tornar um especialista em IA aplicada.")

    with st.expander("1. Fundamentos de Programação"):
        st.markdown("""
        - Python (básico a intermediário)
        - Git e GitHub
        - Orientação a Objetos
        - Estruturas de Dados e Algoritmos
        """)

    with st.expander("2. Matemática para IA"):
        st.markdown("""
        - Álgebra Linear
        - Cálculo
        - Estatística e Probabilidade
        - Otimização
        """)

    with st.expander("3. Fundamentos de Machine Learning"):
        st.markdown("""
        - Modelos supervisionados e não supervisionados
        - Avaliação de modelos
        - Overfitting e underfitting
        - Feature engineering
        """)

    with st.expander("4. Deep Learning"):
        st.markdown("""
        - Redes Neurais Artificiais
        - CNNs, RNNs, Transformers
        - Frameworks: TensorFlow, PyTorch
        - Treinamento em GPU e tuning de modelos
        """)

    with st.expander("5. Engenharia de Prompt e Modelos de Linguagem"):
        st.markdown("""
        - Fundamentos de LLMs
        - Técnicas de Prompting
        - OpenAI, LangChain e Assistants
        - Aplicações com RAG (retrieval-augmented generation)
        """)

    with st.expander("6. Implantação e MLOps"):
        st.markdown("""
        - Deployment com Streamlit, FastAPI, Gradio
        - Versionamento de modelos
        - Pipelines de CI/CD para ML
        - Monitoramento e testes em produção
        """)

    with st.expander("7. Projetos Práticos"):
        st.markdown("""
        - Classificação de texto e imagem
        - Chatbots com IA generativa
        - Sistemas de recomendação
        - Análise de sentimentos e dados em tempo real
        """)

def main():

    st.title("🧠 Trilha Engenheiro AI")
    st.markdown("""
    Bem-vindo à sua jornada para se tornar um especialista em **Inteligência Artificial Aplicada**!

    Esta trilha irá guiá-lo do nível básico ao avançado, utilizando ferramentas, modelos prontos e integração com APIs para acelerar projetos reais.

    ### 📌 Tópicos sugeridos:
    - Fundamentos de IA e Machine Learning
    - Uso prático de APIs da OpenAI
    - Automatização de fluxos com IA
    - Projetos com visão computacional e NLP
    - Engenharia de prompts e Assistants

    👉 Escolha o próximo módulo no menu lateral para começar!
    """)
#    st.title("🚀 Cursos em Andamento")
#    st.markdown("Escolha um curso para explorar sua trilha de aprendizado.")

    if "curso_ativo" not in st.session_state:
        st.session_state["curso_ativo"] = None

    if st.session_state["curso_ativo"] == "engenheiro_ai":
        if st.button("🔙 Voltar"):
            st.session_state["curso_ativo"] = None
            st.experimental_rerun()

        st.markdown("## 🧠 Trilha Engenheiro AI")
        exibir_trilha_engenheiro_ai()

    else:
        st.markdown("Escolha um curso para explorar sua trilha de aprendizado.")
        if st.button("🧠 Engenheiro AI", use_container_width=True):
            st.session_state["curso_ativo"] = "engenheiro_ai"
            st.experimental_rerun()

