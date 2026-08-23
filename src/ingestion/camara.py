import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/raio_x_db")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json"
}

def buscar_deputados():
    """Busca os deputados em exercício na legislatura atual."""

    url = f"{BASE_URL}/deputados"

    params = {
        "ordem": "ASC",
        "ordenarPor": "nome"
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return pd.DataFrame(
        response.json().get("dados", [])
    )
def buscar_despesas_ceap(df_deputados):
    """Baixa a CEAP 2026 e relaciona despesas aos deputados."""

    ano = 2026
    url = f"http://www.camara.leg.br/cotas/Ano-{ano}.csv.zip"

    print(f"--- Baixando CEAP {ano} ---")
    print(f"URL: {url}")

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=120
        )

        response.raise_for_status()

        print(
            f"✅ Arquivo ZIP baixado: "
            f"{len(response.content):,} bytes"
        )

        from io import BytesIO
        from zipfile import ZipFile
        import unicodedata
        import re

        with ZipFile(BytesIO(response.content)) as zip_file:

            arquivos = zip_file.namelist()

            print(
                f"📦 Arquivos dentro do ZIP: {arquivos}"
            )

            arquivo_csv = next(
                (
                    nome
                    for nome in arquivos
                    if nome.lower().endswith(".csv")
                ),
                None
            )

            if not arquivo_csv:
                raise Exception(
                    "Nenhum CSV encontrado dentro do ZIP."
                )

            print(f"📄 Lendo: {arquivo_csv}")

            with zip_file.open(arquivo_csv) as arquivo:

                df_ceap = pd.read_csv(
                    arquivo,
                    sep=";",
                    encoding="utf-8",
                    low_memory=False
                )

        print(
            f"✅ Registros CEAP encontrados: "
            f"{len(df_ceap):,}"
        )

        print(
            f"📋 Colunas encontradas: "
            f"{list(df_ceap.columns)}"
        )

        # ---------------------------------------------------------
        # Normalização dos nomes
        # ---------------------------------------------------------

        def normalizar_nome(nome):

            if pd.isna(nome):
                return ""

            nome = str(nome).upper().strip()

            nome = unicodedata.normalize(
                "NFKD",
                nome
            )

            nome = "".join(
                c for c in nome
                if not unicodedata.combining(c)
            )

            nome = re.sub(
                r"[^A-Z0-9 ]",
                " ",
                nome
            )

            nome = re.sub(
                r"\s+",
                " ",
                nome
            ).strip()

            return nome

        # ---------------------------------------------------------
        # Criar chave nome + UF
        # ---------------------------------------------------------

        df_deputados["nome_chave"] = (
            df_deputados["nome"]
            .apply(normalizar_nome)
        )

        df_deputados["uf_chave"] = (
            df_deputados["siglaUf"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df_ceap["nome_chave"] = (
            df_ceap["txNomeParlamentar"]
            .apply(normalizar_nome)
        )

        df_ceap["uf_chave"] = (
            df_ceap["sgUF"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        # ---------------------------------------------------------
        # Cruzamento
        # ---------------------------------------------------------

        mapa_deputados = (
            df_deputados[
                [
                    "id",
                    "nome",
                    "siglaUf",
                    "nome_chave",
                    "uf_chave"
                ]
            ]
            .drop_duplicates(
                subset=["nome_chave", "uf_chave"]
            )
        )

        df_filtrado = df_ceap.merge(
            mapa_deputados[
                [
                    "id",
                    "nome_chave",
                    "uf_chave"
                ]
            ],
            on=[
                "nome_chave",
                "uf_chave"
            ],
            how="inner"
        )

        # O ID da API passa a ser nosso id_camara
        df_filtrado = df_filtrado.rename(
            columns={
                "id": "id_camara"
            }
        )

        # ---------------------------------------------------------
        # Resultado
        # ---------------------------------------------------------

        deputados_encontrados = (
            df_filtrado["id_camara"]
            .nunique()
            if not df_filtrado.empty
            else 0
        )

        print(
            f"🎯 Despesas relacionadas: "
            f"{len(df_filtrado):,}"
        )

        print(
            f"👥 Deputados relacionados: "
            f"{deputados_encontrados}"
        )

        if not df_filtrado.empty:

            print(
                "🔎 Exemplo de relacionamento:"
            )

            print(
                df_filtrado[
                    [
                        "id_camara",
                        "txNomeParlamentar",
                        "sgUF",
                        "vlrLiquido"
                    ]
                ]
                .head(5)
                .to_string(index=False)
            )

        return df_filtrado

    except Exception as e:

        print(
            f"❌ Erro ao baixar/processar CEAP: {e}"
        )

        return pd.DataFrame()
def salvar_deputados(df, engine):
    """Salva os deputados no PostgreSQL."""
    if df.empty:
        return
    colunas = {
        "id": "id_camara",
        "nome": "nome",
        "siglaPartido": "partido",
        "siglaUf": "uf",
        "idLegislatura": "id_legislatura",
        "email": "email",
        "urlFoto": "url_foto"
    }
    df_filtrado = df[list(colunas.keys())].rename(columns=colunas)
    df_filtrado.to_sql("deputados", engine, if_exists="replace", index=False)
    print(f"✅ {len(df_filtrado)} deputados salvos no banco de dados.")

def salvar_despesas(df_deputados, engine):
    """Salva as despesas CEAP no PostgreSQL."""

    print("--- Coletando despesas (CEAP)... ---")

    df_ceap = buscar_despesas_ceap(
        df_deputados
    )

    if df_ceap.empty:
        print("⚠️ Nenhuma despesa encontrada.")
        return

    colunas_map = {
        "id_camara": "id_camara",
        "txtDescricao": "tipo_despesa",
        "txtFornecedor": "fornecedor",
        "txtCNPJCPF": "cnpj_cpf_fornecedor",
        "vlrLiquido": "valor",
        "datEmissao": "data"
    }

    colunas_presentes = [
        c
        for c in colunas_map
        if c in df_ceap.columns
    ]

    df_despesas = (
    df_ceap[
        colunas_presentes
    ]
    .rename(
        columns=colunas_map
    )
    )

    df_despesas["valor"] = pd.to_numeric(
        df_despesas["valor"],
        errors="coerce"
    )

    df_despesas["data"] = pd.to_datetime(
        df_despesas["data"],
        errors="coerce"
    ).dt.date

    # Limpa os dados antigos sem destruir a estrutura da tabela
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE despesas"))

    # Insere os novos dados
    df_despesas.to_sql(
        "despesas",
        engine,
        if_exists="append",
        index=False
    )

    print(
        f"✅ {len(df_despesas):,} registros de despesas "
        f"salvos no PostgreSQL!"
    )
if __name__ == "__main__":
    print("--- Iniciando Pipeline de Ingestão Completa ---")

    engine = create_engine(DATABASE_URL)

    df_deputados = buscar_deputados()

    salvar_deputados(
        df_deputados,
        engine
    )

    salvar_despesas(
        df_deputados,
        engine
    )

