# YemenJPT — Initial API Specification

## Status

This is the initial service boundary, not a final OpenAPI document.

The implementation agent should generate a versioned OpenAPI 3.1 specification from these contracts.

## 1. Authentication

Required for protected application endpoints.

Exact identity provider/protocol is TBD.

## 2. Cases

```text
GET    /api/v1/cases
POST   /api/v1/cases
GET    /api/v1/cases/{case_id}
PATCH  /api/v1/cases/{case_id}
GET    /api/v1/cases/{case_id}/timeline
GET    /api/v1/cases/{case_id}/entities
GET    /api/v1/cases/{case_id}/evidence
GET    /api/v1/cases/{case_id}/narratives
GET    /api/v1/cases/{case_id}/signals
```

## 3. Research / intelligence

```text
POST /api/v1/research
POST /api/v1/fact-check
POST /api/v1/osint/search
POST /api/v1/disinformation/analyze
POST /api/v1/narratives/analyze
POST /api/v1/geoint/analyze
```

These endpoints should create auditable tasks/events rather than perform opaque synchronous “magic”.

## 4. Events

```text
GET  /api/v1/events/{event_id}
POST /api/v1/events
GET  /api/v1/cases/{case_id}/events
```

Direct external Event creation should be permission-controlled.

## 5. Entities

```text
GET /api/v1/entities/{entity_id}
GET /api/v1/entities/{entity_id}/relationships
GET /api/v1/entities/{entity_id}/timeline
```

## 6. Reports

```text
POST /api/v1/reports
GET  /api/v1/reports/{report_id}
GET  /api/v1/reports/{report_id}/export
```

## 7. Missions

```text
GET  /api/v1/missions
POST /api/v1/missions
GET  /api/v1/missions/{mission_id}
POST /api/v1/missions/{mission_id}/cancel
```

## 8. Administrative APIs

Potential areas:
- users
- roles
- permissions
- agents
- models
- sources
- connectors
- system health
- audit logs

These require stronger authorization and should not be exposed as public user APIs.

## 9. API rules

Every intelligence response should expose or reference:
- evidence,
- provenance,
- confidence,
- processing status,
- relevant Event identifiers where appropriate.

## 10. Async-first rule

Long-running collection, analysis, GEOINT, batch processing and agent workflows should be asynchronous.

The API should return a task/mission identifier and allow status retrieval.

## 11. TBD

The Blueprint does not define exact:
- authentication provider,
- API gateway,
- rate limits,
- pagination format,
- error envelope,
- webhook contract.

The implementation agent must document these as explicit decisions.
