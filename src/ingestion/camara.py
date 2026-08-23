import os
import requests
import pandas as pd
from sqlalchemy import create_engine

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/raio_x_db")

def buscar_deputados():
    """Busca os deputados na API e retorna como DataFrame do Pandas."""
    url = f"{BASE_URL}/deputados"
    params = {"ordem": "ASC", "ordenarPor": "nome"}
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    dados = response.json().get("dados", [])
    
    return pd.DataFrame(dados)

def salvar_no_banco(df):
    """Salva o DataFrame no banco de dados PostgreSQL."""
    if df.empty:
        print("Nenhum dado para salvar.")
        return

    # Conecta no Postgres via SQLAlchemy
    engine = create_engine(DATABASE_URL)
    
    # Seleciona e renomeia apenas as colunas úteis
    colunas_uteis = {
        "id": "id_camara",
        "nome": "nome",
        "siglaPartido": "partido",
        "siglaUf": "uf",
        "idLegislatura": "id_legislatura",
        "email": "email",
        "urlFoto": "url_foto"
    }
    
    df_filtrado = df[list(colunas_uteis.keys())].rename(columns=colunas_uteis)
    
    # Insere no banco (substitui a tabela 'deputados' se já existir)
    df_filtrado.to_sql("deputados", engine, if_exists="replace", index=False)
    print(f"Sucesso! {len(df_filtrado)} deputados salvos no banco PostgreSQL.")

if __name__ == "__main__":
    print("--- Iniciando Pipeline de Ingestão ---")
    df_deputados = buscar_deputados()
    salvar_no_banco(df_deputados)
