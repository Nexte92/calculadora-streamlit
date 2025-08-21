import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Financeira",
    page_icon="🧮",
    layout="centered"
)

# --- FUNÇÕES AUXILIARES ---

def formatar_valor(valor, prefixo="R$ ", casas_decimais=2):
    """Formata um número para o padrão monetário brasileiro (ex: R$ 1.234,56)."""
    try:
        return f"{prefixo}{valor:,.{casas_decimais}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return f"{prefixo}0,00"

def converter_para_float(valor_str):
    """Converte uma string de valor monetário brasileiro para float."""
    if not valor_str or not isinstance(valor_str, str):
        return 0.0
    try:
        # Remove "R$" e espaços, depois substitui pontos de milhar e a vírgula decimal
        valor_limpo = valor_str.replace("R$", "").strip().replace(".", "").replace(",", ".")
        return float(valor_limpo)
    except ValueError:
        st.error(f"O valor '{valor_str}' é inválido. Por favor, use apenas números, pontos e vírgulas.")
        return None


# --- PÁGINA 1: CALCULADORA DE DESCONTOS ---

def pagina_calculadora_descontos():
    """Exibe a interface e a lógica para a calculadora de descontos."""
    st.header("Calculadora de Descontos e Despesas", divider="blue")

    # Inicializa o session_state para guardar os resultados
    if 'desconto_por_peca' not in st.session_state:
        st.session_state.desconto_por_peca = 0
    if 'calculo_feito' not in st.session_state:
        st.session_state.calculo_feito = False
    if 'resultados' not in st.session_state:
        st.session_state.resultados = {}


    with st.form("calculo_desconto_form"):
        # Entradas do usuário com colunas para melhor layout
        col1, col2 = st.columns(2)
        with col1:
            valor_total_produto_str = st.text_input("Valor Total do Produto (R$)", "0,00")
            quantidade_str = st.text_input("Quantidade", "1")
        with col2:
            valor_total_nota_str = st.text_input("Valor Total da Nota (R$)", "0,00")
            valor_unitario_str = st.text_input("Valor Unitário (R$) com 4 casas", "0,0000")

        submitted = st.form_submit_button("Calcular Desconto", type="primary", use_container_width=True)

        if submitted:
            # Conversão e validação dos valores
            valor_total_produto = converter_para_float(valor_total_produto_str)
            valor_total_nota = converter_para_float(valor_total_nota_str)
            valor_unitario = converter_para_float(valor_unitario_str)
            
            try:
                quantidade = int(quantidade_str)
                if quantidade <= 0:
                    st.error("A quantidade deve ser um número inteiro maior que zero.")
                    st.session_state.calculo_feito = False
                    return
            except (ValueError, TypeError):
                st.error("A quantidade deve ser um número inteiro válido.")
                st.session_state.calculo_feito = False
                return

            if any(v is None for v in [valor_total_produto, valor_total_nota, valor_unitario]):
                st.session_state.calculo_feito = False
                return

            if valor_total_produto == 0:
                st.warning("O 'Valor Total do Produto' não pode ser zero para calcular o desconto.")
                st.session_state.calculo_feito = False
                return

            # Cálculos
            desconto_percentual = (1 - (valor_total_nota / valor_total_produto)) * 100
            valor_unitario_com_desconto = valor_unitario * (1 - (desconto_percentual / 100))
            valor_total_sem_desconto = quantidade * valor_unitario
            valor_total_com_desconto = quantidade * valor_unitario_com_desconto
            diferenca_desconto = valor_total_sem_desconto - valor_total_com_desconto
            desconto_por_peca = diferenca_desconto / quantidade if quantidade > 0 else 0

            # Armazena os resultados no session_state
            st.session_state.calculo_feito = True
            st.session_state.desconto_por_peca = desconto_por_peca
            st.session_state.resultados = {
                "desconto_percentual": f"{desconto_percentual:.2f}%".replace(".", ","),
                "valor_total_sem_desconto": formatar_valor(valor_total_sem_desconto),
                "valor_unitario_com_desconto": formatar_valor(valor_unitario_com_desconto, casas_decimais=4),
                "valor_total_com_desconto": formatar_valor(valor_total_com_desconto),
                "desconto_por_peca": formatar_valor(desconto_por_peca, casas_decimais=4),
                "diferenca_desconto": formatar_valor(diferenca_desconto)
            }

    # Exibe os resultados e o campo de devolução se o cálculo foi feito
    if st.session_state.calculo_feito:
        st.subheader("Resultados do Cálculo Inicial", divider="blue")
        res = st.session_state.resultados
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label="Desconto Aplicado (%)", value=res['desconto_percentual'])
            st.metric(label="Valor Total sem Desconto", value=res['valor_total_sem_desconto'])
        with col_res2:
            st.metric(label="Valor Unitário c/ Desconto", value=res['valor_unitario_com_desconto'])
            st.metric(label="Valor Total c/ Desconto", value=res['valor_total_com_desconto'])
        with col_res3:
            st.metric(label="Desconto por Peça", value=res['desconto_por_peca'])
            st.metric(label="Desconto Total (R$)", value=res['diferenca_desconto'])

        st.markdown("---")
        st.subheader("Cálculo para Devolução (NFD)", divider="orange")
        
        qtd_devolucao = st.number_input("Insira a 'QTD para Devolução':", min_value=0, step=1)

        if qtd_devolucao > 0:
            valor_total_desconto_nfd = qtd_devolucao * st.session_state.desconto_por_peca
            
            st.success(f"**Valor Total de Desconto:** {formatar_valor(valor_total_desconto_nfd)}")
            st.info("Usar este valor no campo 'desconto' da Nota Fiscal de Devolução (NFD).")


