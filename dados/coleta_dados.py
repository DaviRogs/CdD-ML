import requests
import time
import pandas as pd

# Lista para armazenar todas as despesas de todos os deputados
todas_despesas = []

# Requisição para obter a lista de deputados
response = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados", params={"itens": 1000})

if response.status_code == 200:
    deputados = response.json()["dados"] 

    for deputado in deputados:
        deputado_id = deputado["id"]
        nome = deputado["nome"]

        print(f"\n🔹 Buscando despesas do deputado: {nome} (ID: {deputado_id})")

        url_despesas = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado_id}/despesas"
        
        params_despesas = {
            "ano": 2022,
            "itens": 50,
            "pagina": 1
        }

        response_despesas = requests.get(url_despesas, params=params_despesas)

        if response_despesas.status_code == 200:
            despesas = response_despesas.json()["dados"]

            for despesa in despesas:
                tipo = despesa["tipoDespesa"]
                fornecedor = despesa["nomeFornecedor"]
                valor = despesa["valorDocumento"]
                data = despesa["dataDocumento"]
                numeroDoc = despesa["numDocumento"]

                todas_despesas.append({
                    "numeroDoc": numeroDoc,
                    "idDeputado": deputado_id,
                    "nomeDeputado": nome,
                    "tipo_despesa": tipo,
                    "fornecedor": fornecedor,
                    "valor": valor,
                    "data": data
                })

        else:
            print(f"⚠️ Erro ao buscar despesas de {nome} (ID: {deputado_id})")

        time.sleep(0.5)  # Respeitar a API

    # Cria o DataFrame com todas as despesas e exporta para CSV
    df = pd.DataFrame(todas_despesas)
    df.to_csv("despesas_deputados_2024.csv", index=False, encoding='utf-8-sig')
    print("\n✅ Arquivo 'despesas_deputados_2024.csv' gerado com sucesso!")

else:
    print(f"❌ Erro ao buscar deputados: {response.status_code}")