# FoyerGate

> An OSS supply chain gateway: vet open-source packages **before** they enter your local repository.

**FoyerGate** is a self-hosted service that sits between the public npm registry and a Sonatype Nexus repository. Every package requested by a developer or CI pipeline is fetched into a **quarantine zone**, analyzed by a pluggable pipeline of checkers (vulnerabilities, licenses, malware indicators, metadata), and only **promoted** to the internal repo once it passes policy.

The project takes its name from the *foyer* — the small entryway where you stop, take off your boots, and check yourself before stepping into the house.

## Why FoyerGate?

Modern software supply chains are under attack. Typosquatting, dependency confusion, malicious post-install scripts, compromised maintainer accounts, and license drift are no longer hypothetical — they are weekly news. Most organizations rely on a local artifact mirror without a vetting layer in front of it: whatever the upstream registry serves, the local repo caches.

FoyerGate adds the missing **input control**: an explicit, auditable, policy-driven gate that decides what is allowed to enter your repository.

## Quickstart

> Requires Docker and Docker Compose v2.

```bash
git clone https://github.com/denimoll/foyergate.git
cd foyergate
cp .env.example .env
docker compose -f deploy/docker/compose.yaml up -d
```

Open the API documentation at <http://localhost:9876/docs>.

For local development setup (Python, hot reload, tests), see [docs/quickstart.md](docs/quickstart.md).

## Documentation

- [Quickstart](docs/quickstart.md) — get running in five minutes
- [Architecture](docs/architecture.md) — components and data flow
- [Concepts](docs/concepts.md) — checkers, policies, verdicts
- [API reference](docs/api.md) — HTTP contract
- [Extending](docs/extending.md) — write your own checker or ecosystem adapter
- [Operations](docs/operations.md) — deployment, monitoring, hardening

## Contributing

Contributions are welcome. For now, please open an issue first to discuss substantial changes.

If you discover a security issue, please follow [SECURITY.md](SECURITY.md).

## License

Apache License 2.0 — see [LICENSE](LICENSE).
