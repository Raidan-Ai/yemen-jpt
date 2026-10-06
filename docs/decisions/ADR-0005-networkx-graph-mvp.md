# ADR-0005: networkx + PostgreSQL for Knowledge Graph (MVP)

**Status:** Accepted  
**Date:** 2026-10-05  
**Deciders:** YemenJPT Architecture Team

---

## Context

YemenJPT requires a knowledge graph to model relationships between entities (persons, organizations, locations, events, documents). Production graph databases (Neo4j, TypeDB, Amazon Neptune) provide:

- Expressive query languages (Cypher, TypeQL, SPARQL)
- Native graph storage with index-free adjacency
- Horizontal scaling for large graphs

Running a graph database adds operational complexity:
- Additional Docker service (Neo4j Community requires 1-2 GB RAM minimum)
- Query language expertise (Cypher/TypeQL)
- License considerations (Neo4j Community vs Enterprise)

For MVP, the knowledge graph is moderate in size (hundreds to low thousands of nodes/edges). Python's `networkx` library provides a full suite of graph algorithms with zero infrastructure.

## Decision

**networkx in-memory graph + PostgreSQL `graph_nodes` / `graph_edges` tables for persistence.**

```
KnowledgeGraphStore interface (abstract):
  add_node(id: str, label: str, properties: dict) -> None
  add_edge(source_id: str, target_id: str, relation: str, properties: dict) -> None
  get_neighbors(node_id: str, relation: str | None, depth: int) -> list[Node]
  shortest_path(source_id: str, target_id: str) -> list[str]
  subgraph(node_ids: list[str]) -> Graph
  delete_node(id: str) -> None
```

MVP implementation: `NetworkxKnowledgeGraph`
- `networkx.MultiDiGraph` for in-memory graph operations
- PostgreSQL `graph_nodes` and `graph_edges` tables for durability
- Graph loaded into memory on startup; writes go to both networkx and PostgreSQL
- All graph algorithm operations (BFS, shortest path, centrality) run against networkx

## Alternatives Considered

| Option | Reason Not Selected for MVP |
|--------|---------------------------|
| Neo4j Community (Docker) | Requires Docker service + Cypher expertise; 1-2 GB RAM footprint; license restrictions on scale |
| TypeDB | More expressive type system but steeper learning curve; community smaller than Neo4j |
| Amazon Neptune | Cloud-only; not suitable for local development |
| DGL (Deep Graph Library) | Focused on GNN training, not general knowledge graph operations |
| pgvector + recursive CTEs | PostgreSQL supports graph traversal via recursive CTEs; viable but verbose for complex queries |

## Consequences

**Positive:**
- Zero additional infrastructure for MVP
- `networkx` provides full graph algorithm library (centrality, community detection, path finding, clustering)
- PostgreSQL persistence ensures graph survives process restarts
- Interface is preserved — no application code changes to swap database

**Negative / Mitigations:**
- In-memory graph: large graphs consume RAM → acceptable for MVP (< 100k nodes)
- No Cypher/TypeQL: complex graph queries require Python code → acceptable; networkx API is expressive for the required queries
- Write path has dual-write latency (networkx + PostgreSQL) → async writes to PostgreSQL; networkx write is synchronous but fast

## Future Replacement Path

1. Deploy Neo4j Community (Docker) or AuraDB (cloud)
2. Implement `Neo4jKnowledgeGraph(KnowledgeGraphStore)` using `neo4j` Python driver
3. Migrate existing graph (one-time script: `scripts/migrate_graph.py` — reads PostgreSQL tables, writes to Neo4j)
4. Update factory in `src/api/core/config.py`
5. Zero application-layer code changes required
