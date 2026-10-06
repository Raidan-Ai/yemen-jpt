"""Verification Agent — true/false/mixed/unknown."""
from __future__ import annotations
import uuid, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from yemenjpt_contracts.schemas.events import CanonicalEvent, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

class VerificationAgent(BaseAgent):
    agent_id = "verification_agent"
    purpose = "Cross-source claim verification"
    input_event_types = ["nlp.extracted"]
    output_event_types = ["verification.completed"]

    async def process(self, event: CanonicalEvent) -> None:
        p = event.payload
        claims = p.get("claims", [])
        from ..ai.factory import get_model_router
        router = get_model_router()
        results = []
        for claim in claims:
            text = claim.get("text", "")
            r = await router.extract_structured(prompt=f"Verify claim: {text}\nEvidence: {str(event.evidence)[:500]}\nJSON: {{status,reasoning,confidence}}", schema_description="Verification result")
            results.append({"claim_id": claim.get("claim_id", str(uuid.uuid4())), "claim_text": text, "status": r.get("status", "unknown"), "reasoning": r.get("reasoning", "Insufficient evidence"), "confidence": r.get("confidence", 0.1), "supporting_evidence": [], "contradicting_evidence": [], "_synthetic": r.get("_synthetic", False)})
        out = CanonicalEvent(event_type="verification.completed", source=event.source, case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={"source_id": p.get("source_id"), "claims_verified": len(results), "verification_results": results, "verification_note": "Single-source. Human review required."}, evidence=event.evidence, provenance=event.provenance, confidence=Confidence(score=0.3, label="low"))
        await get_event_bus().publish(out)
