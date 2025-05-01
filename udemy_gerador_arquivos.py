import pandas as pd
import re
import csv
import io
from openpyxl import Workbook
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

def gerar_csv_udemy(texto, nome_arquivo):
    blocos = re.split(r"(?=Question \d+\n)", texto.strip())
    questions = []

    for bloco in blocos:
        linhas = bloco.strip().splitlines()
        if not linhas or not linhas[0].startswith("Question"):
            continue

        question_text = ""
        answers = []
        correct_indexes = []
        in_question = False

        for i, linha in enumerate(linhas):
            linha = linha.strip()

            if re.match(r"^Question \d+", linha):
                in_question = True
                continue

            if in_question and not question_text and linha and linha.upper() != "SKIPPED":
                question_text = linha
                continue

            if "Correct answer" in linha or "Correct selection" in linha:
                if i + 1 < len(linhas):
                    resposta = linhas[i + 1].strip()
                    if resposta not in answers:
                        answers.append(resposta)
                    correct_indexes.append(answers.index(resposta) + 1)
            elif linha and not linha.startswith("Overall explanation") and not linha.startswith("Skipped") and not any(kw in linha for kw in ["Correct answer", "Correct selection"]):
                if linha not in answers:
                    answers.append(linha)

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

    df_full = pd.DataFrame(questions, columns=CSV_HEADER)
    caminho = f"{nome_arquivo}.csv"
    df_full.to_csv(caminho, index=False, encoding="utf-8")
