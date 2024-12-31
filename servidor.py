from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import locale

# Configurar o locale para o formato brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale pt_BR.UTF-8 não suportado no sistema.")

app = FastAPI()

# Modelo de dados para entrada
class CalculadoraRequest(BaseModel):
    valor_total_produto: float
    valor_total_nota: float
    quantidade: int
    valor_unitario: float

# Função para realizar os cálculos
def realizar_calculos(dados: CalculadoraRequest):
    try:
        desconto_em_porcentagem = 1 - (dados.valor_total_nota / dados.valor_total_produto)
        valor_unitario_com_desconto = -(dados.valor_unitario * (desconto_em_porcentagem - 1))
        valor_total_sem_desconto = dados.quantidade * dados.valor_unitario
        valor_total_com_desconto = dados.quantidade * valor_unitario_com_desconto
        usar_no_desconto = valor_total_sem_desconto - valor_total_com_desconto

        return {
            "desconto_em_porcentagem": round(desconto_em_porcentagem * 100, 2),
            "valor_unitario_com_desconto": locale.currency(valor_unitario_com_desconto, grouping=True),
            "usar_no_desconto": locale.currency(usar_no_desconto, grouping=True),
            "valor_total_com_desconto": locale.currency(valor_total_com_desconto, grouping=True),
            "valor_total_sem_desconto": locale.currency(valor_total_sem_desconto, grouping=True),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Rota principal
@app.post("/calcular")
async def calcular(request: CalculadoraRequest):
    resultado = realizar_calculos(request)
    return resultado
