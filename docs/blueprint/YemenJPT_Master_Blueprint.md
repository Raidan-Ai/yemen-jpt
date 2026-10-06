# YemenJPT — Master Blueprint
## YemenJPT / YemenCore Sovereign Intelligence & Knowledge Platform

**Document status:** Architecture Blueprint  
**Scope:** Product, intelligence, multi-agent, knowledge, data, event-driven, investigation, UI/UX, deployment and roadmap  
**Primary language:** Arabic / English technical terminology where appropriate  
**Architecture principle:** Evidence-first, provenance-preserving, event-driven, case-centric, human-governed

---

## 1. Executive Definition

YemenJPT is a Yemeni sovereign AI and knowledge platform designed for journalism, research, investigation, media intelligence, OSINT, GEOINT, verification, narrative analysis and knowledge management.

It is **not** fundamentally a chatbot, a news reader, or a conventional RAG application.

The platform is built around **YemenCore**, a living knowledge and intelligence layer that continuously transforms heterogeneous Yemeni information into structured events, entities, relationships, narratives, signals and temporal knowledge.

The conceptual transformation is:

```text
Raw Reality
    ↓
Data Sources
    ↓
Ingestion
    ↓
Events
    ↓
Specialized Intelligence Agents
    ↓
Verification + Context + Relationships
    ↓
YemenCore Memory
    ├── Knowledge Graph
    ├── Vector Memory
    ├── Temporal Memory
    └── Source / Raw Archive
    ↓
Intelligence Engines
    ├── Contradictions
    ├── Narratives
    ├── Signals
    ├── Trust
    ├── Influence
    ├── Silence
    └── Reconstruction
    ↓
Cases / Investigations
    ↓
YemenJPT Journalist Workspace
    ↓
Human Decision / Publication
```

The strategic objective is to build a **living representation of Yemen's information environment**, not merely generate text.

---

# 2. Product Identity

## 2.1 YemenJPT

YemenJPT is the **user-facing platform**.

It provides the interface through which journalists, researchers, investigators and authorized users interact with YemenCore.

Core experiences include:

- AI Chat
- Research Assistant
- Investigative Assistant
- Fact Check
- Disinformation Scanner
- OSINT Explorer
- Media Intelligence
- GEOINT
- Document Intelligence
- Archive Assistant
- Knowledge Graph
- Timeline Builder
- Narrative Intelligence
- Reports
- Translation
- Writing Studio
- Governance / Legal / NGO workflows
- Mission Center
- Agent Marketplace

The user should not need to understand model routing, vector databases, queues, agent orchestration or infrastructure.

**YemenJPT is the work environment.**

---

# 3. YemenCore

## 3.1 Definition

YemenCore is the central knowledge, memory and intelligence layer.

Its purpose is to maintain a continuously evolving representation of:

- People
- Organizations
- Locations
- Events
- Documents
- News
- Claims
- Statements
- Sources
- Relationships
- Narratives
- Signals
- Indicators
- Contradictions
- Historical context
- Temporal changes

The strategic distinction is:

> YemenJPT is the platform; YemenCore is the underlying knowledge and intelligence system.

---

## 3.2 YemenCore as Living Memory

YemenCore should not be treated as a static knowledge base.

It should support:

```text
Past
 ↓
Current State
 ↓
New Event
 ↓
Relationship Update
 ↓
Verification
 ↓
Narrative Update
 ↓
Profile Update
 ↓
Signal Update
```

The system therefore preserves history rather than replacing old information whenever a new event arrives.

---

# 4. Core Architectural Principles

## 4.1 Evidence First

The system begins with evidence and provenance rather than an answer.

## 4.2 Provenance Preservation

Every significant intelligence output must retain links to its source events and evidence.

## 4.3 Fact / Inference Separation

The system must distinguish:

```text
Observed Fact
Claim
Interpretation
Inference
Prediction
```

These are not interchangeable.

## 4.4 Confidence Propagation

Confidence should be represented explicitly and updated as new evidence appears.

## 4.5 No Hallucination

Agents must not fabricate:

- Sources
- Events
- People
- Quotes
- Relationships
- Locations
- Evidence

## 4.6 No Direct Agent-to-Agent Communication

Agents communicate through Events and the Event Bus.

```text
Agent A
   ↓
Event Bus
   ↓
Agent B
```

This makes the system traceable and modular.

## 4.7 Stateless Specialist Agents

