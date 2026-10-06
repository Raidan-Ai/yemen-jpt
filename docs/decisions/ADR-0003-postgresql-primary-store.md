# ADR-0003: PostgreSQL as Primary Data Store

**Status:** Accepted  
**Date:** 2026-10-05  
**Deciders:** YemenJPT Architecture Team

---

## Context

YemenJPT requires a durable relational store for:

- Investigation cases, events, entities, users, audit logs
- Flexible event payloads (variable schema per event type)
- Graph node/edge persistence (MVP, backing networkx)
- Event bus durability (`events` table)
- Temporal memory (time-series queries)

The store must support async access from FastAPI/SQLAlchemy, schema migrations with rollback, and JSONB for semi-structured payloads.

## Decision

**PostgreSQL 15+ via SQLAlchemy 2.x async (`asyncpg` driver) + Alembic migrations.**

Key PostgreSQL features used:
- `JSONB` columns for event payloads and entity metadata (indexed, queryable)
- `asyncpg` — the fastest async PostgreSQL driver for Python
- `TIMESTAMPTZ` for all temporal data
- Full-text search (`tsvector`) for Arabic/English content (future)
- `TimescaleDB` extension path for time-series (future, non-breaking)
- Row-level security (future, for multi-tenant isolation)

## Alternatives Considered

| Option | Reason Not Selected |
|--------|-------------------|
| MySQL / MariaDB | Weaker JSONB support; `JSON` type is less capable; slower async driver ecosystem |
| SQLite | Not suitable for concurrent async writes from multiple agent coroutines; no JSONB |
| CockroachDB | Distributed complexity not needed for MVP; PostgreSQL wire-compatible (future migration path if needed) |
| MongoDB | Schema-less approach increases risk of data integrity issues across agents; harder to join with relational data |

## Consequences

**Positive:**
- JSONB enables flexible event payload schemas without separate document store
- `asyncpg` provides non-blocking I/O compatible with FastAPI's async handlers
- Alembic provides versioned, reversible schema migrations
- Single database service in `docker-compose.yml` for MVP (PostgreSQL handles relational, event store, graph persistence, and temporal memory)
- TimescaleDB upgrade path is non-breaking (extension install only)

**Negative / Mitigations:**
- Requires Docker for local development → already required; included in `docker-compose.yml`
- PostgreSQL graph queries are less expressive than Cypher/TypeQL → mitigated: networkx handles graph algorithms in-process; PostgreSQL stores nodes/edges as relational rows

## Future Replacement Path

- Alembic schema migrations remain portable; SQL schema is documented
- SQLAlchemy ORM abstracts provider differences for standard queries
- Raw SQL used only where necessary; annotated with comments for future portability
- TimescaleDB: `ALTER EXTENSION timescaledb INSTALL` — non-breaking upgrade
- Graph: replace PostgreSQL graph tables with Neo4j; application interface unchanged (see ADR-0005)
