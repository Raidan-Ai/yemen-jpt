"""Journalist Interface Agent — generate briefs."""
from __future__ import annotations
import uuid, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from datetime import datetime, timezone
from yemenjpt_contracts.schemas.events import CanonicalEvent, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus
from .base import BaseAgent

class JournalistInterfaceAgent(BaseAgent):
    agent_id = "journalist_interface_agent"
    purpose = "Generate evidence-backed investigation briefs"
    input_event_types = ["verification.completed", "graph.updated"]
    output_event_types = ["brief.generated"]

    async def process(self, event: CanonicalEvent) -> None:
        from ..ai.factory import get_model_router
        from ..ai.router import Capability
        router = get_model_router()
        p = event.payload
        vr = p.get("verification_results", [])
        prompt = f"Generate evidence-backed investigation brief.\nCase: {event.case_id}\nClaims assessed: {len(vr)}\nEntities: {p.get('total_nodes', 0)}\nRULES: Distinguish FACT/CLAIM/INFERENCE. Mark uncertain items [UNVERIFIED]. Never fabricate.\n\nBrief:"
        brief = await router.generate_text(capability=Capability.SUMMARIZATION, messages=[{"role": "user", "content": prompt}])
        rid = str(uuid.uuid4())
        report = {"report_id": rid, "case_id": event.case_id, "title": f"Brief — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC", "content": brief, "confidence": {"score": 0.3, "label": "low"}, "provenance": [pv.model_dump() for pv in event.provenance], "verification_results": vr, "editorial_note": "AI-assisted. Human review required before publication.", "generated_at": datetime.now(timezone.utc).isoformat()}
        from ..routes.reports import store_report
        store_report(report)
        out = CanonicalEvent(event_type="brief.generated", source=event.source, case_id=event.case_id, correlation_id=event.correlation_id, producer=self.make_producer(), payload={"report_id": rid, "brief_summary": brief[:500], "full_report_available": True}, evidence=event.evidence, provenance=event.provenance, confidence=Confidence(score=0.3, label="low"))
        await get_event_bus().publish(out)
