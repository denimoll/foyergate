"""Security and quality checkers.

Each checker implements the ``Checker`` interface from ``checkers.base``
and produces a list of ``Finding`` objects for a given artifact.

Checkers are pure analyzers: they do NOT decide whether to allow or
block a component. That decision belongs to the policy engine, which
consumes findings as input.

Categories shipped with the project:

* ``metadata``        — typosquatting, maintainer signals, package age.
* ``vulnerability``   — known CVEs / GHSAs (Grype, OSV-Scanner).
* ``license``         — license detection and policy classification.
* ``malware``         — heuristic scanners (Guarddog, OSSGadget, custom YARA).
* ``provenance``      — Sigstore / SLSA attestation verification.
"""
