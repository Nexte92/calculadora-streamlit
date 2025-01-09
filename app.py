import streamlit as st

# Função para converter valores com separadores de milhares e decimais
def converter_valor(valor):
    """Converte string com separadores de milhares (ponto ou vírgula) e decimais para float."""
    try:
        # Remover separadores de milhares (pontos) e substituir vírgulas por pontos para compatibilidade com float
        valor = valor.replace(".", "").replace(",", ".")
        return float(valor)
    except ValueError:
        return None

# Função para realizar os cálculos
def realizar_calculos(valor_total_produto, valor_total_nota, quantidade, valor_unitario):
    desconto_em_porcentagem = 1 - (valor_total_nota / valor_total_produto)
    valor_unitario_com_desconto = -(valor_unitario * (desconto_em_porcentagem - 1))
    valor_total_sem_desconto = quantidade * valor_unitario
    valor_total_com_desconto = quantidade * valor_unitario_com_desconto
    usar_no_desconto = valor_total_sem_desconto - valor_total_com_desconto

    return {
        "desconto_em_porcentagem": f"{round(desconto_em_porcentagem * 100, 2):.2f}".replace(".", ","),
        "valor_unitario_com_desconto": f"R$ {valor_unitario_com_desconto:.4f}".replace(".", ","),
        "usar_no_desconto": f"R$ {usar_no_desconto:.2f}".replace(".", ","),
        "valor_total_com_desconto": f"R$ {valor_total_com_desconto:.2f}".replace(".", ","),
        "valor_total_sem_desconto": f"R$ {valor_total_sem_desconto:.2f}".replace(".", ","),
    }

# Configuração da interface do Streamlit
st.title("Calculadora de Descontos e Despesas")

# Entradas do usuário
valor_total_produto_str = st.text_input("Valor Total Produto (R$)")
valor_total_nota_str = st.text_input("Valor Total Nota (R$)")
quantidade = st.number_input("Quantidade", min_value=1, step=1)
valor_unitario_str = st.text_input("Valor Unitário (R$) com 4 casas decimais")

# Conversão dos valores
valor_total_produto = converter_valor(valor_total_produto_str)
valor_total_nota = converter_valor(valor_total_nota_str)
valor_unitario = converter_valor(valor_unitario_str)

# Botão para realizar os cálculos
if st.button("Calcular"):
    erros = []
    if valor_total_produto is None:
        erros.append("Valor Total Produto inválido. Use apenas números com vírgulas e/ou pontos.")
    if valor_total_nota is None:
        erros.append("Valor Total Nota inválido. Use apenas números com vírgulas e/ou pontos.")
    if valor_unitario is None:
        erros.append("Valor Unitário inválido. Use apenas números com vírgulas e/ou pontos.")

    if erros:
        for erro in erros:
            st.error(erro)
    else:
        # Realizar os cálculos e exibir os resultados
        resultado = realizar_calculos(valor_total_produto, valor_total_nota, quantidade, valor_unitario)
        st.write(f"**Desconto (%):** {resultado['desconto_em_porcentagem']}%")
        st.write(f"**Valor Unitário com Desconto:** {resultado['valor_unitario_com_desconto']}")
        st.write(f"**Usar no Desconto:** {resultado['usar_no_desconto']}")
        st.write(f"**Valor Total com Desconto:** {resultado['valor_total_com_desconto']}")
        st.write(f"**Valor Total sem Desconto:** {resultado['valor_total_sem_desconto']}")
