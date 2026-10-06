# YemenJPT — Testing and Acceptance Specification

## 1. Testing layers

### Unit tests
Validate:
- parsers,
- schema validation,
- confidence logic,
- provenance handling,
- entity normalization,
- deterministic transformations.

### Contract tests
Validate:
- Event schema compatibility,
- agent input/output contracts,
- API request/response contracts.

### Integration tests
Validate:
- Event Bus,
- memory projections,
- graph/vector/archive integration,
- workflow state transitions.

### Workflow tests
Validate complete scenarios:
- OSINT -> News -> NLP -> Verification.
- Event -> Knowledge Graph projection.
- Case -> timeline -> report.
- conflicting evidence -> contradiction handling.

### E2E tests
Validate user-visible investigation workflows.

## 2. Critical acceptance tests

### Evidence traceability
Given a generated intelligence result, a reviewer can navigate to the supporting evidence and originating Events.

### No fabricated evidence
If evidence is missing, the system returns uncertainty rather than inventing content.

### Contradiction preservation
Conflicting sources remain visible and produce a contradiction/uncertainty state.

### Agent isolation
Agents cannot bypass the Event Bus contract through undocumented direct state mutation.

### Retry safety
Replaying the same Event does not create duplicate durable entities/relationships unintentionally.

### Temporal preservation
New evidence does not silently erase prior historical state.

### Human review
Protected publication workflows cannot bypass configured approval gates.

## 3. Quality gates

A build is not considered MVP-ready until:
- contracts validate,
- critical workflows pass,
- provenance is demonstrable,
- failures are observable,
- secrets are not embedded,
- migrations are reproducible,
- local development setup is documented.

## 4. Test fixtures

Create synthetic fixtures for:
- single-source claim,
- multi-source agreement,
- conflicting claims,
- missing evidence,
- duplicate article,
- entity alias,
- historical update,
- signal anomaly,
- GEO observation.

Fixtures should not require real sensitive data for CI.
