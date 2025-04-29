import streamlit as st
import pandas as pd
import io
import re
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

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


def gerar_csv_udemy(questoes, nome_arquivo):
    output = io.StringIO()
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
    df_csv.to_csv(output, index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Baixar CSV para Udemy",
        data=output.getvalue(),
        file_name=f"{nome_arquivo}.csv",
        mime="text/csv"
    )

def agregar_planilhas(files, formato, nome_arquivo):
    if formato == "XLSX (Organizado)":
        dfs = [pd.read_excel(file) for file in files]
        resultado = pd.concat(dfs, ignore_index=True)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            resultado.to_excel(writer, index=False)
        st.download_button(
            label="📥 Baixar Planilha Agregada (XLSX)",
            data=output.getvalue(),
            file_name=f"{nome_arquivo}_agregado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        dfs = [pd.read_csv(file) for file in files]
        resultado = pd.concat(dfs, ignore_index=True)
        output = io.StringIO()
        resultado.to_csv(output, index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Baixar Planilha Agregada (CSV)",
            data=output.getvalue(),
            file_name=f"{nome_arquivo}_agregado.csv",
            mime="text/csv"
        )

def main():
    st.title("📚 Udemy Practice Test Manager")

    escolha = st.session_state.get("escolha", "Gerar Nova Planilha")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Gerar Nova Planilha"):
            st.session_state["escolha"] = "Gerar Nova Planilha"
    with col2:
        if st.button("➕ Agregar Planilhas"):
            st.session_state["escolha"] = "Agregar Planilhas"

    escolha = st.session_state.get("escolha", "Gerar Nova Planilha")

    if escolha == "Gerar Nova Planilha":
        nome_arquivo = st.text_input("Nome do Practice Test (sem espaços):")
        texto = st.text_area("Cole o conteúdo das questões:")
        formato = st.radio("Escolha o formato de exportação:", ("XLSX (Organizado)", "CSV (Importação Udemy)"))

        if st.button("Gerar Arquivo"):
            if not texto or not nome_arquivo:
                st.warning("⚠️ Por favor, preencha todos os campos.")
                return

            questoes = processar_questoes(texto)

            if formato == "XLSX (Organizado)":
                gerar_xlsx(questoes, nome_arquivo)
            else:
                gerar_csv_udemy(questoes, nome_arquivo)

    elif escolha == "Agregar Planilhas":
        nome_arquivo = st.text_input("Nome do arquivo final (sem espaços):")
        formato = st.radio("Escolha o formato das planilhas a agregar:", ("XLSX (Organizado)", "CSV (Importação Udemy)"))
        files = st.file_uploader("Envie os arquivos para agregar", type=["xlsx", "csv"], accept_multiple_files=True)

        if st.button("Gerar Planilha Agregada"):
            if not files or not nome_arquivo:
                st.warning("⚠️ Por favor, envie os arquivos e defina o nome final.")
                return
            agregar_planilhas(files, formato, nome_arquivo)

if __name__ == "__main__":
    main()
#