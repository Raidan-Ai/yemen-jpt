"""Cases API — /api/v1/cases"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/cases", tags=["cases"])
_cases: dict[str, dict] = {}
_events_by_case: dict[str, list] = {}
_entities_by_case: dict[str, list] = {}

class CaseCreate(BaseModel):
    title: str
    description: str | None = None
    research_question: str | None = None

class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    research_question: str | None = None

@router.get("")
async def list_cases(status: str | None = None, limit: int = 50, offset: int = 0):
    items = list(_cases.values())
    if status:
        items = [c for c in items if c["status"] == status]
    return {"total": len(items), "items": items[offset:offset+limit]}

@router.post("", status_code=201)
async def create_case(body: CaseCreate):
    cid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    case = {"case_id": cid, "title": body.title, "description": body.description, "research_question": body.research_question, "status": "active", "created_at": now, "updated_at": now}
    _cases[cid] = case
    _events_by_case[cid] = []
    _entities_by_case[cid] = []
    return case

@router.get("/{case_id}")
async def get_case(case_id: str):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    return _cases[case_id]

@router.patch("/{case_id}")
async def update_case(case_id: str, body: CaseUpdate):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    _cases[case_id].update({k: v for k, v in body.model_dump().items() if v is not None})
    _cases[case_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    return _cases[case_id]

@router.get("/{case_id}/timeline")
async def case_timeline(case_id: str):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    return {"case_id": case_id, "events": sorted(_events_by_case.get(case_id, []), key=lambda e: e.get("occurred_at", ""))}

@router.get("/{case_id}/entities")
async def case_entities(case_id: str):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    return {"case_id": case_id, "entities": _entities_by_case.get(case_id, [])}

@router.get("/{case_id}/evidence")
async def case_evidence(case_id: str):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    evidence = [e for evt in _events_by_case.get(case_id, []) for e in evt.get("evidence", [])]
    return {"case_id": case_id, "evidence": evidence}

@router.get("/{case_id}/events")
async def case_events(case_id: str):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    return {"case_id": case_id, "events": _events_by_case.get(case_id, [])}

@router.get("/{case_id}/narratives")
async def case_narratives(case_id: str):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    return {"case_id": case_id, "narratives": []}

@router.get("/{case_id}/signals")
async def case_signals(case_id: str):
    if case_id not in _cases:
        raise HTTPException(404, f"Case {case_id} not found")
    return {"case_id": case_id, "signals": []}

def add_event_to_case(case_id: str, event_dict: dict) -> None:
    if case_id in _events_by_case:
        _events_by_case[case_id].append(event_dict)

def add_entity_to_case(case_id: str, entity_dict: dict) -> None:
    if case_id in _entities_by_case:
        _entities_by_case[case_id].append(entity_dict)
