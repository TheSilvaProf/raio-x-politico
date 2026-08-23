# 🔎 Raio-X Político

Portal para consulta e análise de dados públicos da Câmara dos Deputados.

O projeto coleta dados oficiais da Câmara, armazena e organiza as informações
e disponibiliza uma API para consulta dos deputados e análise de suas despesas
parlamentares.

## 🏗️ Arquitetura

```text
Câmara dos Deputados
        │
        ▼
   ETL em Python
        │
        ▼
     Supabase
   PostgreSQL
        │
        ▼
      FastAPI
        │
        ▼
      Portal
````

## 📊 Dados atuais

* 513 deputados
* 92.986 registros de despesas
* Dados da CEAP 2026
* Fonte: dados públicos da Câmara dos Deputados

## 🔎 Funcionalidades

### Consulta de deputados

```text
GET /api/deputados
```

Lista os deputados disponíveis.

### Perfil do deputado

```text
GET /api/deputados/{id_camara}
```

Retorna informações básicas do parlamentar.

### Raio-X financeiro

```text
GET /api/deputados/{id_camara}/raio-x
```

Apresenta:

* quantidade de despesas;
* total gasto;
* gasto médio;
* categorias de despesas;
* principais fornecedores;
* evolução mensal;
* maiores despesas.

## 🛠️ Stack

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL
* Supabase
* Pandas
* Requests
* Docker

## 🚀 Ambiente

O desenvolvimento local utiliza Docker Compose.

Em produção, a API será executada no Render e utilizará o PostgreSQL
hospedado no Supabase.

A conexão com o banco é configurada através da variável de ambiente:

```text
DATABASE_URL
```

Nenhuma credencial de banco deve ser armazenada no código ou no Git.

## 📁 Estrutura

```text
raio-x-politico/
├── src/
│   ├── api/
│   │   └── main.py
│   ├── database/
│   │   └── models.py
│   ├── ingestion/
│   │   └── camara.py
│   ├── web/
│   │   └── index.html
│   └── config.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🎯 Objetivo

Construir uma ferramenta simples e transparente para que qualquer pessoa
possa consultar dados públicos de parlamentares e compreender como os
recursos da atividade parlamentar são utilizados.

````

### Por que eu prefiro isso?

Porque o README atual contém números e análises que podem ficar rapidamente desatualizados, além de dizer:

> `Banco de Dados: PostgreSQL 15 (Dockerizada)`

Isso **já não representa nossa arquitetura de produção**.

E também temos esta afirmação:

> `Cobertura Parlamentar: 509 dos 513 deputados analisados.`

Mas acabamos de confirmar que a tabela `deputados` tem **513 registros**. Então não quero deixar uma informação potencialmente conflitante no README.

---

### Mas não vamos editar ainda

Temos uma decisão importante aqui.

**Eu sugiro que você substitua o README inteiro pelo modelo acima**, mas antes quero que façamos isso conscientemente, porque estamos entrando na fase de publicação.

Se você topar, o próximo comando é simplesmente:

```bash
nano README.md
````

e substituímos o conteúdo.

Depois:

```bash
git diff
```

E **antes de commitarmos**, eu reviso o diff com você.

Isso mantém nosso processo no estilo que você gosta: **uma mudança por vez, testada antes da próxima.**