Specialist workers should not maintain long-lived internal state.

Long-term state belongs in shared memory and case/entity stores.

## 4.8 Human Governance

The system assists professional judgment.

Final publication, sensitive interpretation and consequential decisions remain subject to human review.

---

# 5. Global System Architecture

```text
                         ┌──────────────────────┐
                         │      YEMENJPT        │
                         │ User / Journalist UI │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   API / Application  │
                         │      Gateway         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Orchestrator      │
                         │ Routing / Workflow   │
                         └──────────┬───────────┘
                                    │
                              EVENT BUS
                                    │
        ┌───────────────┬───────────┼──────────────┬───────────────┐
        ▼               ▼           ▼              ▼               ▼
     Ingestion        OSINT       News          Geo/Sat          NLP
        │               │           │              │               │
        └───────────────┴───────────┼──────────────┴───────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Intelligence Layer   │
                         ├──────────────────────┤
                         │ Verification         │
                         │ Knowledge Graph      │
                         │ Vector Memory        │
                         │ Narrative Intelligence│
                         │ Signal Radar         │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │     YemenCore        │
                         │      Memory          │
                         ├──────────────────────┤
                         │ Graph                │
                         │ Vector               │
                         │ Time-Series          │
                         │ Raw Archive          │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Intelligence Engines │
                         ├──────────────────────┤
                         │ Contradiction        │
                         │ Narrative            │
                         │ Trust                │
                         │ Silence              │
                         │ Influence            │
                         │ Reconstruction       │
                         │ Impact               │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Cases / Investigations│
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Journalist Workspace │
                         └──────────────────────┘
```

---

# 6. Data Source Layer

YemenCore can ingest heterogeneous sources.

## 6.1 News and Media

- News websites
- RSS
- News APIs
- Broadcast transcripts
- Media archives
- Local media
- International media

## 6.2 Open Web / OSINT

- Search engines
- Public databases
- Public websites
- Forums
- Public social content
- Telegram/public channels
- Domain intelligence

## 6.3 Institutional Sources

Potential source classes include:

- UN
- World Bank
- IMF
- OCHA
- WHO
- FAO
- UNICEF
- ACLED
- HDX
- ReliefWeb
- Government and official records
- Research centers

## 6.4 Geospatial / Remote Sensing

Potential source classes include:

- Satellite imagery
- Remote sensing APIs
- Night-light datasets
- Thermal data
- Fire / anomaly datasets
- Open geospatial data
- GIS layers

## 6.5 Economic / Behavioral Indicators

Examples include:

- Connectivity
- Economic indicators
- Public activity signals
- Media activity
- Time-series indicators

## 6.6 User-Provided Evidence

The system should also accept:

- PDFs
- DOCX
- Images
- Videos
- Audio
- URLs
- Spreadsheets
- Research files
- Archive material

---

# 7. Ingestion Architecture

The Ingestion Layer is deliberately separated from analysis.

## Ingestion Agent

Responsibilities:

- Collect raw data
- Preserve source metadata
- Normalize transport format
- Create initial Event
- Send Event to the Event Bus

It must not:

- Analyze
- Interpret
- Classify politically
- Summarize away source material
- Invent missing fields

Example:

```json
{
  "event_type": "news.ingested",
  "timestamp": "ISO-8601",
  "source": "source-id",
  "content": "...",
  "url": "...",
  "language": "ar",
  "raw_metadata": {}
}
```

---

# 8. Data Normalization

Normalization converts heterogeneous input into consistent machine-readable structures.

Responsibilities:

- Schema normalization
- Timestamp normalization
- Language metadata
- Source identifiers
- Location normalization
- Entity references
- Event typing

Rule:

> Normalize the data without introducing new information.

---

# 9. Event Bus

The Event Bus is the nervous system of YemenCore.

Possible implementations from the architecture include:

- Redis Streams
- NATS JetStream
- Kafka + Schema Registry
- Cloudflare Queues in a Cloudflare-native deployment

The implementation can change without changing the conceptual protocol.

---

## 9.1 Event Schema

```json
{
  "event_id": "uuid",
  "event_type": "string",
  "event_version": "1.0",
  "timestamp": "ISO-8601",
  "source_agent": "agent_name",
  "target_agents": [],
  "priority": "low|medium|high|critical",
  "region": "Yemen|MENA|Global",
  "language": "ar|en",
  "payload": {},
  "context": {
    "related_events": [],
    "entities": [],
    "confidence": 0.0
  },
  "security": {
    "classification": "public|internal|sensitive",
    "verification_level": "unverified|partial|verified"
  }
}
```

