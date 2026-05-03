"""Tests for POST /v1/requests and GET /v1/requests/{id}."""

from __future__ import annotations

from typing import Any

from httpx import AsyncClient

VALID_PAYLOAD: dict[str, Any] = {
    "ecosystem": "npm",
    "name": "lodash",
    "version": "4.17.21",
    "requested_by": "alice@example.com",
}


async def test_create_request_returns_202_with_metadata(client: AsyncClient) -> None:
    response = await client.post("/v1/requests", json=VALID_PAYLOAD)

    assert response.status_code == 202
    body = response.json()
    assert body["ecosystem"] == "npm"
    assert body["name"] == "lodash"
    assert body["version"] == "4.17.21"
    assert body["purl"] == "pkg:npm/lodash@4.17.21"
    assert body["state"] == "RECEIVED"
    assert body["verdict"] == "PENDING"
    assert body["requested_by"] == "alice@example.com"
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


async def test_get_request_returns_previously_created(client: AsyncClient) -> None:
    created = (await client.post("/v1/requests", json=VALID_PAYLOAD)).json()

    response = await client.get(f"/v1/requests/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


async def test_get_unknown_request_returns_404(client: AsyncClient) -> None:
    response = await client.get("/v1/requests/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["detail"] == "Request not found"


async def test_get_request_rejects_invalid_uuid(client: AsyncClient) -> None:
    response = await client.get("/v1/requests/not-a-uuid")
    assert response.status_code == 422


async def test_create_request_rejects_unknown_ecosystem(client: AsyncClient) -> None:
    payload = {**VALID_PAYLOAD, "ecosystem": "pypi"}
    response = await client.post("/v1/requests", json=payload)
    assert response.status_code == 422


async def test_create_request_rejects_extra_fields(client: AsyncClient) -> None:
    payload = {**VALID_PAYLOAD, "policy_set": "strict"}
    response = await client.post("/v1/requests", json=payload)
    assert response.status_code == 422


async def test_create_request_rejects_blank_fields(client: AsyncClient) -> None:
    payload = {**VALID_PAYLOAD, "name": ""}
    response = await client.post("/v1/requests", json=payload)
    assert response.status_code == 422


async def test_each_post_creates_a_new_request(client: AsyncClient) -> None:
    first = (await client.post("/v1/requests", json=VALID_PAYLOAD)).json()
    second = (await client.post("/v1/requests", json=VALID_PAYLOAD)).json()
    assert first["id"] != second["id"]
