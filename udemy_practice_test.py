import streamlit as st
import pandas as pd
import re
import io

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

def gerar_nome_arquivo(origem):
    nome = origem.lower().replace("practice test", "practice").replace(" ", "") + ".xlsx"
    return nome

# Streamlit App
st.title("🚀 Gerenciador de Questões Udemy (Versão Web)")

opcao = st.radio("Escolha uma opção:", ["Gerar nova planilha", "Agregar planilhas existentes"])

if opcao == "Gerar nova planilha":
    origem = st.text_input("Digite de qual Practice Test essas questões pertencem (ex: Practice Test 1):")
    texto = st.text_area("Cole aqui o conteúdo das questões (finalize digitando FIM)")
    if st.button("Gerar Planilha"):
        if texto and origem:
            questoes = processar_questoes(texto, origem)
            df = pd.DataFrame(questoes)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            nome_arquivo = gerar_nome_arquivo(origem)
            st.success(f"✅ Planilha gerada com sucesso: {nome_arquivo}")
            st.download_button("📥 Baixar Planilha", data=output.getvalue(), file_name=nome_arquivo)
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
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False)
            st.success(f"✅ Planilha agregada com sucesso!")
            st.download_button("📥 Baixar Planilha Agregada", data=output.getvalue(), file_name="todas_questoes.xlsx")