---

# 10. Multi-Agent Architecture

## 10.1 Orchestrator Agent

Role:

**System coordination and workflow control.**

Responsibilities:

- Route events
- Assign tasks
- Prioritize signals
- Escalate important cases
- Coordinate workflows
- Maintain system coherence
- Handle agent output conflicts

The Orchestrator should not replace specialist analysis.

---

## 10.2 OSINT Agent

Role:

**Open-source intelligence extraction.**

Inputs:

- Public social content
- Telegram
- Forums
- Public databases
- Search
- OSINT datasets

Outputs:

- Entities
- Events
- Signals
- Confidence

Constraints:

- No unsupported identity attribution
- No hidden/private inference
- Observable public evidence only

---

## 10.3 News Intelligence Agent

Role:

**Convert news flow into structured intelligence.**

Capabilities:

- Article parsing
- Event extraction
- Source analysis
- Credibility signals
- Duplicate detection
- Narrative extraction
- Story evolution
- Same-event/different-framing detection

---

## 10.4 NLP Intelligence Agent

Role:

**Semantic understanding layer.**

Capabilities:

- Named Entity Recognition
- Event extraction
- Claim extraction
- Sentiment
- Stance
- Multilingual normalization
- Structured semantic output

---

## 10.5 Verification Agent

Role:

**Cross-source verification.**

Responsibilities:

- Compare claims
- Compare independent sources
- Track supporting evidence
- Track contradictory evidence
- Assign verification state
- Preserve uncertainty

Suggested result states:

```text
verified
partially_verified
mixed
false
unverified
unknown
```

---

## 10.6 Geo / Satellite Intelligence Agent

Role:

**Physical-world evidence layer.**

Capabilities:

- Infrastructure change detection
- Geographic change detection
- Thermal anomalies
- Night-light variation
- Temporal imagery comparison
- Spatial correlation

Rule:

> Describe observable physical changes separately from interpretation of intent.

---

## 10.7 Knowledge Graph Agent

Role:

**Build the Yemen Reality Graph.**

Nodes may include:

```text
Person
Organization
Location
Event
Document
Source
Claim
Narrative
```

Edges may include:

```text
PARTICIPATED_IN
LOCATED_IN
AFFILIATED_WITH
SAID
REPORTED
RELATED_TO
CONTRADICTS
SUPPORTS
OCCURRED_BEFORE
FOLLOWED_BY
```

The exact ontology should evolve under schema governance.

---

## 10.8 Vector Memory Agent

Role:

**Semantic memory and retrieval.**

Responsibilities:

- Generate embeddings
- Retrieve similar events
- Find related documents
- Cluster semantic material
- Support RAG
- Expand investigation context

It must preserve original evidence rather than replacing it with embeddings.

---

## 10.9 Narrative Intelligence Agent

Role:

**Map how different actors represent the same reality.**

Capabilities:

- Narrative clustering
- Narrative comparison
- Framing analysis
- Narrative evolution
- Propaganda-pattern detection
- Contradiction mapping

It must not automatically declare a narrative true or false.

---

## 10.10 Signal Radar / Alert Agent

Role:

**Early warning and anomaly detection.**

Inputs:

- OSINT activity
- News spikes
- Graph changes
- Satellite anomalies
- Historical patterns
- Time-series signals

Outputs:

- Risk score
- Event probability
- Signal type
- Confidence
- Alert priority

Prediction must always remain probabilistic.

---

## 10.11 Journalist Interface Agent

Role:

**Translate machine intelligence into professional human-readable outputs.**

Outputs:

- Investigation brief
- News report
- Timeline
- Fact sheet
- Case summary
- Contradiction explanation
- Evidence summary

Rules:

- No fabricated facts
- Preserve source diversity
- Preserve uncertainty
- Keep fact and inference separate

---

# 11. Shared Memory Architecture

YemenCore should use different memory systems for different information structures.

## 11.1 Graph Memory

Best for:

- Relationships
- Entities
- Events
- Networks
- Temporal relationships

Candidates:

- Neo4j
- TypeDB

## 11.2 Vector Memory

Best for:

- Semantic similarity
- RAG
- Document retrieval
- Narrative clustering
- Similar historical events

Candidates:

