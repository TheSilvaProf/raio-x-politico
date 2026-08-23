from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/raio_x_db"
)

engine = create_engine(DATABASE_URL)

app = FastAPI(
    title="Raio-X Político",
    description="API para consulta de dados públicos de políticos",
    version="0.1.0"
)
app.mount(
    "/web",
    StaticFiles(directory="src/web", html=True),
    name="web"
)
WEB_DIR = "src/web"

@app.get("/", include_in_schema=False)
def pagina_inicial():
    return FileResponse(
        os.path.join(WEB_DIR, "index.html")
    )

app.mount(
    "/web",
    StaticFiles(directory=WEB_DIR),
    name="web"
)
@app.get("/api/deputados")
def listar_deputados():
    query = text("""
        SELECT
            id_camara,
            nome,
            partido,
            uf
        FROM deputados
        ORDER BY nome
    """)

    with engine.connect() as conn:
        resultado = conn.execute(query)

        deputados = [
            dict(row._mapping)
            for row in resultado
        ]

    return {
        "total": len(deputados),
        "deputados": deputados
    }


@app.get("/api/deputados/{id_camara}")
def buscar_deputado(id_camara: int):
    query = text("""
        SELECT
            id_camara,
            nome,
            partido,
            uf
        FROM deputados
        WHERE id_camara = :id_camara
    """)

    with engine.connect() as conn:
        resultado = conn.execute(
            query,
            {"id_camara": id_camara}
        ).fetchone()

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Deputado não encontrado"
        )

    return dict(resultado._mapping)
@app.get("/api/deputados/{id_camara}/raio-x")
def raio_x_deputado(id_camara: int):

    query_deputado = text("""
        SELECT
            id_camara,
            nome,
            partido,
            uf,
            url_foto
        FROM deputados
        WHERE id_camara = :id_camara
    """)

    query_gastos = text("""
        SELECT
            COUNT(*) AS quantidade_despesas,
            COALESCE(SUM(valor), 0)::NUMERIC(14,2) AS total_gasto,
            COALESCE(AVG(valor), 0)::NUMERIC(14,2) AS gasto_medio
        FROM despesas
        WHERE id_camara = :id_camara
    """)
    query_categorias = text("""
        SELECT
            tipo_despesa,
            COUNT(*) AS quantidade,
            SUM(valor)::NUMERIC(14,2) AS total_gasto
        FROM despesas
        WHERE id_camara = :id_camara
        GROUP BY tipo_despesa
        ORDER BY total_gasto DESC
    """)
    query_fornecedores = text("""
        SELECT
            fornecedor,
            cnpj_cpf_fornecedor,
            COUNT(*) AS quantidade_despesas,
            SUM(valor)::NUMERIC(14,2) AS total_recebido
        FROM despesas
        WHERE id_camara = :id_camara
        GROUP BY fornecedor, cnpj_cpf_fornecedor
        ORDER BY total_recebido DESC
        LIMIT 10
    """)
    query_evolucao = text("""
        SELECT
            DATE_TRUNC('month', data)::DATE AS mes,
            COUNT(*) AS quantidade_despesas,
            SUM(valor)::NUMERIC(14,2) AS total_gasto
        FROM despesas
        WHERE id_camara = :id_camara
          AND data IS NOT NULL
        GROUP BY DATE_TRUNC('month', data)
        ORDER BY mes
    """)
    query_maiores_despesas = text("""
        SELECT
            data,
            tipo_despesa,
            fornecedor,
            cnpj_cpf_fornecedor,
            valor
        FROM despesas
        WHERE id_camara = :id_camara
          AND valor IS NOT NULL
        ORDER BY valor DESC
        LIMIT 10
    """)

    with engine.connect() as conn:

        deputado = conn.execute(
            query_deputado,
            {"id_camara": id_camara}
        ).fetchone()

        if deputado is None:
            raise HTTPException(
                status_code=404,
                detail="Deputado não encontrado"
            )

        gastos = conn.execute(
            query_gastos,
            {"id_camara": id_camara}
        ).fetchone()
        categorias = conn.execute(
            query_categorias,
            {"id_camara": id_camara}
        ).fetchall()
        fornecedores = conn.execute(
            query_fornecedores,
            {"id_camara": id_camara}
        ).fetchall()
        evolucao = conn.execute(
            query_evolucao,
            {"id_camara": id_camara}
        ).fetchall()
        maiores_despesas = conn.execute(
            query_maiores_despesas,
            {"id_camara": id_camara}
        ).fetchall()

    return {
        "deputado": dict(deputado._mapping),
        "gastos": dict(gastos._mapping),
        "categorias": [
            dict(row._mapping)
            for row in categorias
        ],
        "fornecedores": [
            dict(row._mapping)
            for row in fornecedores
        ],
        "evolucao_mensal": [
            dict(row._mapping)
            for row in evolucao
        ],
        "maiores_despesas": [
            dict(row._mapping)
            for row in maiores_despesas
        ]

    }
