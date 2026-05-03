# API Reference

The HTTP API contract is defined in `openapi.yaml` at the root of the repository and served live by every running instance.

## Where to read it

* **Live, on a running instance:** <http://localhost:9876/docs> (Swagger UI) or <http://localhost:9876/redoc> (ReDoc).
* **Source of truth:** [`openapi.yaml`](https://github.com/denimoll/foyergate/blob/main/openapi.yaml) in this repository.
* **Raw JSON from a running instance:** <http://localhost:9876/openapi.json>.

## Versioning

* All endpoints are mounted under `/v1/...`.
* Backwards-incompatible changes will introduce a new prefix (`/v2/...`); the previous version stays available for at least one minor release.
* Additive changes (new optional fields, new endpoints) are not considered breaking.

## Authentication

FoyerGate supports API token authentication via the `Authorization: Bearer <token>` header.

## Endpoint groups

| Group           | Purpose                                              |
| --------------- | ---------------------------------------------------- |
| `/v1/requests`  | Submit and inspect component vetting requests.       |
| `/v1/components`| Look up known components and their verdict history. |
| `/v1/policies`  | Read and (with privilege) update policy sets.        |
| `/v1/rescan`    | Trigger ad-hoc rescans.                              |
| `/healthz`      | Liveness probe.                                      |
| `/readyz`       | Readiness probe.                                     |

The full schema for request and response bodies — including the `Verdict`, `Finding`, and `ComponentRef` models — is in `openapi.yaml`.