- Milvus
- Qdrant
- Weaviate
- Cloud-native vector service where appropriate

## 11.3 Time-Series Memory

Best for:

- Event frequency
- Activity changes
- Signal trends
- Historical indicators
- Temporal anomaly detection

Candidates:

- TimescaleDB
- InfluxDB

## 11.4 Object / Archive Storage

Best for:

- Original documents
- Images
- Raw articles
- Satellite imagery
- OSINT dumps
- Media

Candidates:

- S3
- Cloudflare R2
- MinIO

---

# 12. Intelligence Engine Layer

The Intelligence Engines sit above the memory layer.

## 12.1 Disputed Truth Record

A persistent record of:

- Claims
- Evidence
- Supporting sources
- Contradicting sources
- Verification state
- Corrections
- Confidence

## 12.2 Temporal Contradiction Engine

Tracks statements and behavior over time.

```text
Statement A
     ↓
Statement B
     ↓
Conflict detected
     ↓
Timeline context
     ↓
Human review
```

## 12.3 News Reconstruction Engine

Reconstructs an event from multiple sources.

Possible output:

```text
What happened?
What is directly supported?
What is disputed?
What changed over time?
Which sources appeared first?
Which claims were later corrected?
```

## 12.4 Narrative Engine

Builds a structured representation of competing narratives.

```text
Event
 ├── Narrative A
 ├── Narrative B
 ├── Narrative C
 └── International framing
```

## 12.5 Media Silence Engine

Looks for meaningful gaps:

- What was covered?
- What was ignored?
- When did coverage stop?
- Which sources remained silent?

Silence is a signal, not proof of intent.

## 12.6 Source Trust Layer

Maintains historical source behavior.

Potential dimensions:

- Accuracy history
- Correction history
- Independence signals
- Consistency
- Domain-specific reliability

Trust should be contextual, not a single universal number.

## 12.7 Influence Map

Represents relationships among:

- Actors
- Organizations
- Media
- Channels
- Narratives
- Events

## 12.8 Signal Radar

Ranks emerging signals according to factors such as:

- Strength
- Speed
- Risk
- Impact
- Historical relevance
- Cross-source confirmation

---

# 13. Political / Behavioral Profiles

YemenCore's strategic design includes living profiles for entities such as:

- Officials
- Politicians
- Institutions
- Journalists
- Activists
- Media channels
- Organizations

A profile can contain:

```text
Identity
Timeline
Statements
Actions
Relationships
Affiliations
Narratives
Contradictions
Evidence
Historical behavior
Confidence
```

This should be implemented as evidence-linked analytical context, not as unsupported labeling.

---

# 14. Case-Centric Architecture

The primary unit of investigative work is a **Case**.

Example:

```text
CASE: Currency Crisis

├── Overview
├── Evidence
├── Events
├── Timeline
├── Entities
├── Organizations
├── Locations
├── Sources
├── Claims
├── Verification
├── Narratives
├── Contradictions
├── Signals
├── Graph
├── Map
└── Reports
```

A Case should preserve its history and evidence relationships.

---

# 15. Entity Profiles

Each significant entity can have a living profile.

Example:

```text
ENTITY
 ├── Identity
 ├── Aliases
 ├── Organizations
 ├── Locations
 ├── Statements
 ├── Events
 ├── Relationships
 ├── Timeline
 ├── Narrative Position
 ├── Contradictions
 └── Evidence
```

The profile must distinguish observed information from model-generated interpretation.

---

# 16. Journalist Workspace

The UI should hide technical complexity.

## Dashboard

Shows:

- Active cases
- Breaking signals
- Verification queue
- Recent events
- Important entities
- Narrative shifts

## News Analysis

User provides a URL or article.

System returns:

1. Extracted facts
2. Claims
3. Sources
4. Confidence
5. Contradictions
6. Related cases
7. Related historical events

## Signal Radar

Visualizes:

- Trending signals
- Abnormal activity
- Predicted events
- Risk heatmap

## Narratives

Compare:

- Official narrative
- Local narrative
- International narrative
- Alternative narratives
- Contradictions

## Entity Profiles

Show:

- Profile
- Timeline
- Network
- Statements
- Contradiction tracker

## Investigation Builder

Workflow:

```text
Select Case
    ↓
Select Evidence
    ↓
Analyze
    ↓
Build Timeline
    ↓
Draft
    ↓
Journalist Review
    ↓
Publish / Export
```

---

# 17. Investigation Canvas

