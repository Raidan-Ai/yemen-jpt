"""Reports API"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router = APIRouter(prefix="/reports", tags=["reports"])
_reports: dict[str, dict] = {}

class ReportCreate(BaseModel):
    case_id: str
    title: str
    content: str
    confidence_score: float = 0.0

@router.post("", status_code=201)
async def create_report(body: ReportCreate):
    rid = str(uuid.uuid4())
    r = {"report_id": rid, "case_id": body.case_id, "title": body.title, "content": body.content, "confidence": {"score": body.confidence_score, "label": "low"}, "generated_at": datetime.now(timezone.utc).isoformat(), "provenance": []}
    _reports[rid] = r
    return r

@router.get("/{report_id}")
async def get_report(report_id: str):
    if report_id not in _reports:
        raise HTTPException(404)
    return _reports[report_id]

@router.get("")
async def list_reports(case_id: str | None = None):
    items = list(_reports.values())
    if case_id:
        items = [r for r in items if r["case_id"] == case_id]
    return {"total": len(items), "items": items}

def store_report(r: dict) -> None:
    _reports[r["report_id"]] = r
