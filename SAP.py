import streamlit as st
import pandas as pd

# Título da aplicação
st.title("Analisador de SAP Notes")
st.write("Insira o número da SAP Note para extrair objetos técnicos, pré-requisitos e mais.")

# Input do número da nota
nota_sap = st.text_input("Número da SAP Note", "3552903")

# Botão para processar
if st.button("Analisar Nota"):
    # Simulação de extração de dados da nota
    st.success(f"Analisando SAP Note {nota_sap}...")

    # Dados simulados (substituir futuramente pela integração com SAP ou parser real)
    dados = [
        {
            "Nota SAP": nota_sap,
            "Tem Pré-requisitos?": "Sim",
            "Objeto Técnico": "J_1B_NF_VALUE_DETERMINATION",
            "Tipo de Objeto": "Função (FUNCTION)",
            "Transações Impactadas": "J1B*NFE (estimado)"
        },
        {
            "Nota SAP": nota_sap,
            "Tem Pré-requisitos?": "Sim",
            "Objeto Técnico": "LJ1BB2TOP",
            "Tipo de Objeto": "Programa (REPS)",
            "Transações Impactadas": "Transações com J1B*"
        }
    ]

    df = pd.DataFrame(dados)
    st.dataframe(df)

    # Opção para exportar
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar planilha CSV",
        data=csv,
        file_name=f"impacto_nota_{nota_sap}.csv",
        mime='text/csv',
    )
