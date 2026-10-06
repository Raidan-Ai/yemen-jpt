"""Events API — /api/v1/events"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/events", tags=["events"])
_events: dict[str, dict] = {}

class EventCreate(BaseModel):
    event_type: str
    source_id: str
    case_id: str | None = None
    payload: dict[str, Any] = {}
    classification: str = "internal"

@router.get("/{event_id}")
async def get_event(event_id: str):
    if event_id not in _events:
        raise HTTPException(404, f"Event {event_id} not found")
    return _events[event_id]

@router.post("", status_code=201)
async def create_event(body: EventCreate):
    eid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    event = {"event_id": eid, "event_type": body.event_type, "event_version": "1.0", "occurred_at": now, "ingested_at": now, "source": {"source_id": body.source_id}, "case_id": body.case_id, "correlation_id": str(uuid.uuid4()), "producer": {"agent_id": "api", "agent_version": "1.0"}, "payload": body.payload, "evidence": [], "confidence": {"score": 0.0, "label": "unknown"}, "classification": body.classification, "metadata": {}}
    _events[eid] = event
    return event

def store_event(event_dict: dict) -> None:
    _events[event_dict["event_id"]] = event_dict
