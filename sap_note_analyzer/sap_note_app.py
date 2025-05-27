import streamlit as st
import pandas as pd

st.title("Analisador de SAP Notes")
st.write("Insira o número da SAP Note para extrair objetos técnicos, pré-requisitos e mais.")

nota_sap = st.text_input("Número da SAP Note", "3552903")

if st.button("Analisar Nota"):
    st.success(f"Analisando SAP Note {nota_sap}...")

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

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar planilha CSV",
        data=csv,
        file_name=f"impacto_nota_{nota_sap}.csv",
        mime='text/csv',
    )
