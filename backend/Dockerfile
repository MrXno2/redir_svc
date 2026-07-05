# сборка multi stage
# ===== СТАДИЯ СБОРКИ =====
FROM python:3.12-slim AS builder
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir poetry==2.4.1
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# ===== ФИНАЛЬНЫЙ ОБРАЗ =====
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*
# Копируем только установленные пакеты из builder (без poetry!)
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src ./src
EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]