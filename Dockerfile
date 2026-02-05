FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir dbt-duckdb==1.7.2

COPY . /app

CMD ["dbt", "build", "--profiles-dir", "profiles"]
