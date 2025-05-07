import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

MARKMAP_PATH = "./engenheiro_ai_markmap.md"  # Caminho local do arquivo .md

def render_markmap(md_file_path):
    import html
    markdown_text = Path(md_file_path).read_text(encoding="utf-8")
    markdown_escaped = html.escape(markdown_text)

    markmap_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                font-family: Arial, sans-serif;
                background: white;
            }}
            svg {{
                height: 100%;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <pre>{markdown_escaped}</pre>
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

    components.html(markmap_html, height=800, scrolling=True)


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
        st.button("🔙 Voltar ao Portal", on_click=lambda: st.session_state.update({"curso_ativo": None}))
        st.subheader("🧠 Trilha Engenheiro AI - Mapa Mental")
        render_markmap(MARKMAP_PATH)

if __name__ == "__main__":
    main()
