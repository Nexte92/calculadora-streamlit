import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Financeira Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO COMPATÍVEL COM STREAMLIT ---
st.markdown("""
<style>
    /* Reset básico */
    .main {
        padding: 2rem 3rem;
    }
    
    /* Header principal azul */
    .header-blue {
        background: linear-gradient(135deg, #1e88e5 0%, #0d47a1 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(30, 136, 229, 0.3);
    }
    
    .header-blue h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .header-blue p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Cards personalizados */
    .card-blue {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafb 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #e3f2fd;
        box-shadow: 0 4px 25px rgba(30, 136, 229, 0.1);
        margin: 1rem 0;
    }
    
    .card-result {
        background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #1e88e5;
        text-align: center;
        color: #1e88e5;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .card-success {
        background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #2e7d32;
        text-align: center;
        color: #2e7d32;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Section headers */
    .section-title {
        background: linear-gradient(135deg, #1e88e5 0%, #0d47a1 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.2);
    }
    
    /* Botões customizados */
    .stButton > button {
        background: linear-gradient(135deg, #1e88e5 0%, #0d47a1 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4) !important;
    }
    
    /* Inputs estilizados */
    .stTextInput > div > div > input {
        border: 2px solid #e3f2fd !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1e88e5 !important;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1) !important;
    }
    
    .stNumberInput > div > div > input {
        border: 2px solid #e3f2fd !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1e88e5 !important;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1) !important;
    }
    
    /* Métricas customizadas */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafb 100%) !important;
        border: 2px solid #e3f2fd !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.1) !important;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: #1e88e5 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Sidebar */
    .sidebar-header {
        background: linear-gradient(135deg, #1e88e5 0%, #0d47a1 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-left: 4px solid #1e88e5 !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%) !important;
        border-left: 4px solid #2e7d32 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%) !important;
        border-left: 4px solid #ef6c00 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #ffffff 100%) !important;
        border-left: 4px solid #d32f2f !important;
    }
</style>
""", unsafe_allow_html=True)

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
        valor_limpo = valor_str.replace("R$", "").strip().replace(".", "").replace(",", ".")
        return float(valor_limpo)
    except ValueError:
        st.error(f"❌ O valor '{valor_str}' é inválido. Use apenas números, pontos e vírgulas.")
        return None

def criar_header(titulo, subtitulo):
    """Cria um header estilizado."""
    st.markdown(f"""
    <div class="header-blue">
        <h1>{titulo}</h1>
        <p>{subtitulo}</p>
    </div>
    """, unsafe_allow_html=True)

def criar_section_header(titulo):
    """Cria um header de seção."""
    st.markdown(f"""
    <div class="section-title">
        {titulo}
    </div>
    """, unsafe_allow_html=True)

