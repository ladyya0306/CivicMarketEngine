# CivicMarketEngine Development Container

This folder contains an optional local development container for the public
noncommercial demo package. It is intended for repeatable local checks and
does not include private credentials, private prompt material, or generated
run results.

## Prerequisites

- Docker: https://docs.docker.com/engine/install/
- Docker Compose: https://docs.docker.com/compose/install/

## Configure Environment

Create a local `.env` file from the public template only when needed. Do not
commit `.env`.

```bash
cd .container
cp .env.example .env
```

The offline public smoke test does not require external service credentials.

## Start Container

```bash
docker compose up -d
```

## Enter the Container

```bash
docker compose exec atlas-market-engine bash
```

Typical public checks:

```bash
python scripts/check_public_snapshot.py .
python scripts/public_smoke_test.py --rounds 1 --seed 42
python -m pytest tests/test_public_package.py -q
```

## Stop and Remove

```bash
docker compose down
```

## Public Package Boundary

The container setup is a development aid only. Public snapshots must still
exclude local `.env` files, result folders, logs, databases, spreadsheets,
caches, and any private research workspace material.
