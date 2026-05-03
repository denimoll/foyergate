"""Ecosystem adapters.

One subpackage per supported ecosystem (npm, pypi, maven, …). Each adapter
implements the ``EcosystemAdapter`` interface from ``adapters.base`` and
knows how to:

* fetch an artifact from the upstream registry,
* parse its manifest and extract metadata,
* resolve declared dependencies,
* publish the artifact into the internal repository (e.g. Nexus).

Adapters do NOT make policy decisions and do NOT run security checks.
They only handle ecosystem-specific I/O and data shapes.
"""
