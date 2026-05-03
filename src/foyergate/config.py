"""Application configuration.

All settings are read from environment variables with the ``FOYERGATE_`` prefix.
See ``.env.example`` for the full list of supported variables.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "staging", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
    """Service configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="FOYERGATE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────────
    env: Environment = "development"
    log_level: LogLevel = "INFO"
    api_host: str = "0.0.0.0"  # noqa: S104 — binding to 0.0.0.0 is intentional inside containers
    api_port: int = 9876

    # ── Database ───────────────────────────────────────────────────
    db_dsn: str = "postgresql+asyncpg://foyergate:foyergate@localhost:5432/foyergate"

    # ── Cache & queue ──────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── Object storage ─────────────────────────────────────────────
    s3_endpoint: str = "http://localhost:9000"
    s3_region: str = "us-east-1"
    s3_access_key: str = "foyergate"
    s3_secret_key: str = Field(default="changeme-in-production", repr=False)
    s3_bucket_quarantine: str = "foyergate-quarantine"
    s3_bucket_reports: str = "foyergate-reports"

    # ── Policy engine ──────────────────────────────────────────────
    opa_url: str = "http://localhost:8181"
    opa_policy_package: str = "foyergate.default"

    # ── Internal artifact repository ───────────────────────────────
    nexus_url: str = "http://localhost:8081"
    nexus_username: str = "admin"
    nexus_password: str = Field(default="changeme-in-production", repr=False)
    nexus_npm_repository: str = "npm-internal"

    # ── Upstream registries ────────────────────────────────────────
    npm_registry_url: str = "https://registry.npmjs.org"

    # ── Verdict cache & rescan ─────────────────────────────────────
    verdict_ttl_seconds: int = 7 * 24 * 60 * 60  # 7 days
    rescan_cron: str = "0 3 * * *"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Cached so that environment variables are read once per process.
    """
    return Settings()
