"""NLP Intelligence Agent — extract entities, claims, relationships."""
from __future__ import annotations
import uuid, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from yemenjpt_contracts.schemas.events import CanonicalEvent, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

class NlpIntelligenceAgent(BaseAgent):
    agent_id = "nlp_intelligence_agent"
    purpose = "Extract entities, claims via NLP"
    input_event_types = ["news.processed", "source.normalized"]
    output_event_types = ["nlp.extracted"]

    async def process(self, event: CanonicalEvent) -> None:
        p = event.payload
        content = p.get("content", p.get("normalized_content", ""))
        from ..ai.factory import get_model_router
        router = get_model_router()
        structured = await router.extract_structured(prompt=f"Extract entities, claims, relationships:\n\n{content[:3000]}", schema_description="JSON: entities [{name,type,confidence}], claims [{text,taxonomy,confidence}], relationships [{source,target,type}]")
        entities = structured.get("entities", [])
        claims = structured.get("claims", [])
        for e in entities:
            e["entity_id"] = str(uuid.uuid4())
            e["case_id"] = event.case_id
        for c in claims:
            c["claim_id"] = str(uuid.uuid4())
            c["case_id"] = event.case_id
            c["verification_status"] = "unverified"
            c["taxonomy"] = c.get("taxonomy", "CLAIM")
        out = CanonicalEvent(event_type="nlp.extracted", source=event.source, case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={"source_id": p.get("source_id"), "entities": entities, "claims": claims, "relationships": structured.get("relationships", []), "extraction_note": "NLP interpretation, NOT verification.", "_synthetic": structured.get("_synthetic", False)}, evidence=event.evidence, provenance=event.provenance, confidence=Confidence(score=0.4, label="low"))
        await get_event_bus().publish(out)
