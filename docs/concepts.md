# Concepts

A short glossary of the vocabulary FoyerGate uses. Read this before reading the API reference or the source — it will save you back-and-forth.

## Component

A versioned package from a registry. Identified canonically by a [Package URL (PURL)](https://github.com/package-url/purl-spec):

```
pkg:npm/lodash@4.17.21
pkg:pypi/requests@2.32.3
pkg:maven/org.apache.commons/commons-lang3@3.14.0
```

PURLs let FoyerGate talk about components in an ecosystem-neutral way. They line up with CycloneDX, OSV, deps.dev, and most security tooling.

## Ecosystem

The package universe a component belongs to (`npm`, `pypi`, `maven`, …). Each ecosystem has an **adapter** that knows how to fetch, parse, and publish components in that universe.

## Request

A unit of work created by `POST /v1/requests`. A request has:

* a target component,
* a requester (user, CI job, or scheduled rescan),
* a state (`RECEIVED → FETCHING → ANALYZING → DECIDING → PROMOTING → DONE` / `BLOCKED` / `QUARANTINED` / `FAILED`),
* an eventual verdict.

Two requests for the same `(ecosystem, name, version)` deduplicate against a cached verdict if one exists and is still fresh.

## Checker

A pluggable analyzer that examines a quarantined artifact and emits a list of **findings**. Checkers are pure: they observe and report, they do not decide.

Categories shipped by default:

| Category        | Purpose                                                       |
| --------------- | ------------------------------------------------------------- |
| `metadata`      | Typosquatting, package age, maintainer signals.               |
| `vulnerability` | Known CVEs and GHSAs (Grype, OSV-Scanner).                    |
| `license`       | License detection and policy classification (ScanCode).       |
| `malware`       | Heuristic scanners (Guarddog, OSSGadget, custom YARA rules).  |
| `provenance`    | Sigstore / SLSA attestation verification.                     |

## Finding

A single observation from a checker. Fields:

* **checker** — which checker produced it (`grype`, `guarddog`, …).
* **category** — one of the categories above.
* **severity** — `critical` / `high` / `medium` / `low` / `info`.
* **rule_id** — stable identifier (`CVE-2024-XXXX`, `guarddog/exec-base64`, …).
* **title** — short human description.
* **evidence** — structured details (file paths, line numbers, version ranges, …).

Findings are inputs to the policy engine, not decisions themselves.

## Policy

A Rego module that consumes findings and component metadata and returns a verdict. Operators ship one or more **policy sets** — for example a `default` set and a `strict` set — and requesters can pick which set applies (subject to authorization).

Policy-as-code is what makes FoyerGate adaptable to different organizations without forking.

## Verdict

The final decision for a request:

* `ALLOW` — promote the artifact to the internal repository.
* `BLOCK` — do not promote; the requester gets a structured reason.
* `QUARANTINED` — hold for manual review; an authorized reviewer must approve or reject via the appeal flow.
* `PENDING` — analysis still in progress (only seen during async polling).
* `ERROR` — the analysis itself failed; not the same as `BLOCK`.

## Promotion

The act of publishing an `ALLOW`-verdict artifact from the quarantine bucket to the configured internal repository (Nexus npm hosted repo for the MVP).

## Rescan

A cron-driven re-evaluation of previously-allowed components. New CVEs land in databases every day; a verdict that was clean last week may not be clean today. When a rescan finds a regression, the component is flagged according to policy (notify, deprecate, or remove).

## Appeal

The authorized override path: when a `BLOCK` or `QUARANTINED` verdict is contested by a developer, an appeal request is opened. A reviewer with the right role can override the verdict, and the override is fully audited.
