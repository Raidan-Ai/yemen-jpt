# YemenJPT — Event and Data Contracts

## 1. Canonical Event

All inter-agent communication uses a canonical Event envelope.

Illustrative contract:

```json
{
  "event_id": "uuid",
  "event_type": "string",
  "event_version": "1.0",
  "occurred_at": "ISO-8601",
  "ingested_at": "ISO-8601",
  "source": {
    "source_id": "string",
    "source_type": "official|media|social|satellite|document|api|other",
    "uri": "string|null"
  },
  "case_id": "uuid|null",
  "correlation_id": "uuid",
  "producer": {
    "agent_id": "string",
    "agent_version": "string"
  },
  "payload": {},
  "evidence": [],
  "provenance": [],
  "confidence": {
    "score": 0.0,
    "label": "unknown|low|medium|high"
  },
  "classification": "public|internal|restricted",
  "metadata": {}
}
```

This is a starting implementation contract. Exact validation rules should be formalized in JSON Schema during implementation.

## 2. Evidence object

```json
{
  "evidence_id": "uuid",
  "type": "document|quote|image|video|dataset|observation|event",
  "source_id": "string",
  "locator": "string|null",
  "captured_at": "ISO-8601|null",
  "content_hash": "string|null",
  "excerpt": "string|null"
}
```

## 3. Provenance

Provenance answers:
- Where did this information originate?
- Which Event produced it?
- Which agent transformed it?
- Which evidence supports it?

Minimum conceptual chain:

```text
Source
 -> Raw Evidence
 -> Event
 -> Agent Transformation
 -> Derived Event
 -> Intelligence Result
```

## 4. Fact taxonomy

Every substantive statement should be classified as one of:

```text
FACT
CLAIM
INTERPRETATION
INFERENCE
PREDICTION
```

Do not collapse these categories.

## 5. Core entities

The Blueprint identifies these primary knowledge objects:

- Person
- Organization
- Location
- Event
- Document
- News Item
- Claim
- Statement
- Source
- Relationship
- Narrative
- Signal
- Indicator
- Contradiction
- Case

Each entity should have:
- stable identifier
- type
- created/updated timestamps
- provenance
- confidence where applicable
- temporal validity where applicable

## 6. Relationship principles

Relationships must be:
- typed,
- time-aware where relevant,
- evidence-backed,
- confidence-aware,
- traceable to source Events.

## 7. Immutable history principle

When new evidence conflicts with prior information, do not silently overwrite historical state.

Instead:
1. retain prior state,
2. emit a new Event,
3. create/update a contradiction or verification record,
4. preserve temporal validity,
5. expose the change to downstream intelligence.

## 8. TBD implementation decisions

The source material does not uniquely determine:
- final event-bus product,
- final graph database,
- final vector database,
- exact schema field types,
- exact event retention period,
- exact authentication protocol.

These must be selected during implementation and documented as architecture decisions.
