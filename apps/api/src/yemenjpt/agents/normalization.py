"""Normalization Agent — clean text, detect language."""
from __future__ import annotations
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from datetime import datetime, timezone
from yemenjpt_contracts.schemas.events import CanonicalEvent, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

class NormalizationAgent(BaseAgent):
    agent_id = "normalization_agent"
    purpose = "Normalize ingested content"
    input_event_types = ["source.ingested"]
    output_event_types = ["source.normalized"]

    async def process(self, event: CanonicalEvent) -> None:
        p = event.payload
        raw = p.get("raw_content", "")
        norm = re.sub(r'\s+', ' ', raw.replace('\x00', '')).strip()
        arabic = sum(1 for c in norm if '\u0600' <= c <= '\u06ff')
        lang = "ar" if norm and arabic / max(len(norm), 1) > 0.3 else "en"
        out = CanonicalEvent(event_type="source.normalized", source=event.source, case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={**p, "normalized_content": norm, "detected_language": lang, "normalized_timestamp": datetime.now(timezone.utc).isoformat()}, evidence=event.evidence, provenance=event.provenance, confidence=event.confidence, classification=event.classification)
        await get_event_bus().publish(out)
