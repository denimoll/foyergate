# Architecture

FoyerGate is a **gateway service**: it stands between public package registries and your internal artifact repository, and decides what is allowed to cross over. This page describes the moving parts and how a request flows through them.

## High-level diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                 │
│   Developer · CI · Cron rescanner · External integrations       │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS (REST)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FoyerGate API                              │
│  Auth · Validation · Idempotency · Rate limiting                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Orchestrator (state machine)                 │
│  RECEIVED → FETCHING → ANALYZING → DECIDING → PROMOTING → DONE   │
└──┬──────────┬──────────┬──────────┬──────────┬──────────┬──────┘
   │          │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼          ▼
┌──────┐ ┌────────┐ ┌─────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Fetch │ │Metadata│ │  Vuln   │ │License │ │Malware │ │  ...   │
│Worker│ │Checker │ │ Scanner │ │Scanner │ │Scanner │ │Checkers│
└───┬──┘ └───┬────┘ └────┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    │        └───────────┴──────────┴──────────┴──────────┘
    ▼                                  │
┌──────────┐                           ▼
│Quarantine│                  ┌─────────────────┐
│ Storage  │                  │  Policy Engine  │
│  (S3)    │                  │   (OPA/Rego)    │
└──────────┘                  └────────┬────────┘
                                       │ verdict
                                       ▼
                              ┌─────────────────┐
                              │    Promoter     │
                              │   → Nexus REST  │
                              └─────────────────┘

Cross-cutting: PostgreSQL (state) · Redis (cache+queue) ·
               Object storage (artifacts, SBOMs, reports) ·
               OpenTelemetry (tracing+metrics+logs)
```

## Request lifecycle

1. **Receive.** A client posts `POST /v1/requests` with `{ecosystem, name, version, requested_by, options}`. The API validates, dedupes (by PURL), and either returns a cached verdict or enqueues a job.
2. **Fetch.** A worker downloads the artifact from the upstream registry into the quarantine bucket. The artifact is hashed and never executed.
3. **Analyze.** Checkers run in parallel against the quarantined artifact. Each checker emits a list of `Finding` objects (severity + evidence).
4. **Decide.** All findings are submitted to OPA, which evaluates the active policy set and returns `ALLOW`, `BLOCK`, or `QUARANTINED` (the latter routes to manual review).
5. **Promote.** On `ALLOW`, the artifact is uploaded to the configured Nexus repository. The record (verdict + report + SBOM links) is persisted.
6. **Notify.** Webhooks fire on terminal states; the requester sees the verdict in the API response or via the original integration.

## Key design choices

These are short summaries.

* **Self-service first.** The first integration mode accepts explicit requests rather than transparently proxying. Simpler, more auditable, easier to ship. Operators who need transparent interception can wrap FoyerGate themselves.
* **Plugins for ecosystems and checkers.** The orchestrator is plugin-agnostic. New ecosystems and new analyzers (an AI-based heuristic checker, for instance) plug in via stable interfaces.
* **Policy as code.** Decisions live in OPA/Rego, not in Python. Different organizations get different policies without forking.
* **Quarantine before analysis.** Artifacts are downloaded into an isolated bucket and never executed by FoyerGate during static checks. Dynamic analysis (sandbox detonation) is a future, opt-in capability.

## What FoyerGate is **not**

* It is **not** a replacement for SCA at build time. SBOM generation and vulnerability scanning of your own builds remain a separate, complementary practice.
* It is **not** a registry. FoyerGate decides; Nexus stores and serves.
* It is **not** a developer-facing UI. The current surface is API-driven.

## Universality

FoyerGate is designed to be deployable by any organization that uses an internal artifact repository. The same engine handles:

* different ecosystems (via adapters),
* different checkers (via plugins),
* different organizational policies (via Rego),
* different deployment topologies.

The core never changes; everything organization-specific is configuration.
