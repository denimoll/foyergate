"""In-memory ``ScanRequest`` store.

Temporary stand-in for the persistence layer. Replaced by a SQLAlchemy-backed
repository (and arq-driven state transitions) once the DB milestone lands.
The interface is intentionally narrow so the swap is mechanical.
"""

from __future__ import annotations

import asyncio
from uuid import UUID

from foyergate.core.models import ScanRequest


class InMemoryRequestStore:
    """Process-local map of ``UUID → ScanRequest`` guarded by a lock."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._items: dict[UUID, ScanRequest] = {}

    async def add(self, request: ScanRequest) -> None:
        async with self._lock:
            self._items[request.id] = request

    async def get(self, request_id: UUID) -> ScanRequest | None:
        async with self._lock:
            return self._items.get(request_id)

    async def clear(self) -> None:
        async with self._lock:
            self._items.clear()


_store = InMemoryRequestStore()


def get_request_store() -> InMemoryRequestStore:
    """FastAPI dependency provider; tests can override this."""
    return _store