An advanced interface can combine:

```text
Timeline + Map + Graph + Evidence + Narratives
```

The journalist should be able to move between:

- What happened?
- Who was involved?
- Where?
- When?
- What evidence exists?
- What do different sources say?
- What changed?
- What remains unknown?

---

# 18. Narrative Operating System

This is a future architectural direction rather than an MVP dependency.

A Case can evolve into a living narrative:

```text
Beginning
   ↓
Actors
   ↓
Events
   ↓
Narratives
   ↓
Turning Points
   ↓
Contradictions
   ↓
Corrections
   ↓
Current State
```

The Narrative Operating System should maintain the history of how an issue evolves.

---

# 19. Autonomous Newsroom

Future capability:

```text
Monitoring Agent
       ↓
Discovery
       ↓
Verification
       ↓
Analysis
       ↓
Narrative Review
       ↓
Drafting
       ↓
Human Editorial Review
       ↓
Publication
```

Automation should stop short of uncontrolled publication unless explicit governance permits it.

---

# 20. Adversarial Narrative Engine

Future capability for examining competing explanations.

The system can model:

```text
Narrative A
Narrative B
Narrative C
     ↓
Evidence comparison
     ↓
Contradictions
     ↓
Unresolved questions
```

The goal is not to manufacture political positions but to expose competing information structures.

---

# 21. Corrective Memory

YemenCore should remember corrections.

For example:

```text
Original Claim
     ↓
Published
     ↓
Correction
     ↓
Reason
     ↓
New Evidence
     ↓
Updated State
```

This prevents the knowledge layer from silently forgetting previous errors.

---

# 22. Narrative Recycling Detector

Detects when an old claim, image, story or narrative is repackaged as new.

Potential dimensions:

- Text similarity
- Image similarity
- Event similarity
- Temporal mismatch
- Source lineage

---

# 23. Silence Mapping

Maps information gaps over time and across sources.

Example:

```text
Event occurs
   ↓
Source A reports
Source B reports
Source C silent
Source D reports later
   ↓
Coverage evolution
```

Silence should be presented as an observation, not automatically as evidence of coordination.

---

# 24. Digital Twin Lite

Long-term research direction.

A simplified Yemen model could represent:

- Population/activity
- Infrastructure
- Connectivity
- Economy
- Conflict events
- Media activity
- Narrative activity

The objective would be scenario exploration rather than claiming to predict reality exactly.

---

# 25. Cloud-Native Deployment Model

A Cloudflare-native implementation can map the architecture to:

## Workers

```text
ingestion-worker
intelligence-worker
verification-worker
signal-radar-worker
geo-worker
narrative-worker
orchestrator-worker
api-gateway-worker
```

## Queues

Examples:

```text
news.ingested
osint.discovery
intel.events
signal.events
geo.events
factcheck.events
narrative.events
```

## Durable Objects

### OrchestratorDO

Coordinates workflows and prevents duplication.

### CaseDO

Represents one investigation/case.

### EntityProfileDO

Maintains coordination around an entity profile.

## D1

Potentially stores:

- Users
- Event indexes
- Sources
- Audit logs
- Application metadata

## R2

Potentially stores:

- Raw articles
- Documents
- Images
- Satellite data
- OSINT archives

## Vector Database

Used for:

- Semantic search
- Similarity
- Clustering
- Narrative retrieval

The architecture is not tied permanently to Cloudflare. Cloudflare is one deployment model.

---

# 26. API Layer

The application API should expose high-level capabilities rather than exposing internal agent routing.

Conceptual routes:

```text
POST /ingest
POST /query
GET  /case/:id
GET  /entity/:id
GET  /timeline
GET  /signals
GET  /narratives
GET  /graph
POST /investigation
POST /verify
POST /report
```

Internal event routing remains hidden behind the API.

---

# 27. Security and Governance

YemenJPT handles potentially sensitive research data.

The platform should therefore support:

- Authentication
- Role-based access
- Case permissions
- Source classification
- Audit logs
- Evidence provenance
- Data retention policies
- Sensitive-data controls
- Agent/tool permissions
- Human approval gates

Suggested classification:

```text
public
internal
sensitive
restricted
```

---

# 28. Agent Governance

Every Agent should have:

```text
Agent ID
Version
Role
Allowed Inputs
Allowed Outputs
Tools
Model Policy
Permissions
Confidence Policy
Evidence Policy
Audit Trail
```

