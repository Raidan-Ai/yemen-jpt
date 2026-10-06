"""Missions API"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
router = APIRouter(prefix="/missions", tags=["missions"])
_missions: dict[str, dict] = {}

@router.get("")
async def list_missions(status: str | None = None):
    items = list(_missions.values())
    if status:
        items = [m for m in items if m["status"] == status]
    return {"total": len(items), "items": items}

@router.get("/{mission_id}")
async def get_mission(mission_id: str):
    if mission_id not in _missions:
        raise HTTPException(404)
    return _missions[mission_id]

@router.post("/{mission_id}/cancel")
async def cancel_mission(mission_id: str):
    if mission_id not in _missions:
        raise HTTPException(404)
    _missions[mission_id]["status"] = "cancelled"
    return _missions[mission_id]

def create_mission(objective: str, case_id: str | None = None, params: dict | None = None) -> dict:
    mid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    m = {"mission_id": mid, "objective": objective, "case_id": case_id, "status": "pending", "agent_id": "orchestrator", "correlation_id": str(uuid.uuid4()), "parameters": params or {}, "result": None, "created_at": now}
    _missions[mid] = m
    return m

def update_mission(mid: str, **kw) -> None:
    if mid in _missions:
        _missions[mid].update(kw)
