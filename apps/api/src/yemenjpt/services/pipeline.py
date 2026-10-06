"""Full pipeline: source.submit -> Ingestion -> Normalization -> News -> NLP -> Verification -> KG -> Brief"""
from __future__ import annotations
import asyncio, logging, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from datetime import datetime, timezone
from yemenjpt_contracts.schemas.events import CanonicalEvent, SourceRef, Producer, Confidence
from yemenjpt_contracts.services.event_bus import get_event_bus

logger = logging.getLogger(__name__)

async def run_full_pipeline(mission_id: str, params: dict, pipeline_type: str = "research") -> None:
    bus = get_event_bus()
    case_id = params.get("case_id")
    question = params.get("question") or params.get("claim") or params.get("query", "")
    sources = params.get("sources", [])
    logger.info("Pipeline %s: mission=%s case=%s", pipeline_type, mission_id, case_id)
    initial = CanonicalEvent(event_type="source.submit", source=SourceRef(source_id="pipeline", source_type="api"), producer=Producer(agent_id="orchestrator"), case_id=case_id, payload={"mission_id": mission_id, "pipeline_type": pipeline_type, "question": question, "content": question, "url": sources[0] if sources else "", "source_id": f"mission_{mission_id}", "language": "ar", "title": f"Mission: {question[:100]}"}, confidence=Confidence(score=0.5, label="medium"))
    await bus.publish(initial)
    await asyncio.sleep(0.1)
    try:
        await asyncio.wait_for(bus._queue.join(), timeout=30.0)
    except asyncio.TimeoutError:
        logger.warning("Pipeline %s timed out", mission_id)
    logger.info("Pipeline %s complete", pipeline_id if False else mission_id)
