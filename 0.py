import streamlit as st

# Título do aplicativo
st.title("Aplicativo de Saudação")

# Campo para inserir um nome
name = st.text_input("Digite seu nome:")

# Botão para enviar o nome
if st.button("Saudar"):
    if name:
        st.write(f"Olá, {name}!")
    else:
        st.warning("Por favor, digite um nome.")

# Mensagem padrão
st.text("Insira um nome e clique no botão 'Saudar' para ver uma saudação personalizada.")
