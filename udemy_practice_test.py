import streamlit as st
import pandas as pd
import io
import os
import re
import csv
from datetime import datetime
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

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
        if st.button("📑 Gerar Questões", use_container_width=True):
            st.session_state["aba_udemy"] = "questoes"
    with col2:
        if st.button("🎯 Gerar Título do Curso", use_container_width=True):
            st.session_state["aba_udemy"] = "titulo"
    with col3:
        if st.button("🧠 Gerar Intended Learners", use_container_width=True):
            st.session_state["aba_udemy"] = "learners"
    with col4:
        if st.button("🖋️ Gerar Landing Page", use_container_width=True):
            st.session_state["aba_udemy"] = "landing"
    with col5:
        if st.button("✉️ Gerar Course Messages", use_container_width=True):
            st.session_state["aba_udemy"] = "mensagens"

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
        nome_cert, cod_cert = get_dados_certificacao()
        gerar_intended_learners()

    elif aba == "landing":
        nome_cert, cod_cert = get_dados_certificacao()
        gerar_landing_page()

    elif aba == "mensagens":
        nome_cert, cod_cert = get_dados_certificacao()
        gerar_course_messages()


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

def get_dados_certificacao():
    usar_dados = st.checkbox("Usar dados da seção 'Título do Curso'", value=False)
    if usar_dados and "nome_cert" in st.session_state and "cod_cert" in st.session_state:
        return st.session_state["nome_cert"], st.session_state["cod_cert"]
    else:
        nome = st.text_input("Nome da Certificação")
        cod = st.text_input("Código da Certificação")
        return nome, cod

# === FUNCIONALIDADE: Gerar Título do Curso ===

def gerar_intended_learners():
    st.subheader("🧠 Gerar Intended Learners")

    nome_cert = st.text_input("Nome da Certificação", key="nome_cert_learners")
    cod_cert = st.text_input("Código da Certificação", key="cod_cert_learners")

    if nome_cert and cod_cert:
        area = "aws" if "aws" in nome_cert.lower() else "sap" if "sap" in nome_cert.lower() else "geral"

        if area == "aws":
            aprendizados = [
                "EXAM SIMULATION: All practice tests are timed and scored (passing score is 72%) mimicking the real exam.",
                "ASSESS YOUR EXAM READINESS: Pass the exam with a great score.",
                "DETAILED EXPLANATIONS: Every question includes a detailed explanation.",
                "RANDOMIZED QUESTIONS: The questions and answers are randomized to ensure challenge.",
                "ALWAYS UP TO DATE: Content is constantly updated based on real exam feedback.",
                "REFERENCE LINKS: Help you understand AWS concepts."
            ]
            requisitos = [
                f"Students are required to have successfully passed the {nome_cert} exam.",
                f"Before assessing readiness, it's recommended to complete {nome_cert} documentation or course."
            ]
            publico = [
                f"Candidates for the {nome_cert} exam who want to pass on their first attempt.",
                "Students preparing for the exam who want to pass with confidence.",
                "IT Professionals entering AWS technical job interviews.",
                "Anyone who wants to test their skills in exam simulation."
            ]

        elif area == "sap":
            aprendizados = [
                "Practice Test 1 (30 questions)",
                "Practice Test 2 (30 questions)",
                "Practice Test 3 (30 questions)",
                "Practice Test 4 (30 questions)",
                "Practice Test 5 (35 questions)",
                "Practice Test Bonus (53 questions)"
            ]
            requisitos = ["SAP Basis"]
            publico = [
                "SAP Basis consultants",
                "SAP HANA Consultants",
                "Database Administrators for SAP HANA",
                "SAP Consultants"
            ]

        else:
            aprendizados = ["General practice test with varied questions and detailed feedback."]
            requisitos = ["No prerequisites. This course is accessible to all learners."]
            publico = ["Beginners and professionals seeking exam readiness."]

        st.markdown("---")
        st.markdown("**✅ O que os alunos aprenderão:**")
        for i, a in enumerate(aprendizados):
            st.code(a, language="")

        st.markdown("**📌 Requisitos ou pré-requisitos:**")
        for i, r in enumerate(requisitos):
            st.code(r, language="")

        st.markdown("**🎯 Público-alvo:**")
        for i, p in enumerate(publico):
            st.code(p, language="")

    else:
        st.info("🔹 Preencha os campos para gerar as sugestões.")

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

def gerar_landing_page():
    st.subheader("🖋️ Gerar Landing Page")

    nome_cert = st.text_input("Nome da Certificação", key="nome_cert_landing")
    cod_cert = st.text_input("Código da Certificação", key="cod_cert_landing")
    total_questoes = st.number_input("Quantidade total de questões", min_value=10, step=1)
    total_simulados = st.number_input("Quantidade de simulados completos", min_value=1, step=1)

    if nome_cert and cod_cert and total_questoes > 0 and total_simulados > 0:
        ano = datetime.now().year
        title = f"[{ano}] {nome_cert} [{cod_cert}]"
        subtitle = f"{nome_cert} Practice Tests [{cod_cert}] + Explanations + {total_questoes} Questions"

        if "aws" in nome_cert.lower() or "aws" in cod_cert.lower():
            modelo = carregar_template_descricao("aws_saa-c03")
        elif "sap" in nome_cert.lower() or "sap" in cod_cert.lower():
            modelo = carregar_template_descricao("sap_activate")
        else:
            modelo = carregar_template_descricao("default")

        descricao = modelo.replace("{NOME_CERT}", nome_cert)
        descricao = descricao.replace("{COD_CERT}", cod_cert)
        descricao = descricao.replace("{TOTAL_QUESTOES}", str(total_questoes))
        descricao = descricao.replace("{TOTAL_SIMULADOS}", str(total_simulados))

        st.markdown("**Título:**")
        st.code(title)
        st.markdown("**Subtítulo:**")
        st.code(subtitle)
        st.markdown("**Descrição:**")
        st.code(descricao.strip())

        st.markdown("<div style='text-align: right; font-size: 0.75rem; color: gray; font-style: italic;'>Clique para copiar</div>", unsafe_allow_html=True)
        st.components.v1.html(f"""
            <script>
                const codeBlocks = window.parent.document.querySelectorAll('[data-testid="stCodeBlock"] pre');
                codeBlocks.forEach(block => {{
                    block.onclick = function() {{
                        navigator.clipboard.writeText(block.innerText);
                    }}
                }});
            </script>
        """, height=0)
    else:
        st.info("🔹 Preencha todos os campos para gerar os textos da Landing Page.")

def gerar_course_messages():
    st.subheader("✉️ Gerar Course Messages")

    nome_cert = st.text_input("Nome da Certificação", key="nome_cert_msg")
    cod_cert = st.text_input("Código da Certificação", key="cod_cert_msg")

    if nome_cert and cod_cert:
        welcome = carregar_template_mensagem("welcome_message.md")
        congrats = carregar_template_mensagem("congrats_message.md")

        welcome = welcome.replace("{NOME_CERT}", nome_cert).replace("{COD_CERT}", cod_cert)
        congrats = congrats.replace("{NOME_CERT}", nome_cert).replace("{COD_CERT}", cod_cert)

        st.markdown("**📬 Welcome Message:**")
        st.code(welcome.strip())
        st.markdown("**🎉 Congratulations Message:**")
        st.code(congrats.strip())

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
        st.info("🔹 Preencha os dois campos para gerar as mensagens do curso.")
