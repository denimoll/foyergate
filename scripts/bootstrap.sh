#!/usr/bin/env bash
#
# scripts/bootstrap.sh — first-time setup helper.
#
# What it does:
#   1. Verifies Docker and uv are present.
#   2. Copies .env.example to .env if you don't have one yet.
#   3. Installs Python dependencies into a uv-managed venv.
#   4. Brings up the local stack with docker compose.
#
# Usage:
#   ./scripts/bootstrap.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

color() { printf '\033[%sm%s\033[0m' "$1" "$2"; }
info()  { echo "$(color '0;36' '==>') $*"; }
warn()  { echo "$(color '0;33' '!!') $*" >&2; }
fail()  { echo "$(color '0;31' 'xx') $*" >&2; exit 1; }

# ── 1. Prerequisites ───────────────────────────────────────────────
command -v docker >/dev/null 2>&1 || fail "docker is required (see https://docs.docker.com/get-docker/)"
docker compose version >/dev/null 2>&1 || fail "docker compose v2 is required"
command -v uv >/dev/null 2>&1 || {
    warn "uv not found — install from https://docs.astral.sh/uv/"
    fail "aborting"
}

# ── 2. .env ────────────────────────────────────────────────────────
if [[ ! -f .env ]]; then
    info "creating .env from .env.example"
    cp .env.example .env
else
    info ".env already exists — leaving it alone"
fi

# ── 3. Python deps ────────────────────────────────────────────────
info "installing Python dependencies with uv"
uv sync --all-extras

# ── 4. Local stack ────────────────────────────────────────────────
info "bringing up the docker compose stack"
docker compose -f deploy/docker/compose.yaml up -d

cat <<EOF

$(color '1;32' 'FoyerGate is up.')

  API docs:      http://localhost:9876/docs
  MinIO console: http://localhost:9001  (foyergate / changeme-in-production)
  OPA:           http://localhost:8181

To tail logs:    make logs
To shut down:    make down

EOF
