# YemenJPT — Agent Runtime and Orchestration

## 1. Runtime principle

The system is event-driven.

```text
Producer
  -> Event Bus
  -> Subscription / Routing
  -> Agent Worker
  -> Validation
  -> Event Bus
  -> Memory Projection / Next Agent
```

## 2. Event Bus responsibilities

- durable delivery where supported
- routing
- retries
- dead-letter handling
- correlation
- event ordering where required
- observability

The Blueprint allows Kafka/NATS or equivalent. The exact product is TBD.

## 3. Orchestrator

The Orchestrator is responsible for:
- task decomposition,
- routing,
- prioritization,
- workflow state,
- escalation,
- failure handling.

It should not become a monolithic reasoning layer containing every domain capability.

## 4. Workflow model

A workflow should expose explicit states.

Example:

```text
CREATED
  -> COLLECTING
  -> NORMALIZING
  -> ANALYZING
  -> VERIFYING
  -> READY_FOR_REVIEW
  -> APPROVED
  -> PUBLISHED
```

Failure paths should be explicit:

```text
FAILED
RETRYING
BLOCKED
CANCELLED
```

## 5. Idempotency

Agent processing should be idempotent where practical.

Use:
- event ID,
- correlation ID,
- deterministic projection keys,
- processing records.

An event must not create duplicate durable knowledge merely because a worker was retried.

## 6. Human-in-the-loop

Human review gates are required for consequential outputs.

At minimum, review should be possible before:
- publication,
- high-impact reporting,
- sensitive profile updates,
- high-risk inference,
- irreversible external actions.

## 7. Model routing

Model/provider routing belongs behind an internal abstraction.

Application logic should ask for capabilities such as:

```text
reasoning
coding
extraction
embedding
translation
vision
```

rather than hard-coding a provider throughout the application.

Exact providers/models are deployment decisions.
