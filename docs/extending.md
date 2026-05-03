# Extending FoyerGate

FoyerGate is built so that you can add new capabilities without touching the core. Two extension points matter most:

* **Ecosystem adapters** — teach FoyerGate to handle a new package universe (PyPI, Maven, NuGet, container images, …).
* **Checkers** — add a new analysis (an AI-based heuristic, an internal SBOM signer, a custom license matcher, …).

This page outlines the contracts. The full API will be locked once the core stabilizes; until then, expect minor signature changes.

## Writing a checker

A checker is a class that:

1. Declares which ecosystems it supports.
2. Receives a quarantined artifact descriptor.
3. Returns a list of `Finding` objects.

Sketch:

```python
from foyergate.checkers.base import Checker, CheckContext
from foyergate.core.models import Finding, Severity


class MyCustomChecker(Checker):
    name = "my-custom"
    supported_ecosystems = ("npm",)

    async def check(self, ctx: CheckContext) -> list[Finding]:
        findings: list[Finding] = []
        # ctx.artifact_path  → path to the unpacked artifact
        # ctx.metadata        → parsed manifest (package.json for npm)
        # ctx.purl            → canonical Package URL
        if "suspicious-marker" in ctx.metadata.get("scripts", {}).get("postinstall", ""):
            findings.append(Finding(
                checker=self.name,
                category="malware",
                severity=Severity.high,
                rule_id="my-custom/suspicious-postinstall",
                title="Postinstall script contains suspicious marker",
                evidence={"script": ctx.metadata["scripts"]["postinstall"]},
            ))
        return findings
```

Register the checker by adding it to `pyproject.toml` under the `foyergate.checkers` entry point group (mechanism documented once the plugin loader lands).

### Guidelines

* **Be a pure observer.** Do not decide; only report. Verdicts come from the policy engine.
* **Be deterministic.** The same input must produce the same findings. Network calls to volatile sources (vulnerability feeds, etc.) should be cached.
* **Never execute the artifact.** Static analysis only, unless you opt into the sandbox runner.
* **Surface evidence.** Findings without evidence are noise. Include enough detail that a reviewer can confirm without re-running the tool.
* **Time-box external calls.** Use the timeout from `ctx.deadline`.

## Writing an ecosystem adapter

An adapter is the I/O layer for one package universe.

Sketch:

```python
from foyergate.adapters.base import EcosystemAdapter
from foyergate.core.models import Artifact, Manifest


class PyPIAdapter(EcosystemAdapter):
    name = "pypi"

    async def fetch(self, name: str, version: str) -> Artifact:
        ...

    async def parse_manifest(self, artifact: Artifact) -> Manifest:
        ...

    async def resolve_dependencies(self, manifest: Manifest) -> list[tuple[str, str]]:
        ...

    async def publish_to_internal_repo(self, artifact: Artifact, target: str) -> str:
        ...

    def build_purl(self, name: str, version: str) -> str:
        return f"pkg:pypi/{name}@{version}"
```

### Guidelines

* **One adapter per ecosystem.** Avoid sharing logic between unrelated registries; differences in resolution rules and metadata semantics matter.
* **Keep secrets out.** Adapters receive credentials via configuration, never embed them.
* **Be polite to upstreams.** Honor rate limits, set a recognizable `User-Agent`, cache where reasonable.

## Writing a policy

Policies are Rego modules consumed by OPA. They consume the findings array and the component descriptor and return a verdict.

A minimal example:

```rego
package foyergate.default

default verdict := "ALLOW"

verdict := "BLOCK" if {
    some f
    input.findings[f].severity == "critical"
}

reason := f.title if {
    some f
    input.findings[f].severity == "critical"
}
```

The full input schema and a starter policy will ship alongside the policy engine integration.
