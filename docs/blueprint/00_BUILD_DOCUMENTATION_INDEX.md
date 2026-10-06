# YemenJPT — Build Documentation Index

## Purpose

This directory is the implementation contract for the YemenJPT / YemenCore platform.

The Master Blueprint defines the vision and architecture. These documents translate that architecture into instructions that a software-engineering agent can execute without silently redefining the system.

## Document hierarchy

1. `01_SYSTEM_SPECIFICATION.md` — authoritative system boundaries and components.
2. `02_AGENT_CONTRACTS.md` — specialist-agent responsibilities, inputs, outputs and constraints.
3. `03_EVENT_AND_DATA_CONTRACTS.md` — canonical Event, provenance, confidence and core entity contracts.
4. `04_KNOWLEDGE_MEMORY_SPECIFICATION.md` — Graph, Vector, Temporal and Archive memory responsibilities.
5. `05_API_SPECIFICATION.md` — initial service/API surface and endpoint intent.
6. `06_REPOSITORY_AND_SERVICE_STRUCTURE.md` — implementation repository layout.
7. `07_AGENT_RUNTIME_AND_ORCHESTRATION.md` — Event Bus, orchestration, workflow and execution rules.
8. `08_SECURITY_GOVERNANCE_AND_OBSERVABILITY.md` — security, permissions, audit and operational telemetry.
9. `09_TESTING_AND_ACCEPTANCE_SPECIFICATION.md` — testing strategy and acceptance criteria.
10. `10_MVP_IMPLEMENTATION_PLAN.md` — build order and MVP boundary.

## Authority rules

- The Master Blueprint is the source of product/architecture intent.
- These Build Documents are the source of implementation contracts.
- If a detail is not defined here or in the Blueprint, mark it `TBD` rather than inventing a requirement.
- Future capabilities must not become MVP dependencies.
- Preserve evidence, provenance and uncertainty throughout the pipeline.

## Core model

```text
YemenJPT
  = User Experience + Investigation Platform

YemenCore
  = Knowledge + Memory + Intelligence Layer

Agents
  = Stateless Specialized Cognitive Workers

Event Bus
  = Inter-Agent Communication Layer

Graph + Vector + Temporal + Archive
  = Shared Memory

Intelligence Engines
  = Analytical Layer

Cases
  = Unit of Human Investigation
```
