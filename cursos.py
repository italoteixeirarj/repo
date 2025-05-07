import streamlit as st
import streamlit.components.v1 as components

# URL do HTML renderizado com Markmap
MARKMAP_URL = "./engenheiro_ai.html"  # Altere para o caminho real

def render_markmap_iframe():
    components.iframe(MARKMAP_URL, height=600, scrolling=True)

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

        st.subheader("🧠 Trilha Engenheiro AI - Mapa Mental")
        render_markmap_iframe()

if __name__ == "__main__":
    main()
