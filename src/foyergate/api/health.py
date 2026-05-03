"""Health and readiness probes.

These endpoints are intentionally simple and dependency-free so that
load balancers, Kubernetes probes, and ``docker compose`` healthchecks
can rely on them without authentication.

* ``GET /healthz`` — liveness: the process is up.
* ``GET /readyz`` — readiness: the service can accept traffic
  (checks downstream dependencies in future iterations).
"""

from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel

from foyergate import __version__

router = APIRouter()


class HealthResponse(BaseModel):
    """Minimal payload returned by health probes."""

    status: str
    version: str


@router.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
)
async def healthz() -> HealthResponse:
    """Return ``ok`` if the process is alive."""
    return HealthResponse(status="ok", version=__version__)


@router.get(
    "/readyz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
)
async def readyz() -> HealthResponse:
    """Return ``ok`` if the service is ready to handle requests.

    Future iterations will check downstream dependencies (Postgres,
    Redis, OPA, object storage) and degrade this probe accordingly.
    """
    return HealthResponse(status="ok", version=__version__)
