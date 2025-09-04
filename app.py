import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Financeira Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    /* Estilo geral da aplicação */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Cards customizados */
    .custom-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: none;
    }
    
    .result-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    /* Títulos estilizados */
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Botões customizados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Métricas customizadas */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f6f9fc 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Inputs estilizados */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        padding: 0.7rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Sidebar estilizada */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Animações */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Dividers estilizados */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
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

def criar_card_customizado(titulo, conteudo, tipo="default"):
    """Cria um card customizado com base no tipo."""
    classes = {
        "default": "custom-card",
        "result": "result-card", 
        "success": "success-card",
        "warning": "warning-card"
    }
    
    st.markdown(f"""
    <div class="{classes.get(tipo, 'custom-card')}">
        <h3>{titulo}</h3>
        <p>{conteudo}</p>
    </div>
    """, unsafe_allow_html=True)

# --- PÁGINA 1: CALCULADORA DE DESCONTOS ---

def pagina_calculadora_descontos():
    """Exibe a interface e a lógica para a calculadora de descontos."""
    
    # Header principal
    st.markdown('<h1 class="main-title">🧮 Calculadora de Descontos</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Calcule descontos e gerencie devoluções com precisão</p>', unsafe_allow_html=True)

    # Inicializa o session_state
    if 'desconto_por_peca' not in st.session_state:
        st.session_state.desconto_por_peca = 0
    if 'calculo_feito' not in st.session_state:
        st.session_state.calculo_feito = False
    if 'resultados' not in st.session_state:
        st.session_state.resultados = {}

    # Container principal com melhor organização
    with st.container():
        st.markdown('<div class="section-header">📊 Dados para Cálculo</div>', unsafe_allow_html=True)
        
        with st.form("calculo_desconto_form"):
            # Layout em 2 colunas para melhor organização
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

            # Botão de cálculo centralizado
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submitted = st.form_submit_button(
                    "🚀 Calcular Desconto", 
                    type="primary", 
                    use_container_width=True
                )

        if submitted:
            # Validações e cálculos
            valor_total_produto = converter_para_float(valor_total_produto_str)
            valor_total_nota = converter_para_float(valor_total_nota_str)
            valor_unitario = converter_para_float(valor_unitario_str)
            
            try:
                quantidade = int(quantidade_str)
                if quantidade <= 0:
                    st.error("⚠️ A quantidade deve ser um número inteiro maior que zero.")
                    st.session_state.calculo_feito = False
                    return
            except (ValueError, TypeError):
                st.error("⚠️ A quantidade deve ser um número inteiro válido.")
                st.session_state.calculo_feito = False
                return

            if any(v is None for v in [valor_total_produto, valor_total_nota, valor_unitario]):
                st.session_state.calculo_feito = False
                return

            if valor_total_produto == 0:
                st.warning("⚠️ O 'Valor Total do Produto' não pode ser zero para calcular o desconto.")
                st.session_state.calculo_feito = False
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

    # Exibição dos resultados
    if st.session_state.calculo_feito:
        st.markdown('<div class="section-header">✅ Resultados do Cálculo</div>', unsafe_allow_html=True)
        
        res = st.session_state.resultados
        
        # Métricas organizadas em grid
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.metric(
                label="📈 Desconto Aplicado", 
                value=res['desconto_percentual'],
                help="Percentual de desconto calculado"
            )
            st.metric(
                label="💰 Total sem Desconto", 
                value=res['valor_total_sem_desconto'],
                help="Valor original sem aplicar desconto"
            )
        
        with col2:
            st.metric(
                label="🏷️ Unitário c/ Desconto", 
                value=res['valor_unitario_com_desconto'],
                help="Valor unitário após aplicar o desconto"
            )
            st.metric(
                label="💵 Total c/ Desconto", 
                value=res['valor_total_com_desconto'],
                help="Valor total com desconto aplicado"
            )
        
        with col3:
            st.metric(
                label="🎯 Desconto por Peça", 
                value=res['desconto_por_peca'],
                help="Valor do desconto unitário por item"
            )
            st.metric(
                label="💸 Desconto Total", 
                value=res['diferenca_desconto'],
                help="Valor total economizado com o desconto"
            )

        # Seção de devolução
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">🔄 Cálculo para Devolução (NFD)</div>', unsafe_allow_html=True)
        
        col_dev1, col_dev2 = st.columns([1, 2])
        
        with col_dev1:
            qtd_devolucao = st.number_input(
                "📦 Quantidade para Devolução:", 
                min_value=0, 
                step=1,
                help="Informe quantas peças serão devolvidas"
            )
        
        with col_dev2:
            if qtd_devolucao > 0:
                valor_total_desconto_nfd = qtd_devolucao * st.session_state.desconto_por_peca
                
                st.markdown(f"""
                <div class="success-card">
                    <h3>💰 Valor Total de Desconto</h3>
                    <h2>{formatar_valor(valor_total_desconto_nfd)}</h2>
                    <p>Use este valor no campo 'desconto' da NFD</p>
                </div>
                """, unsafe_allow_html=True)


