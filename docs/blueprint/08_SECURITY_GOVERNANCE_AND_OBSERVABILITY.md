# YemenJPT — Security, Governance and Observability

## 1. Security principles

- Least privilege.
- Explicit authentication.
- Role/permission enforcement.
- Secret isolation.
- Auditability.
- Data classification.
- Safe handling of sensitive source material.

## 2. Data classification

The Event contract includes:

```text
public
internal
restricted
```

The implementation should support stricter classifications if operationally required.

## 3. Agent permissions

Agents should receive only the tools/data required for their role.

Example:
- Ingestion: source connectors + archive write.
- NLP: source/event read + derived event write.
- Knowledge Graph: entity/event read + graph projection write.
- Journalist Interface: read intelligence + case/report write.
- Orchestrator: workflow/task control, not unrestricted raw data access by default.

## 4. Audit

Record:
- user actions,
- agent executions,
- model/provider calls where appropriate,
- Event creation,
- memory mutations,
- permission changes,
- human approvals,
- report publication.

## 5. Observability

Every workflow should be traceable using:
- correlation ID,
- event ID,
- agent ID,
- workflow/mission ID.

Metrics should cover:
- event throughput,
- processing latency,
- failures,
- retries,
- queue depth,
- agent execution time,
- model latency/cost where available,
- verification outcomes.

## 6. Evidence integrity

Where practical:
- hash raw evidence,
- preserve acquisition timestamps,
- retain source references,
- distinguish source content from derived content.

## 7. Governance

Human governance is part of the architecture, not a UI decoration.

The system must make uncertainty visible rather than hiding it behind fluent prose.
