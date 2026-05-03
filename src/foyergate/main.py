"""Application entry point.

Exposes:

* ``app`` — the ASGI application, used by uvicorn / gunicorn.
* ``cli()`` — a thin command-line wrapper, registered as the ``foyergate``
  console script in ``pyproject.toml``.
"""

from __future__ import annotations

import sys

import uvicorn
from fastapi import FastAPI

from foyergate import __version__
from foyergate.api.health import router as health_router
from foyergate.config import get_settings


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="FoyerGate",
        description=(
            "An OSS supply chain gateway. "
            "Vet open-source packages before they enter your local repository."
        ),
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Routers
    app.include_router(health_router, tags=["health"])

    # Tag the running environment in OpenAPI for visibility
    app.openapi_tags = [
        {"name": "health", "description": "Liveness and readiness probes."},
    ]
    app.state.settings = settings

    return app


# Module-level app instance for uvicorn: `uvicorn foyergate.main:app`
app = create_app()


def cli() -> None:
    """Entry point for the ``foyergate`` console script.

    Currently launches the API server. Subcommands (worker, scheduler, migrate)
    will be added as separate ``foyergate-<name>`` scripts or as click commands.
    """
    settings = get_settings()
    uvicorn.run(
        "foyergate.main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
        reload=settings.env == "development",
    )


if __name__ == "__main__":
    cli()
    sys.exit(0)
