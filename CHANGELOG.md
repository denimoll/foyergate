# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project scaffolding: repository structure, license, configuration baseline.
- Documentation skeleton (quickstart, architecture, concepts, API reference, extending, operations).
- Docker Compose stack for local evaluation: API, worker, Postgres, Redis, MinIO, OPA.
- FastAPI application skeleton with `/healthz` and `/readyz` endpoints.

### Changed

- Dependency floors raised to the latest releases (fastapi 0.162, SQLAlchemy 2.1, pydantic 2.14, alembic 1.20, and others); no known vulnerabilities in the resolved set.
- Docker images moved from Debian bookworm to trixie (`python:3.12-slim-trixie`), `uv` 0.5 → 0.13.
- CI actions updated: `actions/checkout` v7, `astral-sh/setup-uv` v10, `actions/upload-artifact` v7.

[Unreleased]: https://github.com/denimoll/foyergate/commits/main
