# ADR-0002: In-Process Event Bus for MVP

**Status:** Accepted  
**Date:** 2026-10-05  
**Deciders:** YemenJPT Architecture Team

---

## Context

YemenJPT's architecture requires an Event Bus for agent-to-agent communication. The canonical pattern is a durable message broker (NATS JetStream, Kafka, Redis Streams) providing:

- Publish / subscribe
- Acknowledgement + retry
- Dead-letter queue
- Replay / audit trail

Running a full message broker adds significant operational complexity to local MVP development:
- Additional Docker service(s) to manage
- Broker-specific client libraries and connection management
- Operational expertise required for tuning

For MVP, all agents run within the same Python process. Cross-process fan-out is not required at this stage.

## Decision

**In-process Python `EventBus` (asyncio-based) backed by PostgreSQL `events` table for durability.**

```
EventBus interface (abstract):
  publish(event: Event) -> None
  subscribe(topic: str, handler: Callable) -> None
  acknowledge(event_id: str) -> None
  dead_letter(event_id: str, reason: str) -> None
```

MVP implementation: `InProcessEventBus`
- `asyncio` queues per topic
- PostgreSQL `events` table for persistence and audit trail
- Dead-letter table for failed deliveries

Future implementation: `RedisStreamsEventBus` (drop-in replacement, same interface)

## Alternatives Considered

| Option | Reason Not Selected for MVP |
|--------|---------------------------|
| Redis Streams | Requires Redis Docker service; adds ops complexity; not needed when all agents are in-process |
| NATS JetStream | Same concern; excellent choice for production scale-out |
| Kafka | Significantly heavier operational footprint; overkill for MVP agent count |
| Celery + Redis | Task queue, not event bus; harder to model event fan-out |

## Consequences

**Positive:**
- Zero additional infrastructure for MVP (PostgreSQL already required)
- Simpler local development (`docker compose up` needs only PostgreSQL)
- Full durability via PostgreSQL `events` table
- Interface is preserved — no application code changes required to swap broker

**Negative / Mitigations:**
- No cross-process fan-out in MVP → acceptable: all agents run in same process
- `asyncio` queue is in-memory; process crash loses in-flight events → mitigated by PostgreSQL persistence (events written before dispatch)
- Single-process throughput ceiling → acceptable for MVP; future scale-out replaces implementation, not interface

## Future Replacement Path

1. Implement `RedisStreamsEventBus(EventBus)` with same interface
2. Update `pyproject.toml` to include `redis[hiredis]`
3. Update `docker-compose.yml` to add Redis service
4. Change `EventBus` factory in `src/api/core/config.py` to select implementation
5. Zero application-layer code changes required
