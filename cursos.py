import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

MARKMAP_PATH = "./engenheiro_ai_markmap.md"  # Caminho local para seu arquivo .md

def render_markmap(md_file_path):
    markdown_text = Path(md_file_path).read_text(encoding="utf-8")

    html_content = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
      <style>
        html, body {{
          height: 100%;
          margin: 0;
          background-color: #fff;
        }}
        svg {{
          width: 100%;
          height: 100vh;
        }}
      </style>
    </head>
    <body>
      <pre>{markdown_text}</pre>
      <script>
        window.markmapAutoLoader = {{
          onReady() {{
            const els = document.querySelectorAll('pre');
            for (const el of els) {{
              window.markmap.autoLoader.default.transform(el);
            }}
          }}
        }};
      </script>
    </body>
    </html>
    """

    components.html(html_content, height=800, scrolling=True)

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
            st.session_state["curso_ativo"] = None
            st.query_params.clear()
            st.rerun()

        st.subheader("🧠 Trilha Engenheiro AI - Mapa Mental")
        render_markmap(MARKMAP_PATH)

if __name__ == "__main__":
    main()
