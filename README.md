# System Documentation

YemenJPT — Sovereign Intelligence Platform

Evidence-first, provenance-preserving, event-driven, case-centric Yemeni intelligence platform.

## Quick Start

### Option 1: Docker (recommended)

```bash
# From the yemenjpt/ directory
docker compose up -d --build

# API:  http://localhost:8000
# UI:   http://localhost:3000
# Docs: http://localhost:8000/docs
```

### Option 2: Local Development

**Prerequisites:** Python 3.12+, Node.js 20+, PostgreSQL 15

```bash
# Install dependencies
make install

# Start PostgreSQL (or use Docker for just the DB)
docker compose up -d postgres

# Copy and configure env
cp apps/api/.env.example apps/api/.env
# Edit apps/api/.env — set DATABASE_URL

# Start API + UI
make dev

# Seed development data
make seed

# Run tests
make test
```

## Architecture

```
YemenJPT (Next.js UI)
    │
    ▼
FastAPI API (/api/v1/)
    │
    ▼
Event Bus (asyncio in-process)
    │
    ▼
8 MVP Agents:
  Ingestion → Normalization → OSINT → News Intelligence
  → NLP Intelligence → Verification → Knowledge Graph
  → Journalist Interface
    │
    ▼
YemenCore Memory (PostgreSQL + in-memory graph)
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/v1/cases` | List cases |
| `POST /api/v1/cases` | Create case |
| `GET /api/v1/cases/{id}/timeline` | Case timeline |
| `GET /api/v1/cases/{id}/entities` | Case entities |
| `POST /api/v1/research` | Submit research pipeline |
| `POST /api/v1/fact-check` | Verify a claim |
| `GET /api/v1/graph` | Knowledge graph state |
| `GET /docs` | Interactive API docs (Swagger) |

## AI Provider Configuration

Set `MODEL_PROVIDER=mock` (default) for zero-dependency local development.
Set `MODEL_PROVIDER=openai` and provide `OPENAI_API_KEY` for real intelligence.

All AI output is marked with confidence scores. Mock results are labeled `[SYNTHETIC]`.

## Security Notes

- No secrets in source control — use `.env` files
- All AI results require human review before publication
- Evidence provenance is preserved at every pipeline step
- See `docs/decisions/` for Architecture Decision Records
