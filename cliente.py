import requests

def calcular_gpt(valor_total_produto, valor_total_nota, quantidade, valor_unitario):
    url = "http://127.0.0.1:8000/calcular"
    payload = {
        "valor_total_produto": valor_total_produto,
        "valor_total_nota": valor_total_nota,
        "quantidade": quantidade,
        "valor_unitario": valor_unitario
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"erro": f"Erro do servidor: {response.text}"}
    except Exception as e:
        return {"erro": f"Erro ao conectar com o servidor: {str(e)}"}

# Testar a função
if __name__ == "__main__":
    resultado = calcular_gpt(1000.0, 900.0, 10, 100.0)
    print("Resultado do cálculo:")
    print(resultado)
