# YemenJPT — Agent Contracts

## 1. Common agent contract

Every agent MUST define:

- `agent_id`
- `version`
- `purpose`
- `input_event_types`
- `output_event_types`
- `capabilities`
- `prohibited_actions`
- `confidence_policy`
- `provenance_policy`
- `failure_policy`

Every invocation is driven by an Event.

Every output is emitted as an Event.

Agents must not silently mutate another agent's state.

## 2. Ingestion Agent

### Purpose
Collect raw source material and normalize it into Events.

### Must
- Preserve source identity.
- Preserve raw payload/reference.
- Attach acquisition timestamp.
- Emit normalized Events.

### Must not
- Perform substantive analysis.
- Invent missing fields.
- Replace source text with an interpretation.

## 3. OSINT Agent

### Purpose
Collect open-web/public-source intelligence.

### Must
- Gather publicly available source material.
- Preserve URLs/source identifiers.
- Record acquisition metadata.
- Emit source/evidence Events.

### Must not
- Treat collection as verification.
- State conclusions unsupported by source evidence.

## 4. News Intelligence Agent

### Purpose
Process news material.

### Must
- Parse articles.
- Identify source metadata.
- Extract claims/entities/events.
- Detect likely duplicates.
- Preserve original article evidence.

### Must not
- Convert publication into truth.
- Remove contradictory reports.

## 5. NLP Intelligence Agent

### Purpose
Perform linguistic structuring.

### Capabilities
- Named entity recognition.
- Event extraction.
- Claim extraction.
- Multilingual normalization.
- Sentiment/stance where appropriate.

### Constraint
NLP output is structured interpretation of source material, not independent factual verification.

## 6. Verification Agent

### Purpose
Compare claims/evidence across sources.

### Output states
- `true`
- `false`
- `mixed`
- `unknown`

The exact decision must remain evidence-backed.

### Must
- Preserve supporting and contradicting evidence.
- Preserve uncertainty.

### Must not
- Infer truth from source reputation alone.

## 7. Signal Radar Agent

### Purpose
Detect anomalies and possible early signals.

### Must
- Produce probabilistic signals.
- Reference historical/current evidence.
- State confidence.

### Must not
- Present predictions as facts.
- Infer intent without evidence.

## 8. Geo Intelligence Agent

### Purpose
Analyze satellite/geospatial change.

### Must
- Describe observable physical changes.
- Preserve imagery/source metadata.
- Emit geospatial evidence.

### Must not
- Infer intent from physical change alone.

## 9. Narrative Agent

### Purpose
Cluster and compare narratives.

### Must
- Preserve narrative plurality.
- Distinguish source, narrative and confidence.
- Track narrative evolution.

### Must not
- Collapse competing narratives into one “truth” merely because one is more common.

## 10. Data Normalization Agent

### Purpose
Convert inputs into canonical structured Events.

### Must not
- Add new information.
- Perform substantive summarization.

## 11. Knowledge Graph Agent

### Purpose
Create/update entities and relationships.

### Must
- Link graph changes to source Events.
- Preserve temporal context.
- Record confidence/provenance.

## 12. Orchestrator Agent

### Purpose
Route tasks and Events.

### Must
- Determine which agent/workflow should process an Event.
- Prioritize work.
- Track workflow state.

### Must not
- Become a hidden universal analyst.
- Bypass provenance or governance controls.

## 13. Journalist Interface Agent

### Purpose
Turn structured intelligence into readable evidence-backed briefs.

### Must
- Show evidence and uncertainty.
- Preserve source links.
- Distinguish fact from inference.

### Must not
- Manufacture missing evidence.
- hide contradictory evidence.

## 14. Future agents

Potential future components from the Blueprint:
- Political/Behavioral Profile Agent.
- Narrative Recycling Detector.
- Silence Mapping.
- Corrective Memory.
- Autonomous Newsroom.
- Adversarial Narrative Engine.
- Digital Twin Lite.

These remain future scope unless explicitly promoted to an implementation phase.
