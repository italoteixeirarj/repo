import csv
import re
from typing import List
import pandas as pd

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

def parse_questions(raw_text: str) -> List[dict]:
    blocks = re.split(r"(?=Question \d+\n)", raw_text.strip())
    questions = []

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

    return questions

def write_csv(questions: List[dict], output_file: str):
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(questions)

if __name__ == "__main__":
    print("Cole abaixo as questões no formato original (digite 'FIM' em uma nova linha para encerrar):")
    user_lines = []
    while True:
        line = input()
        if line.strip().upper() == "FIM":
            break
        user_lines.append(line)

    raw_data = "\n".join(user_lines)
    parsed_questions = parse_questions(raw_data)

    # Criar DataFrame com todas as colunas do template Udemy
    df_full = pd.DataFrame(parsed_questions, columns=CSV_HEADER)

    # Visualizar conteúdo organizado
    print("\nPré-visualização do conteúdo a ser salvo no CSV:")
    display_cols = ["Question", "Question Type", "Correct Answers"] + [f"Answer Option {i+1}" for i in range(6)]
    print(df_full[display_cols].to_string(index=False))

    confirm = input("\nDeseja salvar o arquivo CSV? (s/n): ").strip().lower()
    if confirm == 's':
        write_csv(parsed_questions, "simulado_gerado_udemy.csv")
        print(f"\n{len(parsed_questions)} questões processadas com sucesso. Arquivo: simulado_gerado_udemy.csv")
    else:
        print("\nOperação cancelada. O arquivo CSV não foi salvo.")