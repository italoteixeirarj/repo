import streamlit as st
import pandas as pd
import io
import os
import re
import csv
from datetime import datetime
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from pathlib import Path as PathlibPath
from udemy_gerador_arquivos import processar_questoes, gerar_xlsx, gerar_csv_udemy, agregar_planilhas


# === INTERFACE PRINCIPAL ===

def main():
    st.title("📚 Udemy Practice Test Manager")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🎯 Gerar Título do Curso", use_container_width=True):
            st.session_state["aba_udemy"] = "titulo"
    with col2:
        if st.button("🧠 Gerar Intended Learners", use_container_width=True):
            st.session_state["aba_udemy"] = "learners"
    with col3:
        if st.button("🖋️ Gerar Landing Page", use_container_width=True):
            st.session_state["aba_udemy"] = "landing"
    with col4:
        if st.button("⭐ Gerar Course Messages", use_container_width=True):
            st.session_state["aba_udemy"] = "mensagens"
    with col5:
        if st.button("📑 Gerar Questões", use_container_width=True):
            st.session_state["aba_udemy"] = "questoes"

    aba = st.session_state.get("aba_udemy", "titulo")

    if aba == "questoes":
        nome_arquivo = st.selectbox("Escolha o Practice Test:", [f"practice{i}" for i in range(1, 7)])
        texto = st.text_area("Cole o conteúdo das questões:")
        formato = st.radio("Escolha o formato de exportação:", ("XLSX (Organizado)", "CSV (Importação Udemy)"))

        if st.button("Gerar Arquivo"):
            if not texto or not nome_arquivo:
                st.warning("⚠️ Por favor, preencha todos os campos.")
            else:
                if formato == "XLSX (Organizado)":
                    questoes = processar_questoes(texto, nome_arquivo)
                    gerar_xlsx(questoes, nome_arquivo)
                else:
                    csv_data, total = gerar_csv_udemy(texto)
                    st.success(f"✅ {total} questões processadas para CSV!")
                    st.download_button(
                        label="📥 Baixar CSV para Udemy",
                        data=csv_data,
                        file_name=f"{nome_arquivo}.csv",
                        mime="text/csv"
                    )

        st.divider()
        st.subheader("🗃️ Agregador de Planilhas")
        ativar_agregador = st.checkbox("Desejo agregar arquivos CSV ou XLSX")

        if ativar_agregador:
            if "uploaded_files" not in st.session_state:
                st.session_state.uploaded_files = []

            novos_uploads = st.file_uploader("Envie os arquivos para agregar", type=["xlsx", "csv"], accept_multiple_files=True)
            if novos_uploads:
                st.session_state.uploaded_files.extend(novos_uploads)

            if st.session_state.uploaded_files:
                st.markdown("### Arquivos na fila:")
                for idx, file in enumerate(st.session_state.uploaded_files):
                    st.write(f"{idx + 1}. {file.name}")

                tipo_saida = st.radio("Escolha o formato da planilha final:", ("CSV", "XLSX"))

                if st.button("🔄 Agregar Planilhas"):
                    ordered_files = sorted(st.session_state.uploaded_files, key=lambda f: f.name)
                    frames = []
                    for file in ordered_files:
                        if file.name.endswith(".xlsx"):
                            df = pd.read_excel(file)
                        elif file.name.endswith(".csv"):
                            df = pd.read_csv(file)
                        else:
                            continue
                        frames.append(df)
                    if frames:
                        df_final = pd.concat(frames, ignore_index=True)

                        if tipo_saida == "CSV":
                            buffer_csv = io.StringIO()
                            df_final.to_csv(buffer_csv, index=False)
                            st.download_button(
                                label="📥 Baixar como CSV",
                                data=buffer_csv.getvalue(),
                                file_name="planilha_agregada.csv",
                                mime="text/csv"
                            )
                        else:
                            buffer_xlsx = io.BytesIO()
                            df_final.to_excel(buffer_xlsx, index=False)
                            buffer_xlsx.seek(0)
                            st.download_button(
                                label="📥 Baixar como XLSX",
                                data=buffer_xlsx,
                                file_name="planilha_agregada.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )

    elif aba == "titulo":
        gerar_titulo_certificacao()

    elif aba == "learners":
        nome_cert, cod_cert = get_dados_certificacao("learners")
        gerar_intended_learners(nome_cert, cod_cert)

    elif aba == "landing":
        nome_cert, cod_cert = get_dados_certificacao("landing")
        gerar_landing_page(nome_cert, cod_cert)

    elif aba == "mensagens":
        nome_cert, cod_cert = get_dados_certificacao("mensagens")
        gerar_course_messages(nome_cert, cod_cert)

if __name__ == "__main__":
    main()

# === FUNCIONALIDADE: Gerar Título do Curso ===

def gerar_titulo_certificacao():
    st.subheader("🎯 Gerar Título do Curso")
    ano_atual = datetime.now().year
    nome_cert = st.text_input("Nome da Certificação", placeholder="Ex: AWS Certified Solutions Architect Associate")
    cod_cert = st.text_input("Código da Certificação", placeholder="Ex: SAA-C03")

    if nome_cert and cod_cert:
        titulo_gerado = f"[{ano_atual}] {nome_cert.strip()} [{cod_cert.strip()}]"

        if len(titulo_gerado) > 60:
            st.error("❌ O título gerado excede 60 caracteres. Tente abreviar o nome da certificação.")
        else:
            st.session_state["titulo_gerado"] = titulo_gerado
            st.session_state["nome_cert"] = nome_cert.strip()
            st.session_state["cod_cert"] = cod_cert.strip()

            st.markdown("**Título do Curso:**")
            st.code(titulo_gerado, language="")
            st.markdown("<div style='text-align: right; font-size: 0.75rem; color: gray; font-style: italic;'>Clique para copiar</div>", unsafe_allow_html=True)
            st.components.v1.html(f"""
                <script>
                    const codeBlocks = window.parent.document.querySelectorAll('[data-testid=\"stCodeBlock\"] pre');
                    codeBlocks.forEach(block => {{
                        block.onclick = function() {{
                            navigator.clipboard.writeText(block.innerText);
                        }}
                    }});
                </script>
            """, height=0)
    else:
        st.info("🔹 Preencha os dois campos para gerar o título.")

# === FUNÇÕES INTENDED LEARNERS ===

def get_dados_certificacao(scope=""):
    usar_dados = st.checkbox("Usar dados da seção 'Título do Curso'", key=f"usar_dados_{scope}")
    if usar_dados and "nome_cert" in st.session_state and "cod_cert" in st.session_state:
        return st.session_state["nome_cert"], st.session_state["cod_cert"]
    else:
        nome = st.text_input("Nome da Certificação", key=f"nome_cert_{scope}")
        cod = st.text_input("Código da Certificação", key=f"cod_cert_{scope}")
        return nome, cod

def carregar_md_personalizado(caminho, nome_cert, cod_cert):
    try:
        texto = PathlibPath(caminho).read_text(encoding="utf-8")
        return texto.replace("{course_name}", nome_cert).replace("{course_code}", cod_cert)
    except FileNotFoundError:
        return "Arquivo de template não encontrado."

def gerar_intended_learners(nome_cert, cod_cert):
    st.subheader("🧠 Gerar Intended Learners")

    if not nome_cert or not cod_cert:
        st.warning("⚠️ Preencha o nome e o código da certificação para continuar.")
        return

    textos = {
        "What will students learn in your course?": "text/intended_learn_what.md",
        "What are the requirements or prerequisites for taking your course?": "text/intended_learn_requirements.md",
        "Who is this course for?": "text/intended_learn_target.md",
    }

    for titulo, caminho in textos.items():
        st.markdown(f"### {titulo}")
        conteudo = carregar_md_personalizado(caminho, nome_cert, cod_cert)
        for linha in conteudo.strip().split("\n"):
            if linha:
                st.code(linha.strip(), language="")
                st.markdown("<div style='text-align: right; font-size: 0.75rem; color: gray; font-style: italic;'>Clique para copiar</div>", unsafe_allow_html=True)

    st.components.v1.html(f"""
        <script>
            const blocks = window.parent.document.querySelectorAll('[data-testid=\"stCodeBlock\"] pre');
            blocks.forEach(block => {{
                block.onclick = function() {{
                    navigator.clipboard.writeText(block.innerText);
                }}
            }});
        </script>
    """, height=0)

# === GERAR LANDING PAGE COM MD ===

def carregar_template_descricao(tipo):
    caminho = os.path.join(os.getcwd(), f"text/landing_{tipo}.md")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return "Descrição padrão ainda não disponível."

def carregar_template_mensagem(nome_arquivo):
    caminho = os.path.join(os.getcwd(), f"text/{nome_arquivo}")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return "Mensagem padrão ainda não disponível."

def gerar_landing_page(nome_cert, cod_cert):
    st.subheader("🖋️ Gerar Landing Page")

    if not nome_cert or not cod_cert:
        st.warning("⚠️ Preencha o nome e o código da certificação para continuar.")
        return

    titulo = st.text_input("Título do Curso", value=st.session_state.get("titulo_gerado", ""), max_chars=60)
    num_questoes = st.number_input("Número de Questões", min_value=1, step=1)
    num_testes = st.number_input("Número de Testes", min_value=1, step=1)
    total_perguntas = num_questoes * num_testes

    subtitulo_auto = f"Practice Test - {nome_cert} [{cod_cert}] + {total_perguntas} Questions"
    subtitulo = st.text_input("Subtítulo do Curso (até 120 caracteres)", value=subtitulo_auto[:120], max_chars=120)

    cod_key = cod_cert.lower().replace("-", "_")
    caminho = f"text/landing_{cod_key}.md"
    if not PathlibPath(caminho).exists():
        caminho = "text/landing_default.md"

    descricao = carregar_md_personalizado(caminho, nome_cert, cod_cert)
    descricao = descricao.replace("{NOME_CERT}", nome_cert)
    descricao = descricao.replace("{COD_CERT}", cod_cert)
    descricao = descricao.replace("{TOTAL_QUESTOES}", str(num_questoes))
    descricao = descricao.replace("{TOTAL_SIMULADOS}", str(num_testes))
    descricao = descricao.replace("{TOTAL_PERGUNTAS}", str(total_perguntas))

    st.markdown("### Course Description")
    st.code(descricao.strip(), language="markdown")
    st.markdown("<div style='text-align: right; font-size: 0.75rem; color: gray; font-style: italic;'>Clique para copiar</div>", unsafe_allow_html=True)

    st.components.v1.html(f"""
        <script>
            const desc = window.parent.document.querySelectorAll('[data-testid=\"stCodeBlock\"] pre');
            desc.forEach(block => {{
                block.onclick = function() {{
                    navigator.clipboard.writeText(block.innerText);
                }}
            }});
        </script>
    """, height=0)


def gerar_course_messages(nome_cert, cod_cert):
    st.subheader("✉️ Gerar Course Messages")

    for campo in ["welcome", "congrats"]:
        caminho = f"text/message_{campo}.md"
        if PathlibPath(caminho).exists():
            texto = carregar_md_personalizado(caminho, nome_cert, cod_cert)
            texto = texto.replace("{NOME_CERT}", nome_cert)
            texto = texto.replace("{COD_CERT}", cod_cert)
            st.markdown(f"### {campo.capitalize()} Message")
            st.code(texto.strip(), language="markdown")
            st.markdown("<div style='text-align: right; font-size: 0.75rem; color: gray; font-style: italic;'>Clique para copiar</div>", unsafe_allow_html=True)

    st.components.v1.html(f"""
        <script>
            const msgs = window.parent.document.querySelectorAll('[data-testid=\"stCodeBlock\"] pre');
            msgs.forEach(block => {{
                block.onclick = function() {{
                    navigator.clipboard.writeText(block.innerText);
                }}
            }});
        </script>
    """, height=0)