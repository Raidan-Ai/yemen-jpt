# YemenJPT — MVP Implementation Plan

## Goal

Build the smallest production-shaped system that demonstrates the core YemenJPT thesis:

> evidence enters the system, specialized agents structure and analyze it, YemenCore retains the knowledge, and a journalist investigates the result through a case-centric interface.

## Phase 0 — Foundation

Deliver:
- monorepo
- configuration system
- local development environment
- contracts package
- Event schema
- basic API
- authentication placeholder/implementation
- observability baseline
- database migration framework

## Phase 1 — Core pipeline

Implement:
1. Ingestion
2. Normalization
3. Event Bus
4. OSINT
5. News Intelligence
6. NLP Intelligence
7. Verification
8. Knowledge Graph projection
9. Vector retrieval
10. Case storage

Primary demo:

```text
Source
 -> Ingestion
 -> Event
 -> NLP
 -> Verification
 -> Knowledge Graph
 -> Case
 -> Journalist View
```

## Phase 2 — Intelligence UX

Implement:
- investigation dashboard
- timeline
- evidence view
- entity view
- graph view
- verification panel
- narrative panel
- confidence/provenance UI
- report generation

## Phase 3 — Signals

Implement:
- Signal Radar
- temporal indicators
- anomaly detection
- alert workflow
- mission center

## Phase 4 — Advanced intelligence

Potential capabilities:
- political/behavioral profiles
- disputed truth record
- temporal contradiction engine
- media silence detection
- influence map
- narrative recycling detector
- corrective memory
- autonomous newsroom
- adversarial narrative engine
- Digital Twin Lite

These are not required to validate the initial MVP.

## Definition of MVP success

A user can:
1. create a Case,
2. ingest or collect source material,
3. see normalized Events,
4. run specialized analysis,
5. inspect entities/relationships,
6. compare evidence,
7. see uncertainty/conflicts,
8. review a timeline,
9. generate an evidence-backed brief,
10. trace the brief back to source evidence.

## Implementation discipline

The coding agent must:
- read all architecture documents before modifying the system,
- make explicit Architecture Decision Records for unresolved choices,
- avoid speculative infrastructure,
- avoid premature microservices,
- preserve contracts,
- write tests with each subsystem,
- keep future features behind clear boundaries.