def criar_card_resultado(titulo, valor, tipo="result"):
    """Cria um card de resultado."""
    classe = f"card-{tipo}"
    st.markdown(f"""
    <div class="{classe}">
        <h3 style="margin: 0 0 0.5rem 0;">{titulo}</h3>
        <h2 style="margin: 0; font-size: 1.8rem;">{valor}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- PÁGINA 1: CALCULADORA DE DESCONTOS ---

def pagina_calculadora_descontos():
    """Exibe a interface e a lógica para a calculadora de descontos."""
    
    # Header principal
    criar_header("🧮 Calculadora de Descontos", "Calcule descontos e gerencie devoluções com precisão profissional")

    # Inicializa o session_state
    if 'desconto_por_peca' not in st.session_state:
        st.session_state.desconto_por_peca = 0
    if 'calculo_feito' not in st.session_state:
        st.session_state.calculo_feito = False
    if 'resultados' not in st.session_state:
        st.session_state.resultados = {}

    # Seção de entrada de dados
    criar_section_header("📊 Dados para Cálculo")
    
    with st.form("calculo_desconto_form"):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("**💰 Valores Principais**")
            valor_total_produto_str = st.text_input(
                "💵 Valor Total do Produto", 
                "0,00",
                help="Valor original do produto antes do desconto"
            )
            quantidade_str = st.text_input(
                "📦 Quantidade", 
                "1",
                help="Quantidade de itens"
            )
        
        with col2:
            st.markdown("**🧾 Dados da Nota**")
            valor_total_nota_str = st.text_input(
                "📋 Valor Total da Nota", 
                "0,00",
                help="Valor final que aparece na nota fiscal"
            )
            valor_unitario_str = st.text_input(
                "🔢 Valor Unitário (4 casas)", 
                "0,0000",
                help="Valor unitário com 4 casas decimais"
            )

        # Botão centralizado
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submitted = st.form_submit_button("🚀 Calcular Desconto", use_container_width=True)

        if submitted:
            # Validações
            valor_total_produto = converter_para_float(valor_total_produto_str)
            valor_total_nota = converter_para_float(valor_total_nota_str)
            valor_unitario = converter_para_float(valor_unitario_str)
            
            try:
                quantidade = int(quantidade_str)
                if quantidade <= 0:
                    st.error("⚠️ A quantidade deve ser um número inteiro maior que zero.")
                    return
            except (ValueError, TypeError):
                st.error("⚠️ A quantidade deve ser um número inteiro válido.")
                return

            if any(v is None for v in [valor_total_produto, valor_total_nota, valor_unitario]):
                return

            if valor_total_produto == 0:
                st.warning("⚠️ O 'Valor Total do Produto' não pode ser zero.")
                return

            # Cálculos
            desconto_percentual = (1 - (valor_total_nota / valor_total_produto)) * 100
            valor_unitario_com_desconto = valor_unitario * (1 - (desconto_percentual / 100))
            valor_total_sem_desconto = quantidade * valor_unitario
            valor_total_com_desconto = quantidade * valor_unitario_com_desconto
            diferenca_desconto = valor_total_sem_desconto - valor_total_com_desconto
            desconto_por_peca = diferenca_desconto / quantidade if quantidade > 0 else 0

            # Armazena os resultados
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

    # Resultados
    if st.session_state.calculo_feito:
        criar_section_header("✅ Resultados do Cálculo")
        
        res = st.session_state.resultados
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.metric("📈 Desconto (%)", res['desconto_percentual'])
            st.metric("💰 Total sem Desconto", res['valor_total_sem_desconto'])
        
        with col2:
            st.metric("🏷️ Unitário c/ Desconto", res['valor_unitario_com_desconto'])
            st.metric("💵 Total c/ Desconto", res['valor_total_com_desconto'])
        
        with col3:
            st.metric("🎯 Desconto por Peça", res['desconto_por_peca'])
            st.metric("💸 Desconto Total", res['diferenca_desconto'])

        # Devolução
        st.markdown("---")
        criar_section_header("🔄 Cálculo para Devolução (NFD)")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            qtd_devolucao = st.number_input("📦 Quantidade para Devolução:", min_value=0, step=1)
        
        with col2:
            if qtd_devolucao > 0:
                valor_total_desconto_nfd = qtd_devolucao * st.session_state.desconto_por_peca
                criar_card_resultado(
                    "💰 Valor Total de Desconto",
                    formatar_valor(valor_total_desconto_nfd),
                    "success"
                )
                st.info("Use este valor no campo 'desconto' da NFD")

# --- PÁGINA 2: CÁLCULO FORNECEDOR SB ---
def pagina_calculo_fornecedor():
    """Exibe a interface e a lógica para o cálculo de custo do fornecedor."""
    
    # Header
    criar_header("🏭 Cálculo Fornecedor SB", "Calcule custos de aquisição e gerencie descontos por peça")
    
    # Session state
    if 'calculo_peca_feito' not in st.session_state:
        st.session_state.calculo_peca_feito = False
    if 'desconto_unitario_peca' not in st.session_state:
        st.session_state.desconto_unitario_peca = 0.0
    if 'valor_unitario_final_peca' not in st.session_state:
        st.session_state.valor_unitario_final_peca = 0.0

    # Custo de Aquisição
    criar_section_header("💰 Custo de Aquisição")
    
    st.info("📋 Esta calculadora determina a base de cálculo do custo, somando todas as despesas.")

    with st.form("calculo_fornecedor"):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("**💵 Valores Principais**")
            valor_nota_str = st.text_input("📄 Valor da Nota Fiscal", "0,00")
            valor_frete_str = st.text_input("🚚 Valor do Frete", "0,00")
            valor_seguro_str = st.text_input("🛡️ Seguro", "0,00")
        
        with col2:
            st.markdown("**💸 Despesas e Descontos**")
            outras_despesas_str = st.text_input("🔧 Outras Despesas", "0,00")
            desconto_str = st.text_input("💸 Desconto", "0,00")
            ipi_str = st.text_input("📊 Valor do IPI", "0,00")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🚀 Calcular Custo", use_container_width=True)

        if submitted:
            valores = [converter_para_float(v) for v in [valor_nota_str, valor_frete_str, valor_seguro_str, outras_despesas_str, desconto_str, ipi_str]]
            if any(v is None for v in valores):
                return

            valor_nota, valor_frete, valor_seguro, outras_despesas, desconto, ipi = valores
            base_de_calculo = (valor_nota + valor_frete + valor_seguro + outras_despesas - desconto + ipi)

            criar_card_resultado(
                "💰 Custo Total de Aquisição",
                formatar_valor(base_de_calculo),
                "success"
            )
            
    # Desconto por Peça
    st.markdown("---")
    criar_section_header("🎯 Desconto por Peça")
    
    with st.form("calculo_desconto_peca_form"):
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            qtd_peca_str = st.text_input("📦 Quantidade", "1")
        with col2:
            valor_unit_str = st.text_input("💰 Valor Unitário (sem desc.)", "0,00")
        with col3:
            valor_total_desc_str = st.text_input("💸 Valor Total do Desconto", "0,00")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted_peca = st.form_submit_button("🎯 Calcular Desconto", use_container_width=True)

        if submitted_peca:
            valor_unit = converter_para_float(valor_unit_str)
            valor_total_desc = converter_para_float(valor_total_desc_str)
            
            try:
                qtd_peca = int(qtd_peca_str)
                if qtd_peca <= 0:
                    st.error("⚠️ A quantidade deve ser maior que zero.")
                    return
            except (ValueError, TypeError):
                st.error("⚠️ A quantidade deve ser um número inteiro válido.")
                return

            if valor_unit is not None and valor_total_desc is not None:
                valor_total_sem_desc = qtd_peca * valor_unit
                if valor_total_sem_desc <= 0:
                    st.warning("⚠️ O Valor Total deve ser maior que zero.")
                    return

                desconto_total = valor_total_sem_desc - valor_total_desc
                if desconto_total < 0:
                    st.warning("⚠️ O valor com desconto é maior que o original.")
                    desconto_total = 0

                desconto_por_peca = desconto_total / qtd_peca if qtd_peca > 0 else 0
                percentual_desconto = (desconto_total / valor_total_sem_desc) * 100 if valor_total_sem_desc > 0 else 0
                valor_unitario_com_desconto = valor_total_desc / qtd_peca if qtd_peca > 0 else 0

                st.session_state.calculo_peca_feito = True
                st.session_state.desconto_unitario_peca = desconto_por_peca
                st.session_state.valor_unitario_final_peca = valor_unitario_com_desconto

                col1, col2 = st.columns(2, gap="medium")
                
                with col1:
                    st.metric("💰 Total (sem desconto)", formatar_valor(valor_total_sem_desc))
                    st.metric("🎯 Desconto Unitário", formatar_valor(desconto_por_peca, casas_decimais=4))
                
                with col2:
                    st.metric("📈 Desconto (%)", f"{percentual_desconto:.2f}%".replace(".", ","))
                    st.metric("💵 Valor Unit. (c/ desc.)", formatar_valor(valor_unitario_com_desconto, casas_decimais=4))

    # Devolução
    if st.session_state.calculo_peca_feito:
        st.markdown("---")
        criar_section_header("🔄 Valor para Devolução")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            qtd_devolucao_peca = st.number_input("📦 Quantidade para devolução:", min_value=0, step=1, key="qtd_devolucao_fornecedor")
        
        with col2:
            if qtd_devolucao_peca > 0:
                valor_total_devolucao = qtd_devolucao_peca * st.session_state.valor_unitario_final_peca
                criar_card_resultado(
                    f"💰 Valor Total para Devolução ({qtd_devolucao_peca} peças)",
                    formatar_valor(valor_total_devolucao),
                    "success"
                )

# --- SIDEBAR E NAVEGAÇÃO ---
def configurar_sidebar():
    """Configura a sidebar."""
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h2 style="margin: 0;">💰 FinanceCalc</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Calculadoras Profissionais</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        st.sidebar.image(
            "https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=400&auto=format&fit=crop", 
            use_container_width=True,
            caption="🏢 Gestão Financeira"
        )
    except:
        pass
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Menu Principal")
    
    return st.sidebar.radio(
        "",
        ["🧮 Calculadora de Descontos", "🏭 Cálculo Fornecedor SB"],
        key="navegacao_principal"
    )

# --- MAIN ---
def main():
    """Função principal da aplicação."""
    selecao = configurar_sidebar()
    
    if selecao == "🧮 Calculadora de Descontos":
        pagina_calculadora_descontos()
    elif selecao == "🔄 Calculadora de Devolução NFD":
        pagina_calculadora_devolucao()
    elif selecao == "🏭 Cálculo Fornecedor SB":
        pagina_calculo_fornecedor()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.success("🚀 **FinanceCalc Pro v2.0**\n\nDesenvolvido para otimizar seus cálculos financeiros!")

if __name__ == "__main__":
    main()
