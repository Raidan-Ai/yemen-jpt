# ADR-0004: SQLite + numpy for Vector Memory (MVP)

**Status:** Accepted  
**Date:** 2026-10-05  
**Deciders:** YemenJPT Architecture Team

---

## Context

YemenJPT requires vector memory for semantic retrieval — finding semantically similar entities, events, or documents without exact keyword matching. Production vector databases (Milvus, Qdrant, Weaviate, Pinecone) provide:

- Approximate nearest-neighbor (ANN) search at scale
- Filtering on metadata alongside vector similarity
- Persistent storage with HNSW / IVF indexes

Running a vector database adds operational complexity:
- Additional Docker service
- Index configuration and tuning
- Memory footprint (Milvus alone requires 8 GB+ RAM for production)

For MVP, the expected corpus is small (hundreds to low thousands of documents). Brute-force cosine similarity over numpy arrays is fast enough.

## Decision

**SQLite + numpy cosine similarity for MVP. `VectorMemoryStore` interface defined.**

```
VectorMemoryStore interface (abstract):
  upsert(id: str, vector: list[float], metadata: dict) -> None
  search(query_vector: list[float], top_k: int, filter: dict | None) -> list[SearchResult]
  delete(id: str) -> None
```

MVP implementation: `SqliteVectorMemory`
- SQLite database file for persistence (no Docker service required)
- Embeddings stored as BLOB (numpy `float32` array serialized via `numpy.tobytes()`)
- Search: load all vectors, compute cosine similarity with numpy, return top-k
- Metadata stored as JSON column in SQLite

## Alternatives Considered

| Option | Reason Not Selected for MVP |
|--------|---------------------------|
| Qdrant (embedded mode) | Embedded Qdrant is a viable option; chose SQLite+numpy to minimize non-Python dependencies |
| Chroma | Adds a dependency; SQLite+numpy has zero additional dependencies beyond `numpy` (already required) |
| FAISS | C++ extension; adds build complexity on Windows; SQLite+numpy is pure Python |
| pgvector (PostgreSQL extension) | Would eliminate separate SQLite; deferred: pgvector requires PostgreSQL extension install in Docker image; good future option |

## Consequences

**Positive:**
- Zero additional infrastructure for MVP
- Pure Python + numpy (numpy already required for NLP workloads)
- SQLite file is portable and inspectable
- Interface is preserved — no application code changes to swap provider

**Negative / Mitigations:**
- Brute-force O(n) search — not suitable for large corpora → acceptable for MVP (< 10k documents)
- No metadata filtering in brute-force path → post-filter after top-k for MVP
- SQLite concurrent writes limited → agents serialize vector writes via asyncio lock; acceptable for MVP

## Future Replacement Path

1. Deploy Qdrant (Docker) or pgvector (PostgreSQL extension)
2. Implement `QdrantVectorMemory(VectorMemoryStore)` or `PgVectorMemory(VectorMemoryStore)`
3. Migrate existing vectors (one-time script: `scripts/migrate_vectors.py`)
4. Update factory in `src/api/core/config.py`
5. Zero application-layer code changes required
