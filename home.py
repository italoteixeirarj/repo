import streamlit as st
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(page_title="Portal de Programas", layout="centered")

st.title("🛠️ Portal de Programas")

# Menu principal usando Tiles
opcao = option_menu(
    menu_title=None,
    options=["Udemy Practice Test"],
    icons=["book"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Execução de cada programa
if opcao == "Udemy Practice Test":
    # Importa e executa o app do Practice Test
    import udemy_practice_test
    udemy_practice_test.main()
