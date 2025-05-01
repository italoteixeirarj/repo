import streamlit as st
import pandas as pd
import io
import re
import csv
from datetime import datetime
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from pathlib import Path as PathlibPath
from openai import OpenAI

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

def obter_cliente_openai():
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não configurada em st.secrets.")
    return OpenAI(api_key=api_key)

def processar_questoes(texto, origem):
    questoes = []
    blocos = re.split(r'Question \d+', texto)

    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco:
            continue

        question_data = gerar_pergunta_xlsx_com_ia(bloco)
        if question_data:
            question_data["Origem"] = origem
            questoes.append(question_data)

    return questoes

def gerar_pergunta_xlsx_com_ia(bloco):
    prompt = f"""
Você é um assistente que extrai perguntas de simulados para um arquivo Excel.
A estrutura da pergunta deve ser formatada como:

Pergunta: Pergunta completa (adicione a quantidade de corretas, se houver mais de uma)
Opção A: Texto da opção A
Opção B: Texto da opção B
Opção C: Texto da opção C
Opção D: Texto da opção D
Opção E: Texto da opção E
Resposta(s) Correta(s): Texto(s) exato(s) das respostas corretas (separadas por ponto e vírgula se mais de uma)
Explicação: Texto explicando a resposta correta

A partir do seguinte bloco, extraia esses campos e me retorne em formato JSON:
{bloco.strip()}
"""

    client = obter_cliente_openai()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente para formatação de simulados em Excel."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    try:
        content = response.choices[0].message.content.strip()
        dados = eval(content) if content.startswith("{") else {}
        return dados
    except:
        return None

def gerar_xlsx(questoes, nome_arquivo):
    df = pd.DataFrame(questoes)
    caminho = f"{nome_arquivo}.xlsx"
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Questoes", index=False)
        wb = writer.book
        ws = writer.sheets["Questoes"]
        for col_num, _ in enumerate(df.columns, 1):
            col_letter = get_column_letter(col_num)
            ws.column_dimensions[col_letter].width = 30

def gerar_csv_udemy(texto):
    output = io.StringIO()
    questions = []

    blocks = re.split(r"(?=Question \d+\n)", texto.strip())

    for block in blocks:
        question_data = gerar_pergunta_csv_com_ia(block)
        if question_data:
            questions.append(question_data)

    df_csv = pd.DataFrame(questions, columns=CSV_HEADER)
    df_csv.to_csv(output, index=False)
    output.seek(0)
    return output.getvalue(), len(df_csv)

def gerar_pergunta_csv_com_ia(bloco):
    prompt = f"""
Você é um assistente que extrai perguntas de simulados no formato Udemy CSV.
A estrutura da pergunta é como no exemplo abaixo:

Question: Pergunta completa
Question Type: multiple-choice ou multi-select
Answer Option 1: Opção A
Answer Option 2: Opção B
Answer Option 3: Opção C
Answer Option 4: Opção D
Answer Option 5: Opção E (se houver)
Answer Option 6: Opção F (se houver)
Correct Answers: índice(s) da(s) opção(ões) correta(s), separados por vírgula (ex: 1,3)
Overall Explanation: Explicação detalhada
Domain: (deixe em branco)

Extraia os dados do seguinte bloco e me responda em JSON:
{bloco.strip()}
"""

    client = obter_cliente_openai()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente para formatação de simulados Udemy."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    try:
        content = response.choices[0].message.content.strip()
        dados = eval(content) if content.startswith("{") else {}
        return dados
    except:
        return None
