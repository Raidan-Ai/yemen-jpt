"""OSINT Agent — structure public signals."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from yemenjpt_contracts.schemas.events import CanonicalEvent, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

class OsintAgent(BaseAgent):
    agent_id = "osint_agent"
    purpose = "Collect open-source intelligence"
    input_event_types = ["osint.search", "source.normalized"]
    output_event_types = ["osint.collected"]

    async def process(self, event: CanonicalEvent) -> None:
        p = event.payload
        q = p.get("query") or p.get("normalized_content", "")[:200]
        findings = []
        if p.get("url"):
            findings.append({"type": "url_reference", "value": p["url"], "confidence": 0.7})
        if q:
            findings.append({"type": "content_signal", "value": q[:200], "confidence": 0.3})
        out = CanonicalEvent(event_type="osint.collected", source=event.source, case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={"query": q, "findings": findings, "collection_note": "MVP: structured from ingested content."}, evidence=event.evidence, provenance=event.provenance, confidence=Confidence(score=0.3, label="low"))
        await get_event_bus().publish(out)
