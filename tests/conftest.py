"""Shared pytest fixtures."""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from foyergate.core.store import get_request_store
from foyergate.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """An httpx AsyncClient bound to the FastAPI app, no network needed."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def _isolate_request_store() -> AsyncIterator[None]:
    """Reset the in-memory store between tests so they cannot leak state."""
    await get_request_store().clear()
    yield
    await get_request_store().clear()
