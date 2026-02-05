# dbt-duckdb

Projeto dbt open source usando DuckDB como engine principal, pronto para execução local e em CI.

## Estrutura

```
.
├── Dockerfile
├── docker-compose.yml
├── dbt_project.yml
├── packages.yml
├── profiles/
│   └── profiles.yml
├── models/
│   ├── silver/
│   │   └── example_silver.sql
│   └── gold/
│       └── example_gold.sql
├── data/
│   └── raw.duckdb
├── README.md
└── .gitignore
```

## Pré-requisitos

- Docker (para execução containerizada)
- Python 3.11+ (para execução local)

## Execução com Docker

```bash
docker compose up --build
```

## Execução local

```bash
python -m venv .venv
source .venv/bin/activate
pip install dbt-duckdb==1.7.2

dbt build --profiles-dir profiles
```

## Como funciona

- **Silver**: camada de normalização com `example_silver.sql`.
- **Gold**: camada de consumo com agregações via `example_gold.sql`.

## CI

Em pipelines, execute:

```bash
dbt deps

dbt build --profiles-dir profiles
```
