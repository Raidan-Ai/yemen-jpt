# YemenJPT — Repository and Service Structure

## Recommended monorepo

```text
yemenjpt/
├── apps/
│   ├── web/                    # YemenJPT user interface
│   ├── admin/                  # administration/governance UI
│   └── api/                    # public/application API
│
├── services/
│   ├── orchestrator/
│   ├── ingestion/
│   ├── normalization/
│   ├── osint/
│   ├── news-intelligence/
│   ├── nlp-intelligence/
│   ├── verification/
│   ├── geo-intelligence/
│   ├── narrative-intelligence/
│   ├── signal-radar/
│   ├── knowledge-graph/
│   └── journalist-interface/
│
├── packages/
│   ├── contracts/              # Event/data schemas
│   ├── event-bus/
│   ├── provenance/
│   ├── confidence/
│   ├── auth/
│   ├── observability/
│   ├── database/
│   ├── ai/
│   └── ui/
│
├── schemas/
│   ├── events/
│   ├── entities/
│   ├── api/
│   └── config/
│
├── workflows/
│   ├── investigation/
│   ├── fact-check/
│   ├── osint/
│   └── reporting/
│
├── infrastructure/
│   ├── docker/
│   ├── migrations/
│   ├── deployment/
│   └── observability/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── workflow/
│   └── e2e/
│
├── docs/
│   ├── architecture/
│   ├── agents/
│   ├── api/
│   ├── operations/
│   └── decisions/
│
└── README.md
```

## Architectural rule

Do not create a microservice merely because a component is called an “agent”.

The logical agent boundary and deployment boundary are separate decisions.

For MVP, multiple agents may run in one worker/runtime while retaining independent contracts.

## Package ownership

`packages/contracts` is authoritative for machine-readable contracts.

`schemas/` contains versioned JSON Schema/OpenAPI artifacts generated or maintained from the implementation contract.

## Configuration

No secrets in source control.

Use environment/configuration management with explicit separation between:
- development,
- staging,
- production.
