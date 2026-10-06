# YemenJPT Implementation Status

_Last updated: 2026-10-05T22:56:46Z_

---

## Current State

- Empty repository with 11 architecture documents and `MANIFEST.json`
- No source code, no `package.json`, no `pyproject.toml`, no `docker-compose`, nothing
- OS: Windows (win32), working directory: `D:\YemenJPT`
- All architectural decisions are captured in this document and in `docs/decisions/`

---

## Architecture Mapping

| Layer | Technology Decision |
|-------|-------------------|
| **Experience Layer** | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| **API / Application Layer** | Python 3.12 + FastAPI, async, PostgreSQL via SQLAlchemy 2.x (async) + Alembic migrations |
| **Intelligence Agents** | Python modules within the API service (one module per agent), communicating via in-process Event Bus for MVP; interface supports future replacement with Redis Streams / NATS |
| **Event Bus** | In-process Python `EventBus` (asyncio publish/subscribe/acknowledge/dead-letter) backed by PostgreSQL `events` table; `RedisStreamsEventBus` adapter interface defined for future |
| **Knowledge Graph** | PostgreSQL + `networkx` for local graph operations (MVP); interface compatible with future Neo4j |
| **Vector Memory** | SQLite + numpy cosine similarity for local embeddings (MVP); interface compatible with future Milvus/Qdrant |
| **Temporal Memory** | PostgreSQL time-series table (MVP) |
| **Archive / Raw Storage** | Local filesystem + PostgreSQL metadata (MVP); interface compatible with future S3/R2/MinIO |
| **AI / Model Layer** | Abstract `ModelRouter` with capability-based routing; OpenAI-compatible provider + deterministic mock fallback when no provider configured |
| **Auth** | JWT-based authentication (`python-jose`), development mode allows bypass |

---

## Missing Components

All components — this is a greenfield build. Nothing exists yet.

### Backend (Python / FastAPI)
- `pyproject.toml` / `poetry.lock` / dependency manifest
- `src/api/` — FastAPI application, routers, middleware
- `src/api/core/config.py` — settings via `pydantic-settings`
- `src/api/core/logging.py` — structured JSON logging
- `src/api/core/auth.py` — JWT middleware
- `src/api/db/base.py` — SQLAlchemy async engine + session factory
- `src/api/db/models/` — ORM models: Case, Event, Entity, User, GraphNode, GraphEdge, VectorEntry, AuditLog
- `alembic/` — migration environment + initial migration
- `src/api/events/bus.py` — `InProcessEventBus` implementation
- `src/api/events/store.py` — PostgreSQL-backed event persistence
- `src/api/agents/base.py` — `BaseAgent` abstract class
- `src/api/agents/ingestion/` — Ingestion Agent
- `src/api/agents/normalization/` — Normalization Agent
- `src/api/agents/osint/` — OSINT Agent
- `src/api/agents/news_intelligence/` — News Intelligence Agent
- `src/api/agents/nlp_intelligence/` — NLP Intelligence Agent
- `src/api/agents/verification/` — Verification Agent
- `src/api/agents/knowledge_graph/` — Knowledge Graph Agent
- `src/api/agents/journalist_interface/` — Journalist Interface Agent
- `src/api/ai/router.py` — `ModelRouter` with capability-based dispatch
- `src/api/ai/providers/openai_compatible.py` — OpenAI-compatible provider
- `src/api/ai/providers/mock.py` — deterministic mock provider
- `src/api/knowledge/graph.py` — `NetworkxKnowledgeGraph` implementing `KnowledgeGraphStore`
- `src/api/memory/vector.py` — `SqliteVectorMemory` implementing `VectorMemoryStore`
- `src/api/memory/temporal.py` — `PostgresTemporalMemory`
- `src/api/storage/archive.py` — `LocalArchiveStore` implementing `ArchiveStore`
- `src/api/workflows/investigation.py` — Investigation workflow orchestrator
- `src/api/routers/cases.py`, `events.py`, `entities.py`, `users.py`, `health.py`
- Contract schemas: `src/contracts/` — JSON Schema / Pydantic models shared across layers

### Frontend (Next.js)
- `apps/web/package.json`, `tsconfig.json`, `next.config.ts`
- `apps/web/src/app/` — App Router layout, pages
- `apps/web/src/app/(investigation)/` — Investigation dashboard
- `apps/web/src/components/` — UI component library
- `apps/web/src/lib/api.ts` — typed API client

### Infrastructure
- `docker-compose.yml` — PostgreSQL, API service, web service
- `.env.example` — required environment variables

### Tests
- `tests/unit/` — unit tests for agents, event bus, models
- `tests/integration/` — API integration tests
- `tests/e2e/` — end-to-end Playwright tests

### Seed / Fixtures
- `scripts/seed.py` — development seed data
- `scripts/create_superuser.py`

---

