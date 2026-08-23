import requests

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

def buscar_deputados():
    """Busca a lista de deputados em exercício na Câmara."""
    url = f"{BASE_URL}/deputados"
    params = {
        "ordem": "ASC",
        "ordenarPor": "nome"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        dados = response.json()
        return dados.get("dados", [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com a API da Câmara: {e}")
        return []

if __name__ == "__main__":
    print("--- Buscando dados da API da Câmara dos Deputados... ---")
    deputados = buscar_deputados()
    
    print(f"Total de deputados encontrados nesta página: {len(deputados)}")
    
    if deputados:
        primeiro = deputados[0]
        print(f"\nPrimeiro deputado da lista:")
        print(f"Nome: {primeiro['nome']}")
        print(f"Partido/UF: {primeiro['siglaPartido']}-{primeiro['siglaUf']}")
        print(f"E-mail: {primeiro['email']}")