# --- PÁGINA 2: CÁLCULO FORNECEDOR SB ---
def pagina_calculo_fornecedor():
    """Exibe a interface e a lógica para o cálculo de custo do fornecedor."""
    
    # Header principal
    st.markdown('<h1 class="main-title">🏭 Cálculo Fornecedor SB</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Calcule custos de aquisição e gerencie descontos por peça</p>', unsafe_allow_html=True)
    
    # Inicializa session_state
    if 'calculo_peca_feito' not in st.session_state:
        st.session_state.calculo_peca_feito = False
    if 'desconto_unitario_peca' not in st.session_state:
        st.session_state.desconto_unitario_peca = 0.0
    if 'valor_unitario_final_peca' not in st.session_state:
        st.session_state.valor_unitario_final_peca = 0.0

    # Seção 1: Cálculo de Custo de Aquisição
    st.markdown('<div class="section-header">💰 Custo de Aquisição</div>', unsafe_allow_html=True)
    
    st.info("📋 Esta calculadora determina a base de cálculo do custo de um produto, somando todas as despesas.")

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

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submitted = st.form_submit_button("🚀 Calcular Custo", type="primary", use_container_width=True)

        if submitted:
            valores = [converter_para_float(v) for v in [valor_nota_str, valor_frete_str, valor_seguro_str, outras_despesas_str, desconto_str, ipi_str]]
            if any(v is None for v in valores):
                return

            valor_nota, valor_frete, valor_seguro, outras_despesas, desconto, ipi = valores
            base_de_calculo = (valor_nota + valor_frete + valor_seguro + outras_despesas - desconto + ipi)

            st.markdown(f"""
            <div class="success-card">
                <h3>💰 Custo Total de Aquisição</h3>
                <h2>{formatar_valor(base_de_calculo)}</h2>
                <p>Este é o valor base para o custo do seu produto</p>
            </div>
            """, unsafe_allow_html=True)
            
    # Seção 2: Cálculo de Desconto por Peça
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎯 Desconto por Peça</div>', unsafe_allow_html=True)
    
    with st.form("calculo_desconto_peca_form"):
        st.markdown("📦 Preencha os valores para descobrir o desconto rateado por item.")
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            qtd_peca_str = st.text_input("📦 Quantidade", "1")
        with col2:
            valor_unit_str = st.text_input("💰 Valor Unitário (sem desc.)", "0,00")
        with col3:
            valor_total_desc_str = st.text_input("💸 Valor Total do Desconto", "0,00")

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submitted_peca = st.form_submit_button("🎯 Calcular Desconto", use_container_width=True)

        if submitted_peca:
            valor_unit = converter_para_float(valor_unit_str)
            valor_total_desc = converter_para_float(valor_total_desc_str)
            
            try:
                qtd_peca = int(qtd_peca_str)
                if qtd_peca <= 0:
                    st.error("⚠️ A quantidade de peças deve ser maior que zero.")
                    st.session_state.calculo_peca_feito = False
                    return
            except (ValueError, TypeError):
                st.error("⚠️ A quantidade deve ser um número inteiro válido.")
                st.session_state.calculo_peca_feito = False
                return

            if valor_unit is not None and valor_total_desc is not None:
                valor_total_sem_desc = qtd_peca * valor_unit
                if valor_total_sem_desc <= 0:
                    st.warning("⚠️ O Valor Total (sem desconto) deve ser maior que zero.")
                    st.session_state.calculo_peca_feito = False
                    return

                desconto_total = valor_total_sem_desc - valor_total_desc
                if desconto_total < 0:
                    st.warning("⚠️ O valor com desconto é maior que o valor original. O desconto será zero.")
                    desconto_total = 0

                desconto_por_peca = desconto_total / qtd_peca if qtd_peca > 0 else 0
                percentual_desconto = (desconto_total / valor_total_sem_desc) * 100 if valor_total_sem_desc > 0 else 0
                valor_unitario_com_desconto = valor_total_desc / qtd_peca if qtd_peca > 0 else 0

                st.session_state.calculo_peca_feito = True
                st.session_state.desconto_unitario_peca = desconto_por_peca
                st.session_state.valor_unitario_final_peca = valor_unitario_com_desconto

                # Exibição dos resultados em formato de cards
                col1, col2 = st.columns(2, gap="medium")
                
                with col1:
                    st.metric(
                        label="💰 Valor Total (sem desconto)", 
                        value=formatar_valor(valor_total_sem_desc),
                        help="Valor total antes da aplicação do desconto"
                    )
                    st.metric(
                        label="🎯 Desconto Unitário", 
                        value=formatar_valor(desconto_por_peca, casas_decimais=4),
                        help="Valor do desconto por unidade"
                    )
                
                with col2:
                    st.metric(
                        label="📈 Desconto Aplicado (%)", 
                        value=f"{percentual_desconto:.2f}%".replace(".", ","),
                        help="Percentual de desconto aplicado"
                    )
                    st.metric(
                        label="💵 Valor Unit. (c/ desconto)", 
                        value=formatar_valor(valor_unitario_com_desconto, casas_decimais=4),
                        help="Valor unitário após aplicação do desconto"
                    )

    # Seção de devolução
    if st.session_state.calculo_peca_feito:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">🔄 Valor para Devolução</div>', unsafe_allow_html=True)
        
        col_dev1, col_dev2 = st.columns([1, 2])
        
        with col_dev1:
            qtd_devolucao_peca = st.number_input(
                "📦 Quantidade para devolução:", 
                min_value=0, 
                step=1, 
                key="qtd_devolucao_fornecedor",
                help="Quantidade de peças a serem devolvidas"
            )
        
        with col_dev2:
            if qtd_devolucao_peca > 0:
                valor_total_devolucao = qtd_devolucao_peca * st.session_state.valor_unitario_final_peca
                
                st.markdown(f"""
                <div class="success-card">
                    <h3>💰 Valor Total para Devolução</h3>
                    <h2>{formatar_valor(valor_total_devolucao)}</h2>
                    <p>Para {qtd_devolucao_peca} peças</p>
                </div>
                """, unsafe_allow_html=True)


