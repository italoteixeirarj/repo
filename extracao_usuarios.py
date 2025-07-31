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

        # Nome das colunas conforme o padrão da planilha
        col_usuario = 'Nome usuário'
        col_mensagem_completa = 'Unnamed: 3'  # Onde está a frase com "failed (Reason=...)"
        col_transacao_extraida = 'Dados variáveis para mensagem'

        # Verificar se as colunas existem
        if col_usuario not in df.columns or col_transacao_extraida not in df.columns or col_mensagem_completa not in df.columns:
            st.error("A planilha não contém as colunas esperadas.")
        else:
            # Selecionar colunas e remover nulos
            df_filtrado = df[[col_usuario, col_transacao_extraida, col_mensagem_completa]].dropna()
            df_filtrado.columns = ['Usuário', 'Transacao', 'MensagemCompleta']

            # Remover transações indesejadas
            df_filtrado = df_filtrado[df_filtrado['Transacao'] != 'SESSION_MANAGER']
            df_filtrado = df_filtrado[
                ~df_filtrado['MensagemCompleta'].str.contains(r'Start of transaction .* failed \(Reason=(2|3) ?\)', case=False, na=False)
            ]

            # Obter dataframe final sem duplicações
            df_final = df_filtrado[['Usuário', 'Transacao']].drop_duplicates().sort_values(by=['Usuário', 'Transacao'])

            # 📈 Métricas
            total_transacoes = df_final['Transacao'].nunique()
            total_usuarios = df_final['Usuário'].nunique()

            # Mostrar métricas
            col1, col2 = st.columns(2)
            col1.metric("🔢 Transações distintas utilizadas", total_transacoes)
            col2.metric("👤 Usuários distintos", total_usuarios)

            st.success(f"{len(df_final)} registros únicos extraídos.")
            st.dataframe(df_final, use_container_width=True)

            # Preparar planilha para download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, sheet_name='Transacoes por Usuario', index=False)
            output.seek(0)

            # Botão de download
            st.download_button(
                label="📥 Baixar Excel com transações por usuário",
                data=output,
                file_name="transacoes_por_usuario.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
