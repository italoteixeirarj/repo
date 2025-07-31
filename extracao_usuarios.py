import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Transações por Usuário", layout="wide")
st.title("📊 Extração de Transações por Usuário (SM20)")

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload da planilha SM20 (formato XLSX)", type=["xlsx"])

if uploaded_file:
    try:
        # Leitura do arquivo Excel
        df = pd.read_excel(uploaded_file)

        # Nomes esperados das colunas
        col_usuario = 'Nome usuário'
        col_mensagem_completa = 'Unnamed: 3'
        col_transacao_extraida = 'Dados variáveis para mensagem'
        col_data = 'Data da criação'

        # Verificação das colunas
        colunas_necessarias = [col_usuario, col_transacao_extraida, col_mensagem_completa, col_data]
        if not all(col in df.columns for col in colunas_necessarias):
            st.error("A planilha não contém todas as colunas esperadas.")
        else:
            # Filtrar e renomear colunas
            df_filtrado = df[[col_usuario, col_transacao_extraida, col_mensagem_completa, col_data]].dropna()
            df_filtrado.columns = ['Usuário', 'Transacao', 'MensagemCompleta', 'DataCriacao']

            # Remover transações indesejadas
            df_filtrado = df_filtrado[df_filtrado['Transacao'] != 'SESSION_MANAGER']
            df_filtrado = df_filtrado[
                ~df_filtrado['MensagemCompleta'].str.contains(r'Start of transaction .* failed \(Reason=(2|3) ?\)', case=False, na=False)
            ]

            # Converter data para tipo correto
            df_filtrado['Data'] = pd.to_datetime(df_filtrado['DataCriacao']).dt.date

            # Agrupar por usuário, transação e data
            df_final = (
                df_filtrado
                .groupby(['Usuário', 'Transacao', 'Data'])
                .size()
                .reset_index(name='Quantidade de acessos')
                .sort_values(by=['Usuário', 'Data', 'Transacao'])
            )

            # Métricas
            total_transacoes = df_final['Transacao'].nunique()
            total_usuarios = df_final['Usuário'].nunique()

            col1, col2 = st.columns(2)
            col1.metric("🔢 Transações distintas utilizadas", total_transacoes)
            col2.metric("👤 Usuários distintos", total_usuarios)

            # Exibição
            st.success(f"{len(df_final)} registros de transações por data e usuário.")
            st.dataframe(df_final, use_container_width=True, hide_index=True)

            # Preparar Excel para download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, sheet_name='Transacoes por Usuario', index=False)
            output.seek(0)

            # Botão de download
            st.download_button(
                label="📥 Baixar relatório em Excel",
                data=output,
                file_name="transacoes_por_usuario.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
