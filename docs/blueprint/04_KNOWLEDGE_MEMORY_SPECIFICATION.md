# YemenJPT — Knowledge and Memory Specification

## 1. Memory model

YemenCore uses four conceptual memory planes.

### A. Knowledge Graph

Stores:
- entities
- relationships
- events
- temporal links
- provenance links

Primary use:
- relationship traversal
- entity context
- event chaining
- influence mapping

### B. Vector Memory

Stores:
- embeddings
- semantic representations
- similar-event clusters
- retrieval context

Primary use:
- semantic search
- RAG
- similarity
- context expansion

### C. Temporal Memory

Stores:
- time-series indicators
- historical signal values
- trend changes
- anomaly context

Primary use:
- signal radar
- historical comparison
- temporal analysis

### D. Raw / Document Archive

Stores:
- source documents
- raw captures
- media references
- source snapshots where permitted

Primary use:
- evidence preservation
- reproducibility
- re-processing

## 2. Write policy

Agents should not write arbitrary free-form intelligence directly into every store.

Prefer:

```text
Agent Output
  -> Canonical Event
  -> Validation
  -> Memory-specific projection
```

## 3. Read policy

Agents retrieve context through explicit tools/services.

The retrieval result must retain provenance.

## 4. Graph projection

The Knowledge Graph Agent transforms Events into graph operations.

Example conceptual projection:

```text
Event
  -> Entity extraction
  -> Entity resolution
  -> Relationship extraction
  -> Temporal qualification
  -> Evidence links
  -> Graph update
```

## 5. Vector projection

Relevant documents/events are embedded and indexed for semantic retrieval.

Embedding model/provider is an implementation decision.

## 6. Temporal projection

Indicators and measurements should be stored with:
- metric name
- value
- unit where applicable
- location/entity scope
- timestamp
- source
- confidence

## 7. Archive policy

Raw evidence should remain independently retrievable from derived intelligence.

A derived summary must never become the only surviving representation of the source evidence.
