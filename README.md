# YemenJPT

Evidence-first, provenance-preserving, event-driven, case-centric Yemeni intelligence platform.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 (async), asyncpg |
| Frontend | Next.js 14 (App Router), React, TailwindCSS, TypeScript |
| Database | PostgreSQL 15 |
| Events | In-process asyncio Event Bus |
| Graph | NetworkX (in-memory MVP) |
| AI | ModelRouter — deterministic `mock` provider by default |

## Architecture

```
Next.js UI  ──►  FastAPI API (/api/v1/)  ──►  Event Bus (asyncio)
                                                      │
                     ┌────────────────────────────────┴──────────────────┐
                     ▼                                                       ▼
              8 MVP Agents                                         YemenCore Memory
   Ingestion → Normalization → OSINT → News →                (PostgreSQL + in-memory graph)
   NLP → Verification → Knowledge Graph → Journalist
```

## Core Pipeline

```
source.submit → Ingestion → Normalization → OSINT → News Intelligence
   → NLP Intelligence → Verification → Knowledge Graph → Investigation Brief
```

Every stage preserves `source_id` provenance. Inference is never presented as fact;
mock output is labeled `[SYNTHETIC]`.

## Quick Start — Local (Docker)

```bash
docker compose up -d --build
# API:  http://localhost:8000
# UI:   http://localhost:3000
# Docs: http://localhost:8000/docs
```

## Quick Start — Local (bare metal)

**Prerequisites:** Python 3.12+, Node.js 20+, PostgreSQL 15

```bash
make install
docker compose up -d postgres
cp apps/api/.env.example apps/api/.env   # set DATABASE_URL
make dev          # API on :8000, UI on :3000
make seed         # load SYNTHETIC development fixtures
make test         # pytest
```

## Quick Start — GitHub Codespaces

1. Code → Codespaces → Create codespace on `main`
2. Wait for `.devcontainer/setup.sh` to finish (installs Python + Node deps)
3. `make dev` — ports 8000 / 3000 are auto-forwarded
4. `make seed` — optional synthetic fixtures

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/v1/cases` | List cases |
| `POST /api/v1/cases` | Create case |
| `GET /api/v1/cases/{id}/timeline` | Case timeline (events) |
| `GET /api/v1/cases/{id}/entities` | Extracted entities |
| `GET /api/v1/cases/{id}/evidence` | Evidence chain |
| `GET /api/v1/reports` | Reports for a case |
| `POST /api/v1/research` | Submit research pipeline |
| `POST /api/v1/fact-check` | Verify a claim |
| `GET /api/v1/missions` | Pipeline mission status |
| `GET /api/v1/graph` | Knowledge graph state |
| `GET /docs` | OpenAPI / Swagger UI |

## AI Provider

`MODEL_PROVIDER=mock` (default) → zero-dependency, fully offline, deterministic.
`MODEL_PROVIDER=openai` → set `OPENAI_API_KEY` for real model calls.

All AI output carries a confidence label. All AI output requires human editorial
review before publication. Never treat inference as verified fact.

## Security Notes

- No secrets in source control — `.env` files are gitignored, only `.env.example` is tracked
- All AI results require human review before publication
- Evidence provenance preserved at every pipeline step
- Architecture decisions: see `docs/decisions/` (ADRs)
- Reported vulnerabilities: open a **private** security advisory (Security tab), not a public issue