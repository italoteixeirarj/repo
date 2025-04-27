import pandas as pd
import re
import io
import streamlit as st

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

        while len(opcoes) < 6:
            opcoes.append("")

        questoes.append({
            "Pergunta": pergunta,
            "Opções": opcoes,
            "Respostas Corretas": respostas_corretas,
            "Explicação": explicacao.strip(),
            "Origem": origem
        })

    return questoes

def gerar_nome_base(origem):
    return origem.lower().replace("practice test", "practice").replace(" ", "")

def main():
    st.title("📚 Gerador de CSV para Udemy")

    origem = st.text_input("Digite de qual Practice Test essas questões pertencem (ex: Practice Test 1):")
    texto = st.text_area("Cole o conteúdo das questões aqui:")

    if st.button("Gerar Arquivos"):
        if texto and origem:
            questoes = processar_questoes(texto, origem)
            nome_base = gerar_nome_base(origem)

            output_csv = io.BytesIO()

            csv_data = []
            for questao in questoes:
                alternativas_corretas = []
                for idx, resposta in enumerate(questao["Opções"]):
                    if resposta in questao["Respostas Corretas"]:
                        alternativas_corretas.append(str(idx + 1))

                csv_data.append({
                    "Question": questao["Pergunta"],
                    "Question Type": "multiple-choice" if len(alternativas_corretas) == 1 else "multi-select",
                    "Answer Option 1": questao["Opções"][0],
                    "Answer Option 2": questao["Opções"][1],
                    "Answer Option 3": questao["Opções"][2],
                    "Answer Option 4": questao["Opções"][3],
                    "Answer Option 5": questao["Opções"][4],
                    "Answer Option 6": questao["Opções"][5],
                    "Explanation 1": "",
                    "Explanation 2": "",
                    "Explanation 3": "",
                    "Explanation 4": "",
                    "Explanation 5": "",
                    "Explanation 6": "",
                    "Correct Answers": ";".join(alternativas_corretas),
                    "Overall Explanation": questao["Explicação"],
                    "Domain": ""
                })

            df_csv = pd.DataFrame(csv_data)
            df_csv.to_csv(output_csv, index=False, encoding='utf-8-sig')
            st.download_button("📥 Baixar CSV para Udemy", data=output_csv.getvalue(), file_name=f"{nome_base}.csv")
            st.success(f"✅ CSV gerado com sucesso! Total de questões: {len(questoes)}")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos!")
