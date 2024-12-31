import streamlit as st
import requests

st.title("Calculadora de Descontos")

# Inputs do usuário
valor_total_produto = st.number_input("Valor Total Produto", min_value=0.0, format="%.2f")
valor_total_nota = st.number_input("Valor Total Nota", min_value=0.0, format="%.2f")
quantidade = st.number_input("Quantidade", min_value=1, step=1)
valor_unitario = st.number_input("Valor Unitário", min_value=0.0, format="%.2f")

if st.button("Calcular"):
    # Enviar dados para o servidor
    payload = {
        "valor_total_produto": valor_total_produto,
        "valor_total_nota": valor_total_nota,
        "quantidade": quantidade,
        "valor_unitario": valor_unitario
    }
    response = requests.post("http://127.0.0.1:8000/calcular", json=payload)
    if response.status_code == 200:
        resultado = response.json()
        st.write(f"**Desconto (%):** {resultado['desconto_em_porcentagem']}%")
        st.write(f"**Valor Unitário com Desconto:** {resultado['valor_unitario_com_desconto']}")
        st.write(f"**Usar no Desconto:** {resultado['usar_no_desconto']}")
    else:
        st.error(f"Erro: {response.text}")