Agents should not gain unrestricted access to all data or tools by default.

---

# 29. Model Routing

YemenJPT should treat models as replaceable infrastructure.

The platform should be able to route different tasks to different models:

```text
Fast model
   → classification / extraction

Reasoning model
   → complex investigation

Coding model
   → engineering workflows

Vision model
   → image / satellite / media analysis

Embedding model
   → vector memory

Arabic specialist model
   → Arabic NLP / normalization
```

The application layer should not hard-code the user experience to a specific model vendor.

---

# 30. Agent Marketplace

YemenJPT can eventually expose specialized agents as reusable capabilities.

The project's conceptual agent ecosystem includes specialized identities such as:

- YARA
- Aftahan
- Nashwan
- Belqis
- Shamsan
- Al-Hamdani
- Suhail

These should be treated as **specialized agent personas/capability packages**, not as separate databases or independent architectures.

---

# 31. Mission Center

Mission Center is the operational control layer for complex tasks.

A Mission can represent:

```text
Mission
 ├── Objective
 ├── Case
 ├── Agents
 ├── Sources
 ├── Tasks
 ├── Events
 ├── Evidence
 ├── Status
 └── Outputs
```

Example:

> Investigate the evolution of a political event over 30 days.

The Orchestrator decomposes the mission into specialized tasks.

---

# 32. Example End-to-End Intelligence Flow

Scenario:

**Emerging political incident**

```text
1. Ingestion
   ↓
2. OSINT detects unusual public activity
   ↓
3. News Agent finds related reports
   ↓
4. NLP extracts entities / claims / events
   ↓
5. Geo Agent checks physical-world evidence
   ↓
6. Knowledge Graph links actors and events
   ↓
7. Vector Memory finds historical similarities
   ↓
8. Verification compares claims
   ↓
9. Narrative Agent identifies competing narratives
   ↓
10. Signal Radar evaluates anomaly / risk
   ↓
11. Orchestrator determines priority
   ↓
12. Case is created or updated
   ↓
13. Journalist Workspace receives structured briefing
```

This is the fundamental operating pattern of YemenCore.

---

# 33. MVP Architecture

The project should not attempt to build the complete vision at once.

The documented MVP agent set is:

```text
OSINT
News
NLP
Knowledge Graph
Alert
Journalist Interface
```

A practical MVP should additionally include the minimum infrastructure needed for:

```text
Ingestion
Event Bus
Source / Evidence Store
Vector Retrieval
Case Management
Verification
Basic UI
```

The goal is to prove the intelligence loop before building every advanced engine.

---

# 34. Phase 1 — Foundation

Build:

- YemenCore data model
- Source registry
- Ingestion
- Event schema
- Event Bus
- Basic NLP
- Basic OSINT
- News intelligence
- Vector search
- Knowledge graph
- Case model
- Basic verification
- Journalist workspace

Success criterion:

> The system can turn incoming Yemeni information into searchable, traceable, structured intelligence.

---

# 35. Phase 2 — Intelligence

Add:

- Temporal contradictions
- Narrative intelligence
- Entity profiles
- Trust layer
- Media silence
- News reconstruction
- Advanced verification
- Investigation canvas

Success criterion:

> The system can explain relationships and disagreements rather than merely retrieve documents.

---

# 36. Phase 3 — Early Warning

Add:

- Signal Radar
- Anomaly detection
- Risk scoring
- Cross-source signal correlation
- Scenario analysis
- Campaign detection
- Impact timelines

Success criterion:

> YemenCore can identify meaningful emerging patterns before they become obvious in a conventional search interface.

---

# 37. Phase 4 — Specialized Yemeni Intelligence

Long-term specialization:

- Yemeni Arabic NLP
- Yemeni political terminology
- Yemeni media language
- Yemeni place-name normalization
- Local source reliability models
- Historical Yemeni knowledge models
- Narrative analysis specialized for Yemen

Success criterion:

> YemenCore understands Yemen as a domain, rather than merely applying generic global AI models to Yemeni data.

---

# 38. What YemenJPT Is NOT

It should not be architecturally reduced to:

```text
Chatbot
```

or:

```text
Search Engine
```

or:

```text
RAG App
```

or:

```text
News Aggregator
```

or:

```text
Single AI Agent
```

or:

```text
Automatic Article Writer
```

These can exist as features, but none defines the platform.

---

# 39. The Core Mental Model

