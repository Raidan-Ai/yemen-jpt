# YemenJPT — System Specification

## 1. System boundary

YemenJPT is the user-facing investigation and intelligence platform.

YemenCore is the shared knowledge, memory and intelligence layer.

The system converts heterogeneous source material into structured Events, enriches them with specialized agents, stores durable knowledge, runs intelligence engines, and presents evidence-backed results to human users.

## 2. Logical layers

### Layer A — Experience

Responsibilities:
- Authentication and user context.
- Chat and research experiences.
- Investigation/case workspace.
- Timeline, graph, narrative, verification and signal views.
- Reports and export.
- Mission Center.
- Agent Marketplace.

The UI must not expose low-level model/provider routing unless an administrative interface explicitly requires it.

### Layer B — Application / Case Layer

Responsibilities:
- Cases and investigations.
- Tasks/missions.
- User workflows.
- Human review states.
- Evidence collections.
- Report generation.
- Publication/export workflow.

### Layer C — Intelligence Layer

Responsibilities:
- OSINT collection.
- News intelligence.
- NLP intelligence.
- Verification.
- Narrative intelligence.
- GEO intelligence.
- Signal/risk analysis.
- Knowledge graph construction.
- Vector retrieval.
- Journalist briefing.

### Layer D — Event Layer

Responsibilities:
- Canonical event envelope.
- Event routing.
- Agent subscriptions.
- Retry/dead-letter handling.
- Event provenance.
- Correlation identifiers.

### Layer E — Memory Layer

Required conceptual stores:
- Knowledge Graph.
- Vector Memory.
- Temporal / time-series memory.
- Raw/document archive.

The exact database products are implementation choices unless explicitly fixed elsewhere.

### Layer F — Source / Ingestion Layer

Source classes defined by the Blueprint include:
- Official/government sources.
- International organizations.
- Media.
- Public social platforms.
- Satellite / remote sensing.
- Economic and behavioral indicators.
- Files and archives.

## 3. Global invariants

1. No fabricated evidence.
2. Every intelligence claim must be traceable to evidence.
3. Fact, claim, inference and prediction remain distinct.
4. Agents communicate through Events, not hidden direct calls.
5. Specialist agents remain stateless with durable state in shared stores.
6. Historical information is not silently overwritten.
7. Human review is required for consequential publication.
8. Future capabilities must not be hard dependencies of the MVP.

## 4. Primary flow

```text
Source
  -> Ingestion
  -> Normalization
  -> Event
  -> Agent processing
  -> Verification / enrichment
  -> Memory update
  -> Intelligence Engine
  -> Case
  -> Human review
  -> Output
```

## 5. Case-centric rule

A Case is the primary unit of human investigation.

A Case may reference:
- Events
- Sources
- Documents
- Entities
- Claims
- Relationships
- Narratives
- Signals
- Verification results
- Timelines
- Reports

## 6. MVP boundary

The Blueprint identifies the following minimal intelligence agents:
- OSINT
- News
- NLP
- Knowledge Graph
- Alert
- Journalist Interface

The build may additionally require the Orchestrator, Event infrastructure, normalization and verification as platform services.

Advanced systems such as Digital Twin Lite, Adversarial Narrative Engine and Autonomous Newsroom are not MVP blockers.
