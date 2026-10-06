"""Research API"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
router = APIRouter(tags=["research"])

class ResearchRequest(BaseModel):
    question: str
    case_id: str | None = None
    sources: list[str] = []

class FactCheckRequest(BaseModel):
    claim: str
    case_id: str | None = None

class OsintSearchRequest(BaseModel):
    query: str
    case_id: str | None = None

@router.post("/research")
async def submit_research(body: ResearchRequest, bg: BackgroundTasks):
    mid = str(uuid.uuid4())
    bg.add_task(_run, mid, body.model_dump(), "research")
    return {"mission_id": mid, "status": "pending", "created_at": datetime.now(timezone.utc).isoformat()}

@router.post("/fact-check")
async def submit_fact_check(body: FactCheckRequest, bg: BackgroundTasks):
    mid = str(uuid.uuid4())
    bg.add_task(_run, mid, body.model_dump(), "fact_check")
    return {"mission_id": mid, "status": "pending"}

@router.post("/osint/search")
async def submit_osint(body: OsintSearchRequest, bg: BackgroundTasks):
    mid = str(uuid.uuid4())
    bg.add_task(_run, mid, body.model_dump(), "osint")
    return {"mission_id": mid, "status": "pending"}

async def _run(mid: str, params: dict, ptype: str) -> None:
    from ..services.pipeline import run_full_pipeline
    await run_full_pipeline(mission_id=mid, params=params, pipeline_type=ptype)