# --- SIDEBAR E NAVEGAÇÃO ---
def configurar_sidebar():
    """Configura a sidebar com navegação e informações."""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2 style="color: #2c3e50; margin-bottom: 0.5rem;">💰 FinanceCalc Pro</h2>
        <p style="color: #7f8c8d; font-size: 0.9rem;">Calculadoras Financeiras Avançadas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Imagem com melhor tratamento de erro
    try:
        st.sidebar.image(
            "https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=400&auto=format&fit=crop", 
            use_container_width=True,
            caption="Gestão Financeira Inteligente"
        )
    except:
        st.sidebar.markdown("📊 **Dashboard Financeiro**")
    
    st.sidebar.markdown("---")
    
    # Menu de navegação estilizado
    st.sidebar.markdown("### 🧭 Navegação")
    
    return st.sidebar.radio(
        "Escolha a calculadora:",
        ["🧮 Calculadora de Descontos", "🏭 Cálculo Fornecedor SB"],
        key="navegacao_principal"
    )


# --- MENU PRINCIPAL E ROTEAMENTO ---
def main():
    """Função principal da aplicação."""
    
    # Configuração da sidebar
    selecao = configurar_sidebar()
    
    # Roteamento de páginas
    if selecao == "🧮 Calculadora de Descontos":
        pagina_calculadora_descontos()
    elif selecao == "🏭 Cálculo Fornecedor SB":
        pagina_calculo_fornecedor()
    
    # Footer da sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.8rem; padding: 1rem;">
        <p>🚀 <strong>FinanceCalc Pro</strong></p>
        <p>Desenvolvido para otimizar<br>seus cálculos financeiros</p>
        <p>📊 Versão 2.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
