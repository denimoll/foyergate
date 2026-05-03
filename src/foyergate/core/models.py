"""Domain models for FoyerGate.

These models are the source of truth for the public API contract. They are
intentionally small for the in-memory milestone; SQLAlchemy mappings will
mirror them once the persistence layer lands, and ``Finding`` /
``ComponentRef`` will follow when checkers are implemented.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID, uuid4

from packageurl import PackageURL
from pydantic import BaseModel, ConfigDict, Field

# MVP scope per docs/architecture.md is npm-only. Adding "pypi", "maven", …
# here is the entry point for new ecosystem adapters.
Ecosystem = Literal["npm"]


class RequestState(StrEnum):
    """Lifecycle of a ``ScanRequest`` (see docs/concepts.md)."""

    RECEIVED = "RECEIVED"
    FETCHING = "FETCHING"
    ANALYZING = "ANALYZING"
    DECIDING = "DECIDING"
    PROMOTING = "PROMOTING"
    DONE = "DONE"
    BLOCKED = "BLOCKED"
    QUARANTINED = "QUARANTINED"
    FAILED = "FAILED"


class Verdict(StrEnum):
    """Final decision attached to a request."""

    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    QUARANTINED = "QUARANTINED"
    PENDING = "PENDING"
    ERROR = "ERROR"


class ScanRequestCreate(BaseModel):
    """Payload accepted by ``POST /v1/requests``."""

    model_config = ConfigDict(extra="forbid")

    ecosystem: Ecosystem
    name: str = Field(min_length=1, max_length=214)
    version: str = Field(min_length=1, max_length=64)
    requested_by: str = Field(min_length=1, max_length=256)


class ScanRequest(BaseModel):
    """A submitted vetting request and its current status."""

    id: UUID
    ecosystem: Ecosystem
    name: str
    version: str
    purl: str
    requested_by: str
    state: RequestState
    verdict: Verdict
    created_at: datetime
    updated_at: datetime

    @classmethod
    def new(cls, payload: ScanRequestCreate) -> ScanRequest:
        """Build a fresh ``RECEIVED`` / ``PENDING`` request from input."""
        now = datetime.now(UTC)
        purl = PackageURL(
            type=payload.ecosystem,
            name=payload.name,
            version=payload.version,
        ).to_string()
        return cls(
            id=uuid4(),
            ecosystem=payload.ecosystem,
            name=payload.name,
            version=payload.version,
            purl=purl,
            requested_by=payload.requested_by,
            state=RequestState.RECEIVED,
            verdict=Verdict.PENDING,
            created_at=now,
            updated_at=now,
        )
