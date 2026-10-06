"""News Intelligence Agent — extract article metadata."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from yemenjpt_contracts.schemas.events import CanonicalEvent, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

class NewsIntelligenceAgent(BaseAgent):
    agent_id = "news_intelligence_agent"
    purpose = "Extract structured intelligence from news"
    input_event_types = ["source.normalized", "osint.collected"]
    output_event_types = ["news.processed"]

    async def process(self, event: CanonicalEvent) -> None:
        p = event.payload
        content = p.get("normalized_content", p.get("raw_content", ""))
        out = CanonicalEvent(event_type="news.processed", source=event.source, case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={"source_id": p.get("source_id"), "language": p.get("detected_language", "ar"), "article_metadata": {"title": p.get("title", ""), "url": p.get("url", ""), "word_count": len(content.split())}, "credibility_signals": {"has_url": bool(p.get("url")), "note": "Multi-source verification required"}, "content": content, "ready_for_nlp": True}, evidence=event.evidence, provenance=event.provenance, confidence=Confidence(score=0.4, label="low"))
        await get_event_bus().publish(out)
