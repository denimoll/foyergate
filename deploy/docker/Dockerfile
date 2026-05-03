# syntax=docker/dockerfile:1.7
#
# FoyerGate — service image
#
# Multi-stage:
#   1. builder — install dependencies into an isolated venv via uv
#   2. runtime — copy the venv into a slim base, drop privileges, run
#
# Build:
#   docker build -f deploy/docker/Dockerfile -t foyergate:dev .
# Run:
#   docker run --rm -p 9876:9876 --env-file .env foyergate:dev

# ── Stage 1: builder ───────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

# Pin uv from its own image to avoid bootstrapping it via pip.
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /build

# Install dependencies first (layer cached when only source changes).
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv && \
    uv sync --frozen --no-dev --no-install-project || \
    uv sync --no-dev --no-install-project

# Now copy the source and install the project itself.
COPY README.md ./
COPY src/ ./src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-editable

# ── Stage 2: runtime ──────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS runtime

ARG APP_UID=10001
ARG APP_GID=10001

RUN groupadd --system --gid ${APP_GID} foyergate && \
    useradd  --system --uid ${APP_UID} --gid ${APP_GID} \
             --home /app --shell /usr/sbin/nologin foyergate && \
    mkdir -p /app && chown foyergate:foyergate /app

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    FOYERGATE_API_HOST=0.0.0.0 \
    FOYERGATE_API_PORT=9876

# Copy the prepared virtualenv from the builder.
COPY --from=builder --chown=root:root /opt/venv /opt/venv

WORKDIR /app
USER foyergate:foyergate

EXPOSE 9876

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; \
sys.exit(0 if urllib.request.urlopen('http://localhost:9876/healthz', timeout=3).status==200 else 1)"

# Default command: API server. Override with `worker` once the worker
# entrypoint is in place.
CMD ["foyergate"]
