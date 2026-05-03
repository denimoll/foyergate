# Quickstart

This guide gets a local FoyerGate stack running on your laptop in about five minutes. It is intended for **evaluation and development**, not production.

## Prerequisites

* Docker Engine with the Compose v2 plugin (`docker compose ...`)
* `git`
* About 2 GB of free RAM and 5 GB of disk

For local Python work (running tests, hacking on the code) you also need:

* Python 3.12 or newer
* [`uv`](https://docs.astral.sh/uv/) — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Run with Docker Compose

```bash
git clone https://github.com/denimoll/foyergate.git
cd foyergate
cp .env.example .env
make up
```

The stack includes:

| Service   | Port       | Purpose                                |
| --------- | ---------- | -------------------------------------- |
| API       | 9876       | FastAPI HTTP API and Swagger UI        |
| Postgres  | 5432       | Persistent state                       |
| Redis     | 6379       | Cache and arq queue                    |
| MinIO     | 9000, 9001 | S3-compatible object storage           |
| OPA       | 8181       | Policy engine                          |

Once the containers report healthy, open:

* **API + Swagger UI:** <http://localhost:9876/docs>
* **MinIO console:** <http://localhost:9001>
* **OPA:** <http://localhost:8181>

To tail logs:

```bash
make logs
```

To shut everything down:

```bash
make down
```

## Run the API locally (without Docker for the app)

Useful for fast iteration with hot reload.

```bash
make install            # uv sync --all-extras
make up                 # start Postgres, Redis, MinIO, OPA in containers
uv run foyergate        # run the API on the host with reload
```

## Run the tests

```bash
make test
```

For a coverage report:

```bash
make test-cov
open htmlcov/index.html
```

## Next steps

* Read [Architecture](architecture.md) to understand the request lifecycle.
* Read [Concepts](concepts.md) for the vocabulary (verdict, finding, checker, policy).
* Read [Extending](extending.md) when you want to plug in a new checker or ecosystem.
