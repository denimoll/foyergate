"""Component vetting requests.

* ``POST /v1/requests`` — submit a new request. Returns ``202 Accepted`` with
  the freshly created record (state ``RECEIVED``, verdict ``PENDING``).
* ``GET /v1/requests/{id}`` — fetch a previously submitted request.

In this milestone the request is held in process memory only. A worker will
later pick it up and walk the state machine through ``FETCHING → ANALYZING →
DECIDING → PROMOTING``.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from foyergate.core.models import ScanRequest, ScanRequestCreate
from foyergate.core.store import InMemoryRequestStore, get_request_store

router = APIRouter(prefix="/v1/requests", tags=["requests"])

StoreDep = Annotated[InMemoryRequestStore, Depends(get_request_store)]


@router.post(
    "",
    response_model=ScanRequest,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a new component vetting request",
)
async def create_request(
    payload: ScanRequestCreate,
    store: StoreDep,
) -> ScanRequest:
    request = ScanRequest.new(payload)
    await store.add(request)
    return request


@router.get(
    "/{request_id}",
    response_model=ScanRequest,
    status_code=status.HTTP_200_OK,
    summary="Fetch a previously submitted request",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Request not found"}},
)
async def read_request(
    request_id: UUID,
    store: StoreDep,
) -> ScanRequest:
    request = await store.get(request_id)
    if request is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Request not found")
    return request