# --- PÁGINA 2: CÁLCULO FORNECEDOR SB ---
def pagina_calculo_fornecedor():
    """Exibe a interface e a lógica para o cálculo de custo do fornecedor."""
    st.header("Cálculo de Custo de Aquisição (Fornecedor SB)", divider="green")
    st.info("Esta calculadora determina a base de cálculo do custo de um produto, somando todas as despesas.")

    with st.form("calculo_fornecedor"):
        st.write("Preencha os valores abaixo:")
        
        col1, col2 = st.columns(2)
        with col1:
            valor_nota_str = st.text_input("Valor da Nota Fiscal (R$)", "0,00")
            valor_frete_str = st.text_input("Valor do Frete (R$)", "0,00")
            valor_seguro_str = st.text_input("Seguro (R$)", "0,00")
        with col2:
            outras_despesas_str = st.text_input("Outras Despesas (R$)", "0,00")
            desconto_str = st.text_input("Desconto (R$)", "0,00")
            ipi_str = st.text_input("Valor do IPI (R$)", "0,00")

        submitted = st.form_submit_button("Calcular Custo de Aquisição", type="primary", use_container_width=True)

        if submitted:
            valores = [converter_para_float(v) for v in [valor_nota_str, valor_frete_str, valor_seguro_str, outras_despesas_str, desconto_str, ipi_str]]
            if any(v is None for v in valores):
                return

            valor_nota, valor_frete, valor_seguro, outras_despesas, desconto, ipi = valores
            base_de_calculo = (valor_nota + valor_frete + valor_seguro + outras_despesas - desconto + ipi)

            st.success("Cálculo realizado com sucesso!")
            st.metric(
                label="💰 Custo Total de Aquisição",
                value=formatar_valor(base_de_calculo),
                help="Este é o valor base para o custo do seu produto."
            )

# --- MENU PRINCIPAL E ROTEAMENTO ---
st.sidebar.title("Menu de Navegação")
st.sidebar.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=2511&auto=format&fit=crop", use_container_width=True)

paginas = {
    "Calculadora de Descontos": pagina_calculadora_descontos,
    "Cálculo Fornecedor SB": pagina_calculo_fornecedor,
}

selecao = st.sidebar.radio("Escolha a calculadora:", list(paginas.keys()))
pagina_selecionada = paginas[selecao]
pagina_selecionada()

st.sidebar.markdown("---")
st.sidebar.info("Aplicativo desenvolvido para cálculos financeiros rápidos.")
