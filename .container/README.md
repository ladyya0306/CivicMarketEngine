# Atlas Market Engine Development Container

This folder contains an optional local development container for Atlas Market
Engine. It is intended for repeatable local testing and does not include any
private credentials or generated run results.

## Prerequisites

- Docker: https://docs.docker.com/engine/install/
- Docker Compose: https://docs.docker.com/compose/install/

## Configure Environment

Create a local `.env` file from the template. Do not commit `.env`.

```bash
cd .container
cp .env.example .env
```

Edit `.env` and replace the placeholder values with your own keys only when
you need live LLM or external API calls. For offline smoke tests, prefer mock
mode.

## Start Container

```bash
docker compose up -d
```

This builds the local image and starts the `atlas-market-engine-dev`
container with the repository mounted at `/workspace/atlas-market-engine`.

## Enter the Container

```bash
docker compose exec atlas-market-engine bash
```

Typical checks:

```bash
python -m compileall agent_behavior.py database.py simulation_runner.py real_estate_demo_v2_1.py
python -m pytest
```

## Stop and Remove

```bash
docker compose down
```

## Public Package Boundary

The container setup is a development aid only. Public or registration
snapshots must still exclude local `.env` files, `results/`, `output/`,
`logs/`, database files, caches, and other generated artifacts.
