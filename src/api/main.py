from fastapi import FastAPI, HTTPException
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


@app.get("/")
def raiz():
    return {
        "nome": "Raio-X Político",
        "status": "online",
        "versao": "0.1.0"
    }


@app.get("/deputados")
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


@app.get("/deputados/{id_camara}")
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
