"""Ingestion Agent — preserve source, emit Events."""
from __future__ import annotations
import hashlib, uuid, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from datetime import datetime, timezone
from yemenjpt_contracts.schemas.events import CanonicalEvent, SourceRef, Confidence, EvidenceRef, EvidenceType, SourceType
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

class IngestionAgent(BaseAgent):
    agent_id = "ingestion_agent"
    purpose = "Collect raw source material and emit Events"
    input_event_types = ["source.submit", "url.submit", "document.submit"]
    output_event_types = ["source.ingested"]

    async def process(self, event: CanonicalEvent) -> None:
        p = event.payload
        raw = p.get("content", "")
        url = p.get("url", "")
        sid = p.get("source_id", str(uuid.uuid4()))
        h = hashlib.sha256(raw.encode()).hexdigest() if raw else None
        ev = EvidenceRef(type=EvidenceType.DOCUMENT, source_id=sid, locator=url or None, captured_at=datetime.now(timezone.utc), content_hash=h, excerpt=raw[:500] if raw else None)
        out = CanonicalEvent(event_type="source.ingested", source=SourceRef(source_id=sid, source_type=SourceType.MEDIA, uri=url or None), case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={"source_id": sid, "url": url, "language": p.get("language", "ar"), "content_length": len(raw), "content_hash": h, "raw_content": raw, "title": p.get("title", ""), "acquired_at": datetime.now(timezone.utc).isoformat()}, evidence=[ev], confidence=Confidence(score=0.5, label="medium"))
        await get_event_bus().publish(out)
