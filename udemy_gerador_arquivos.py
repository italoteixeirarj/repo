import streamlit as st
import pandas as pd
import io
import re
import csv
from datetime import datetime
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
import os
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
                    if linha.startswith("•"):
                        pergunta += "\n" + linha
                    elif linha.lower() in ['true', 'false']:
                        encontrou_true_false = True
                        opcoes.append(linha)
                    else:
                        opcoes.append(linha)

        if encontrou_true_false and not opcoes:
            opcoes = ["True", "False"]

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

    client = OpenAI()
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