The entire project can be remembered as seven layers:

```text
1. YEMENJPT
   User Interface / Work Environment

2. YEMENCORE
   Knowledge + Intelligence Layer

3. AGENTS
   Specialized Cognitive Workers

4. EVENT BUS
   Nervous System / Event Flow

5. MEMORY
   Graph + Vector + Time + Archive

6. INTELLIGENCE ENGINES
   Verification + Narratives + Signals + Contradictions

7. CASES
   Human Investigation / Journalism Workflow
```

---

# 40. Final Architecture Statement

YemenJPT should ultimately be understood as:

> **A sovereign Yemeni intelligence and knowledge platform that continuously converts fragmented information about Yemen into traceable events, entities, relationships, narratives and signals, stores them as a living knowledge system through YemenCore, processes them through specialized multi-agent intelligence workers, and presents the resulting evidence and analysis through a case-centric workspace for journalists, researchers and investigators.**

The central innovation is not the number of AI models.

It is the combination of:

```text
Evidence
+
Events
+
Agents
+
Memory
+
Relationships
+
Time
+
Narratives
+
Verification
+
Human Investigation
```

That combination is what turns YemenJPT from an AI application into a **Yemen-focused Intelligence & Knowledge Operating System**.

---

# Appendix A — Canonical Component Map

```text
YemenJPT
│
├── Experience Layer
│   ├── Chat
│   ├── Research
│   ├── Investigation
│   ├── Verification
│   ├── OSINT
│   ├── GEOINT
│   ├── Media Intelligence
│   ├── Documents
│   ├── Reports
│   └── Mission Center
│
├── Application Layer
│   ├── API Gateway
│   ├── Cases
│   ├── Users
│   ├── Permissions
│   ├── Reports
│   └── Agent Registry
│
├── Orchestration Layer
│   ├── Orchestrator
│   ├── Mission Manager
│   ├── Workflow Engine
│   └── Event Router
│
├── Intelligence Agents
│   ├── Ingestion
│   ├── Normalization
│   ├── OSINT
│   ├── News
│   ├── NLP
│   ├── Verification
│   ├── Geo
│   ├── Satellite
│   ├── Knowledge Graph
│   ├── Vector Memory
│   ├── Narrative
│   ├── Signal Radar
│   └── Journalist
│
├── Event Layer
│   ├── Event Bus
│   ├── Event Schema
│   ├── Topics
│   ├── Provenance
│   └── Confidence
│
├── YemenCore Memory
│   ├── Graph
│   ├── Vector
│   ├── Time-Series
│   └── Raw Archive
│
├── Intelligence Engines
│   ├── Truth / Claims
│   ├── Contradiction
│   ├── Narrative
│   ├── Trust
│   ├── Silence
│   ├── Influence
│   ├── Reconstruction
│   ├── Impact
│   └── Campaign Detection
│
└── Governance
    ├── Authentication
    ├── Authorization
    ├── Audit
    ├── Security
    ├── Human Review
    └── Data Governance
```

---

# Appendix B — Core Event Lifecycle

```text
SOURCE
  ↓
INGEST
  ↓
NORMALIZE
  ↓
EVENT
  ↓
ROUTE
  ↓
ANALYZE
  ↓
VERIFY
  ↓
LINK
  ↓
STORE
  ↓
CORRELATE
  ↓
DETECT PATTERNS
  ↓
CREATE / UPDATE CASE
  ↓
JOURNALIST REVIEW
  ↓
REPORT / DECISION
```

---

# Appendix C — Core System Rules

1. Evidence before conclusion.
2. Every significant output must preserve provenance.
3. Facts and inference must remain distinguishable.
4. Predictions must remain probabilistic.
5. Narrative analysis must remain separate from factual verification.
6. Agents communicate through Events.
7. Long-term state belongs in shared memory.
8. Agents must not fabricate missing information.
9. Source diversity must be preserved.
10. Contradictions must be retained, not silently averaged away.
11. Corrections must become part of system memory.
12. Human editorial judgment remains authoritative for publication.

---

## Source Basis

This Blueprint consolidates the architecture and concepts contained in the project's YemenJPT/YemenCore materials, including the multi-agent architecture, Event Bus protocol, Cloudflare deployment concept, journalist interface, intelligence systems, strategic vision and future Narrative Operating System concepts.

Where an item is described as **Future**, **Advanced**, or **Candidate**, it should not be interpreted as an already implemented component.
