# Operations

This page covers running FoyerGate beyond the laptop: deployment topologies, monitoring, upgrades, and hardening.

## Deployment

The compose file at `deploy/docker/compose.yaml` brings up the full stack on a single host. It is suitable for evaluation, demos, and small teams.

```bash
docker compose -f deploy/docker/compose.yaml up -d
```

For production deployments — Kubernetes, air-gapped installations, multi-region setups — operators are expected to wrap the published Docker image in their own deployment manifests.

## Configuration

All settings are environment variables prefixed with `FOYERGATE_`. See `.env.example` at the repository root for the complete list with comments. Sensitive values (database passwords, registry credentials, S3 secret keys) should be sourced from a secret store (HashiCorp Vault, AWS Secrets Manager, Kubernetes Secrets, etc.), never committed.

## Observability

* **Logs:** structured JSON via `structlog`, written to stdout. Aggregate with Loki, Elasticsearch, or your stack of choice.
* **Metrics:** Prometheus endpoint at `/metrics`.
* **Traces:** OpenTelemetry, OTLP-exported.

## Hardening checklist

* Run the API behind authenticated ingress (mTLS, OIDC, or API tokens).
* Isolate the quarantine S3 bucket. No other workload should be able to read or write it.
* Restrict outbound network from workers to the upstream registry only — no SSRF surface.
* Run the OPA policy engine read-only in production; ship policy updates via CI.
* Pin and verify the Docker image digest, not just the tag.
* Rotate API tokens regularly; expire stale ones.
* Audit appeal events — a developer overriding a `BLOCK` is high-signal.
* Back up the Postgres database; the verdict and audit history live there.

## Upgrades

FoyerGate follows [semantic versioning](https://semver.org/). Database migrations are managed with Alembic and run on startup of the API service unless `FOYERGATE_DB_AUTOMIGRATE=false`. For production, run migrations as a separate job.

## Backup and disaster recovery

* **Postgres:** logical backups (`pg_dump`) on a schedule plus point-in-time recovery via WAL archiving.
* **Object storage:** version the quarantine and reports buckets; replicate to a second region for production.
* **Policies:** policies live in Git — the repository is the source of truth.

## Capacity planning

Sizing depends on:

* Request volume (peaks during build hours, near-zero at night).
* Average artifact size (npm packages: median ~50 KB, p99 ~5 MB).
* Checker pipeline cost (vulnerability scan dominates; budget ~5–15 seconds per artifact).

Indicative rule of thumb: one worker container handles ~10 requests/minute sustained. Scale workers horizontally; the API can run with two replicas behind a load balancer for HA.
