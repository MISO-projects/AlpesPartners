FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

RUN chmod -R 755 /app

EXPOSE 8002

ENV HOST=0.0.0.0
ENV PORT=8002
ENV DATABASE_URL=sqlite:///./data/comisiones.db
ENV PULSAR_URL=pulsar://pulsar:6650
ENV LOG_LEVEL=INFO

CMD ["python", "main.py"]
