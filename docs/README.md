# YemenJPT Documentation

All specifications, architecture decisions, and implementation status for YemenJPT.

## Master Blueprint

| Doc | Purpose |
|-----|---------|
| [YemenJPT_Master_Blueprint.md](blueprint/YemenJPT_Master_Blueprint.md) | Full platform vision and architecture |
| [00_BUILD_DOCUMENTATION_INDEX.md](blueprint/00_BUILD_DOCUMENTATION_INDEX.md) | Index of the whole documentation set |

## Specifications

| # | Doc | Purpose |
|---|-----|---------|
| 01 | [System Specification](blueprint/01_SYSTEM_SPECIFICATION.md) | Scope, non-goals, system boundaries |
| 02 | [Agent Contracts](blueprint/02_AGENT_CONTRACTS.md) | Input/output contracts for every agent |
| 03 | [Event and Data Contracts](blueprint/03_EVENT_AND_DATA_CONTRACTS.md) | Event bus and canonical data model |
| 04 | [Knowledge & Memory Specification](blueprint/04_KNOWLEDGE_MEMORY_SPECIFICATION.md) | Memory planes and retrieval |
| 05 | [API Specification](blueprint/05_API_SPECIFICATION.md) | Endpoint definitions |
| 06 | [Repository & Service Structure](blueprint/06_REPOSITORY_AND_SERVICE_STRUCTURE.md) | Monorepo layout and boundaries |
| 07 | [Agent Runtime & Orchestration](blueprint/07_AGENT_RUNTIME_AND_ORCHESTRATION.md) | Runtime, scheduling, orchestration |
| 08 | [Security, Governance & Observability](blueprint/08_SECURITY_GOVERNANCE_AND_OBSERVABILITY.md) | Security model and audit requirements |
| 09 | [Testing & Acceptance Specification](blueprint/09_TESTING_AND_ACCEPTANCE_SPECIFICATION.md) | Test strategy and acceptance criteria |
| 10 | [MVP Implementation Plan](blueprint/10_MVP_IMPLEMENTATION_PLAN.md) | Phased build plan for the MVP |

## Architecture Decision Records

| ADR | Decision | Status |
|-----|----------|--------|
| [ADR-0001](decisions/ADR-0001-python-fastapi-backend.md) | Python + FastAPI backend | Accepted |
| [ADR-0002](decisions/ADR-0002-in-process-event-bus.md) | In-process asyncio Event Bus | Accepted |
| [ADR-0003](decisions/ADR-0003-postgresql-primary-store.md) | PostgreSQL as primary store | Accepted |
| [ADR-0004](decisions/ADR-0004-sqlite-numpy-vector-mvp.md) | SQLite + NumPy vector store for MVP | Accepted |
| [ADR-0005](decisions/ADR-0005-networkx-graph-mvp.md) | NetworkX in-memory graph for MVP | Accepted |

Any decision not covered here must be recorded as a new ADR (`ADR-0006+`) — a decision
without an ADR is not a decision.

## Implementation Status

- [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) — what is built, what is verified, what is missing
- [../README.md](../README.md) — quick start, endpoints, stack
- GitHub Issue #1 — live MVP build tracker

## Documentation Rules

1. Source code is the source of truth for *what exists*; docs describe *what should exist*.
2. Any spec/implementation divergence is a bug — fix the code or update the spec, never both silently.
3. Inference is never documented as fact. `[SYNTHETIC]` marks mock/fixture data everywhere.
4. No secrets, keys, tokens, or `.env` contents in this directory — ever.