## Technology Decisions (ADR References)

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | **Python 3.12 + FastAPI** for API backend | Strong async support, Pydantic v2 validation at system boundaries, auto-generated OpenAPI 3.1, strongest AI/NLP library ecosystem (spaCy, transformers, sentence-transformers) |
| 2 | **Next.js 14 App Router** for UI | Production-grade React with SSR, strong TypeScript support, Tailwind RTL support for Arabic, shadcn/ui accessible primitives |
| 3 | **PostgreSQL** as primary store | JSONB for flexible event payloads, asyncpg driver, mature Alembic migrations, future TimescaleDB extension for temporal memory |
| 4 | **In-process Event Bus** for MVP | Eliminates Redis/NATS as MVP dependency; interface preserved for future swap to `RedisStreamsEventBus` |
| 5 | **SQLite + numpy** for vector MVP | Eliminates Milvus/Qdrant as MVP dependency; interface preserved; zero additional infrastructure |
| 6 | **networkx** for graph MVP | Pure Python, zero infrastructure, full graph algorithm library; PostgreSQL provides persistence |
| 7 | **JWT authentication** | Standard, stateless, compatible with future identity providers (Keycloak, Auth0) |
| 8 | **Pydantic v2** for schema validation | Strict typing at all system boundaries; auto-generates JSON Schema for contracts |

_Full ADR text: `docs/decisions/ADR-000*.md`_

---

## TBD Decisions

| Decision | Current MVP Choice | Future Options | Notes |
|----------|-------------------|----------------|-------|
| Event bus product | In-process asyncio | NATS JetStream, Kafka, Redis Streams | Interface defined; drop-in replacement |
| Graph database | networkx + PostgreSQL | Neo4j, TypeDB | Interface defined; drop-in replacement |
| Vector database | SQLite + numpy | Milvus, Qdrant, Weaviate | Interface defined; drop-in replacement |
| Authentication provider | JWT (python-jose) | Keycloak, Auth0, custom OIDC | JWT as interchange format |
| Rate limiting strategy | TBD | SlowAPI, nginx, Cloudflare | To be decided before production |
| Pagination format | Cursor-based | — | Exact schema TBD |
| Archive storage | Local filesystem | S3, R2, MinIO | Interface defined |

---

## Implementation Order

### Phase 0 — Monorepo Scaffold, Contracts, Config, Observability Baseline
- Create monorepo directory structure (`apps/web/`, `src/api/`, `tests/`, `scripts/`, `docs/`)
- `pyproject.toml` with all dependencies pinned
- `apps/web/package.json` with all dependencies pinned
- Pydantic settings / `.env.example`
- Structured JSON logging baseline
- `docker-compose.yml` (PostgreSQL only at this stage)
- Contract schemas (`src/contracts/`)

### Phase 1 — Event Bus, Database Models, API Skeleton, Agents, AI Layer, Workflow
- PostgreSQL models + initial Alembic migration
- `InProcessEventBus` with PostgreSQL event persistence
- FastAPI application skeleton with health endpoint
- JWT middleware (dev bypass mode)
- All 8 agent modules (stub → minimal implementation)
- `ModelRouter` + OpenAI-compatible provider + mock provider
- `NetworkxKnowledgeGraph`, `SqliteVectorMemory`, `PostgresTemporalMemory`
- `LocalArchiveStore`
- Investigation workflow orchestrator
- Full REST API routers (cases, events, entities, users)

### Phase 2 — Investigation UI
- Next.js 14 App Router scaffold
- Typed API client (`src/lib/api.ts`)
- Investigation dashboard layout
- Case list, case detail, event timeline, entity graph views
- RTL / Arabic support

### Phase 3 — Tests, Seed Data, docker-compose Full Stack
- Unit tests for agents, event bus, models, AI router
- Integration tests for all API endpoints
- Seed script with realistic development data
- `docker-compose.yml` full stack (PostgreSQL + API + web)

### Phase 4 — Run, Verify, Fix
- `docker compose up` end-to-end smoke test
- Fix integration failures
- Verify all health endpoints
- Document local development setup in `README.md`

---

## Build Status

| Component | Status |
|-----------|--------|
| Monorepo structure | ⬜ Pending |
| Contracts / shared schemas | ⬜ Pending |
| Docker Compose (PostgreSQL) | ⬜ Pending |
| `pyproject.toml` + deps | ⬜ Pending |
| `apps/web/package.json` + deps | ⬜ Pending |
| PostgreSQL ORM models | ⬜ Pending |
| Alembic migrations | ⬜ Pending |
| Event Bus (`InProcessEventBus`) | ⬜ Pending |
| FastAPI application skeleton | ⬜ Pending |
| JWT auth middleware | ⬜ Pending |
| Ingestion Agent | ⬜ Pending |
| Normalization Agent | ⬜ Pending |
| OSINT Agent | ⬜ Pending |
| News Intelligence Agent | ⬜ Pending |
| NLP Intelligence Agent | ⬜ Pending |
| Verification Agent | ⬜ Pending |
| Knowledge Graph Agent | ⬜ Pending |
| Journalist Interface Agent | ⬜ Pending |
| AI Model Router | ⬜ Pending |
| OpenAI-compatible provider | ⬜ Pending |
| Mock AI provider | ⬜ Pending |
| Knowledge Graph (networkx) | ⬜ Pending |
| Vector Memory (SQLite+numpy) | ⬜ Pending |
| Temporal Memory (PostgreSQL) | ⬜ Pending |
| Archive Store (local FS) | ⬜ Pending |
| Investigation workflow | ⬜ Pending |
| REST API routers | ⬜ Pending |
| Investigation UI (Next.js) | ⬜ Pending |
| Typed API client | ⬜ Pending |
| Docker Compose (full stack) | ⬜ Pending |
| Unit tests | ⬜ Pending |
| Integration tests | ⬜ Pending |
| Seed data script | ⬜ Pending |
| README / local dev guide | ⬜ Pending |
