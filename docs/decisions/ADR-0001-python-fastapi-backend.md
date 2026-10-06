# ADR-0001: Python 3.12 + FastAPI for API Backend

**Status:** Accepted  
**Date:** 2026-10-05  
**Deciders:** YemenJPT Architecture Team

---

## Context

YemenJPT requires an API backend that:

- Supports fully async I/O for concurrent agent workloads
- Enforces strict schema validation at system boundaries
- Auto-generates an OpenAPI 3.1 specification (required for typed frontend client generation)
- Has first-class access to Python's AI/NLP library ecosystem (spaCy, transformers, sentence-transformers, networkx, numpy)
- Is compatible with SQLAlchemy 2.x async ORM and Alembic migrations

## Decision

**Python 3.12 + FastAPI + Pydantic v2 + SQLAlchemy 2.x (async) + Alembic**

- FastAPI is built on Pydantic v2 and Starlette; it generates OpenAPI 3.1 automatically from type annotations
- Pydantic v2 enforces strict typing at every system boundary (request validation, response serialization, event payloads, agent contracts)
- SQLAlchemy 2.x async (via `asyncpg`) provides non-blocking database access
- Alembic manages schema migrations with full rollback support
- Python 3.12 provides the best compatibility with the AI/NLP library ecosystem

## Alternatives Considered

| Option | Reason Not Selected |
|--------|-------------------|
| Node.js / NestJS | Weaker AI/NLP ecosystem; NLP libraries require Python subprocess bridges |
| Go / Fiber | Minimal AI/NLP library support; would require sidecar Python processes for all intelligence workloads |
| Java / Spring Boot | Heavyweight; AI/NLP ecosystem is Python-centric |

## Consequences

**Positive:**
- Single language for API + agents + AI layer reduces cognitive overhead
- Auto-generated OpenAPI spec enables typed client generation (`openapi-typescript`)
- Pydantic v2 is ~5-10x faster than v1 for validation

**Negative / Mitigations:**
- Python GIL limits true CPU parallelism for NLP workloads → mitigated by async I/O for network-bound operations and future agent decomposition into separate worker processes
- Slower cold start than Go → acceptable for server-side deployment; not a serverless function

## Future Replacement Path

- Services can be extracted to independent runtimes (Go, Rust) behind the same API contract
- Contracts are defined in JSON Schema / Pydantic models that are language-agnostic
- FastAPI → any HTTP server: the OpenAPI spec remains the stable contract
