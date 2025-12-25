# Slim Python image pro menší velikost
FROM python:3.11-slim

# Nastavení pracovního adresáře
WORKDIR /app

# Instalace systémových závislostí (např. pro psycopg2 binary)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopírování requirements.txt
COPY requirements.txt .

# Instalace Python závislostí
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování zdrojového kódu
COPY . .

# Expose port (uvicorn běží na 8000)
EXPOSE 8000

# Spuštění aplikace
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
