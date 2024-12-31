import streamlit as st

# Função para realizar os cálculos diretamente no Streamlit
def realizar_calculos(valor_total_produto, valor_total_nota, quantidade, valor_unitario):
    desconto_em_porcentagem = 1 - (valor_total_nota / valor_total_produto)
    valor_unitario_com_desconto = -(valor_unitario * (desconto_em_porcentagem - 1))
    valor_total_sem_desconto = quantidade * valor_unitario
    valor_total_com_desconto = quantidade * valor_unitario_com_desconto
    usar_no_desconto = valor_total_sem_desconto - valor_total_com_desconto

    return {
        "desconto_em_porcentagem": round(desconto_em_porcentagem * 100, 2),
        "valor_unitario_com_desconto": f"R$ {valor_unitario_com_desconto:.2f}",
        "usar_no_desconto": f"R$ {usar_no_desconto:.2f}",
        "valor_total_com_desconto": f"R$ {valor_total_com_desconto:.2f}",
        "valor_total_sem_desconto": f"R$ {valor_total_sem_desconto:.2f}",
    }

# Configuração da interface do Streamlit
st.title("Calculadora de Descontos")

# Entradas do usuário
valor_total_produto = st.number_input("Valor Total Produto (R$)", min_value=0.0, format="%.2f")
valor_total_nota = st.number_input("Valor Total Nota (R$)", min_value=0.0, format="%.2f")
quantidade = st.number_input("Quantidade", min_value=1, step=1)
valor_unitario = st.number_input("Valor Unitário (R$)", min_value=0.0, format="%.2f")

# Botão para realizar os cálculos
if st.button("Calcular"):
    # Realizar os cálculos e exibir os resultados
    resultado = realizar_calculos(valor_total_produto, valor_total_nota, quantidade, valor_unitario)
    st.write(f"**Desconto (%):** {resultado['desconto_em_porcentagem']}%")
    st.write(f"**Valor Unitário com Desconto:** {resultado['valor_unitario_com_desconto']}")
    st.write(f"**Usar no Desconto:** {resultado['usar_no_desconto']}")
    st.write(f"**Valor Total com Desconto:** {resultado['valor_total_com_desconto']}")
    st.write(f"**Valor Total sem Desconto:** {resultado['valor_total_sem_desconto']}")
