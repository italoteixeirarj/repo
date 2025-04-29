import streamlit as st
import pandas as pd
import io
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
    aba = st.radio("Escolha uma funcionalidade:", [
        "Gerar Questões",
        "Gerar Título do Curso",
        "(em breve) Intended Learners",
        "(em breve) Landing Page",
        "(em breve) Course Messages"
    ])

    if aba == "Gerar Questões":
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

    elif aba == "Gerar Título do Curso":
        gerar_titulo_certificacao()

    elif aba == "(em breve) Intended Learners":
        st.info("🚧 Esta funcionalidade será implementada em breve.")

    elif aba == "(em breve) Landing Page":
        st.info("🚧 Esta funcionalidade será implementada em breve.")

    elif aba == "(em breve) Course Messages":
        st.info("🚧 Esta funcionalidade será implementada em breve.")


# === FUNCIONALIDADE: Gerar Título do Curso ===

def gerar_titulo_certificacao():
    st.subheader("🎯 Gerar Título do Curso")
    ano_atual = datetime.now().year
    nome_cert = st.text_input("Nome da Certificação", placeholder="Ex: AWS Certified Solutions Architect Associate")
    cod_cert = st.text_input("Código da Certificação", placeholder="Ex: SAA-C03")

    if nome_cert and cod_cert:
        titulo_gerado = f"[{ano_atual}] {nome_cert.strip()} [{cod_cert.strip()}]"
        st.text_input("Título Gerado", value=titulo_gerado, disabled=True)
    else:
        st.info("🔹 Preencha os dois campos para gerar o título.")


# === FUNÇÕES EXISTENTES ===

def processar_questoes(texto, origem):
    # ... (mesmo conteúdo da função atual)
    pass

def gerar_xlsx(questoes, nome_arquivo):
    # ... (mesmo conteúdo da função atual)
    pass

def gerar_csv_udemy(texto, nome_arquivo):
    # ... (mesmo conteúdo da função atual)
    pass


if __name__ == "__main__":
    main()
