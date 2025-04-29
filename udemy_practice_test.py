import streamlit as st
import pandas as pd
import io

def processar_questoes(texto):
    questoes = []
    blocos = texto.split('Question')

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
        })

    return questoes

def gerar_xlsx(questoes, nome_arquivo):
    df = pd.DataFrame(questoes)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
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
        st.info("🚧 Função de agregação em desenvolvimento...")

if __name__ == "__main__":
    main()
