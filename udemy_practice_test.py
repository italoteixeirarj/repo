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


CSV_HEADER = [
    "Question", "Question Type",
    "Answer Option 1", "Explanation 1",
    "Answer Option 2", "Explanation 2",
    "Answer Option 3", "Explanation 3",
    "Answer Option 4", "Explanation 4",
    "Answer Option 5", "Explanation 5",
    "Answer Option 6", "Explanation 6",
    "Correct Answers", "Overall Explanation", "Domain"
]

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
        if st.button("✉️ Gerar Course Messages", use_container_width=True):
            st.session_state["aba_udemy"] = "mensagens"
    with col5:
        if st.button("📑 Gerar Questões", use_container_width=True):
            st.session_state["aba_udemy"] = "questoes"

    aba = st.session_state.get("aba_udemy", "questoes")

    if aba == "questoes":
        nome_arquivo = st.text_input("Nome do Practice Test (sem espaços):")
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
                    gerar_csv_udemy(texto, nome_arquivo)

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

# === FUNÇÕES EXISTENTES ===

def processar_questoes(texto, origem):
    questoes = []
    blocos = re.split(r'Question \d+', texto)

    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco:
            continue

        linhas = bloco.split("\n")
        pergunta = ""
        opcoes = []
        respostas_corretas = []
        explicacao = ""
        captura_explicacao = False
        encontrou_true_false = False

        for i, linha in enumerate(linhas):
            linha = linha.strip()

            if i == 0 and linha.lower() == 'skipped':
                continue

            if i == 1 and linha != '':
                pergunta = linha
                continue

            if linha.lower() in [
                'choose the correct answer.',
                'there are two correct answers.',
                'there are three correct answers.',
                'there are four correct answers.',
                'there are five correct answers.'
            ]:
                continue

            if linha.lower().startswith('correct answer') or linha.lower().startswith('correct selection'):
                try:
                    resposta = linhas[i+1].strip()
                    if resposta:
                        respostas_corretas.append(resposta)
                except:
                    pass

            elif linha.lower().startswith('overall explanation'):
                captura_explicacao = True

            elif captura_explicacao:
                explicacao += linha + " "

            else:
                if linha and not linha.lower().startswith('note') and not linha.lower().startswith('skipped'):
                    if linha.lower() in ['true', 'false']:
                        encontrou_true_false = True
                    opcoes.append(linha)

        if encontrou_true_false and not opcoes:
            opcoes = ["True", "False"]

        if not pergunta.strip() or all(not alt.strip() for alt in opcoes):
            continue

        while len(opcoes) < 5:
            opcoes.append("")

        pergunta_formatada = pergunta
        if len(respostas_corretas) > 1:
            pergunta_formatada += f" ({len(respostas_corretas)} correct)"

        questoes.append({
            "Pergunta": pergunta_formatada,
            "Opção A": opcoes[0],
            "Opção B": opcoes[1],
            "Opção C": opcoes[2],
            "Opção D": opcoes[3],
            "Opção E": opcoes[4],
            "Resposta(s) Correta(s)": "; ".join(respostas_corretas),
            "Explicação": explicacao.strip(),
            "Origem": origem
        })

    return questoes

def gerar_xlsx(questoes, nome_arquivo):
    output = io.BytesIO()
    df_final = pd.DataFrame(questoes)
    df_final = df_final.sort_values(by="Pergunta").reset_index(drop=True)

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Questões')
        worksheet = writer.sheets['Questões']
        header_fill = PatternFill(start_color="B7DEE8", end_color="B7DEE8", fill_type="solid")
        for col_num, _ in enumerate(df_final.columns, 1):
            col_letter = get_column_letter(col_num)
            worksheet[f"{col_letter}1"].fill = header_fill

    st.success(f"✅ {len(df_final)} questões geradas com sucesso!")

    st.download_button(
        label="📥 Baixar XLSX",
        data=output.getvalue(),
        file_name=f"{nome_arquivo}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def gerar_csv_udemy(texto, nome_arquivo):
    output = io.StringIO()
    questions = []

    blocks = re.split(r"(?=Question \d+\n)", texto.strip())

    for block in blocks:
        lines = block.strip().splitlines()
        if not lines or not lines[0].startswith("Question"):
            continue

        question_text = ""
        answers = []
        correct_indexes = []
        in_question = False

        for i, line in enumerate(lines):
            line = line.strip()

            if re.match(r"^Question \d+", line):
                in_question = True
                continue

            if in_question and not question_text and line and line.upper() != "SKIPPED":
                question_text = line
                continue

            if "Correct answer" in line or "Correct selection" in line:
                if i + 1 < len(lines):
                    answer_text = lines[i + 1].strip()
                    if answer_text not in answers:
                        answers.append(answer_text)
                    correct_indexes.append(answers.index(answer_text) + 1)
            elif line and not line.startswith("Overall explanation") and not line.startswith("Skipped") and not any(kw in line for kw in ["Correct answer", "Correct selection"]):
                if line not in answers:
                    answers.append(line)

        question_type = "multi-select" if len(correct_indexes) > 1 else "multiple-choice"

        qdata = {
            "Question": question_text,
            "Question Type": question_type,
            "Correct Answers": ",".join(map(str, correct_indexes)),
            "Overall Explanation": "",
            "Domain": ""
        }

        for i in range(6):
            qdata[f"Answer Option {i+1}"] = answers[i] if i < len(answers) else ""
            qdata[f"Explanation {i+1}"] = ""

        questions.append(qdata)

    df_csv = pd.DataFrame(questions, columns=CSV_HEADER)

    df_csv.to_csv(output, index=False)

    st.success(f"✅ {len(df_csv)} questões processadas para CSV!")

    st.download_button(
        label="📥 Baixar CSV para Udemy",
        data=output.getvalue(),
        file_name=f"{nome_arquivo}.csv",
        mime="text/csv"
    )

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
        caminho = f"text/messages_{campo}.md"
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