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

def gerar_nome_base(origem):
    return origem.lower().replace("practice test", "practice").replace(" ", "")

def main():
    st.title("📚 Udemy Practice Test Manager")

    opcao = st.radio("Escolha uma opção:", ["Gerar nova planilha", "Agregar planilhas existentes"])

    if opcao == "Gerar nova planilha":
        origem = st.text_input("Digite de qual Practice Test essas questões pertencem (ex: Practice Test 1):")
        texto = st.text_area("Cole aqui o conteúdo das questões e finalize digitando FIM")

        formato_exportacao = st.selectbox("Escolha o formato de exportação:", ("Excel (.xlsx)", "CSV (.csv)", "Ambos"))

        if st.button("Gerar Arquivos"):
            if texto and origem:
                questoes = processar_questoes(texto, origem)
                nome_base = gerar_nome_base(origem)

                output_xlsx = io.BytesIO()
                output_csv = io.BytesIO()

                df = pd.DataFrame(questoes)

                if formato_exportacao in ["Excel (.xlsx)", "Ambos"]:
                    with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    st.download_button("📥 Baixar Excel", data=output_xlsx.getvalue(), file_name=f"{nome_base}.xlsx")

                if formato_exportacao in ["CSV (.csv)", "Ambos"]:
                    csv_data = []
                    for questao in questoes:
                        respostas = [questao["Opção A"], questao["Opção B"], questao["Opção C"], questao["Opção D"], questao["Opção E"]]
                        alternativas_corretas = []
                        for idx, resposta in enumerate(respostas):
                            if resposta in questao["Resposta(s) Correta(s)"]:
                                alternativas_corretas.append(chr(65 + idx))
                        csv_data.append({
                            "Question Title": questao["Pergunta"],
                            "Question Text": questao["Pergunta"],
                            "Answer 1": questao["Opção A"],
                            "Answer 2": questao["Opção B"],
                            "Answer 3": questao["Opção C"],
                            "Answer 4": questao["Opção D"],
                            "Answer 5": questao["Opção E"],
                            "Multiple Correct": "True" if len(alternativas_corretas) > 1 else "False",
                            "Correct Answer(s)": ";".join(alternativas_corretas),
                            "Explanation": questao["Explicação"]
                        })

                    df_csv = pd.DataFrame(csv_data)
                    df_csv.to_csv(output_csv, index=False, encoding='utf-8-sig')
                    st.download_button("📥 Baixar CSV", data=output_csv.getvalue(), file_name=f"{nome_base}.csv")

                st.success(f"✅ Arquivos gerados com sucesso! Total de questões: {len(questoes)}")
            else:
                st.warning("⚠️ Por favor, preencha todos os campos!")

    elif opcao == "Agregar planilhas existentes":
        arquivos = st.file_uploader("Envie as planilhas (.xlsx) para agregar", type=["xlsx"], accept_multiple_files=True)
        if arquivos:
            if st.button("Agregar Planilhas"):
                frames = []
                for file in arquivos:
                    df = pd.read_excel(file)
                    frames.append(df)
                df_final = pd.concat(frames, ignore_index=True)
                output_final = io.BytesIO()
                with pd.ExcelWriter(output_final, engine='openpyxl') as writer:
                    df_final.to_excel(writer, index=False)
                st.download_button("📥 Baixar Planilha Agregada", data=output_final.getvalue(), file_name="todas_questoes.xlsx")
                st.success(f"✅ Planilhas agregadas com sucesso! Total de questões: {len(df_final)}")