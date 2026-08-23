# Usa uma imagem oficial e leve do Python (já pré-compilada)
FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e força o output no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala ferramentas básicas de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte para dentro do container
COPY . .

# Comando padrão ao rodar o container
CMD ["python", "-m", "src.ingestion.camara"]
