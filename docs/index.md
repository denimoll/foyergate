# FoyerGate Documentation

**FoyerGate** is a self-hosted gateway that vets open-source packages before they enter your local artifact repository. It sits between the public npm registry and your Sonatype Nexus, fetching components into a quarantine zone, running them through a pluggable pipeline of security checks, and only promoting them once a policy says "allow".

## Where to start

| If you want to…                         | Read                                         |
| --------------------------------------- | -------------------------------------------- |
| Run FoyerGate in five minutes           | [Quickstart](quickstart.md)                  |
| Understand how the pieces fit together  | [Architecture](architecture.md)              |
| Learn the vocabulary                    | [Concepts](concepts.md)                      |
| Use the HTTP API                        | [API reference](api.md)                      |
| Add a new checker or ecosystem          | [Extending FoyerGate](extending.md)          |
| Deploy and operate                      | [Operations](operations.md)                  |

## Mental model

```
Developer asks for a package
        │
        ▼
   FoyerGate API
        │
        ▼
  Quarantine fetch  ──►  Checker pipeline  ──►  Policy decision
  (S3, isolated)         (vuln, license,         (OPA / Rego)
                          malware, metadata,
                          provenance)
                                                       │
                       ┌───────────────────────────────┤
                       ▼                               ▼
                   ALLOW                            BLOCK / QUARANTINE
                       │                               │
                       ▼                               ▼
                Promote to Nexus                 Notify, audit, allow appeal
```

Read [Architecture](architecture.md) for a more thorough walkthrough.
