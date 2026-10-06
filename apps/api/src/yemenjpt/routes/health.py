from __future__ import annotations
from datetime import datetime, timezone
from fastapi import APIRouter
router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok", "service": "yemenjpt-api", "timestamp": datetime.now(timezone.utc).isoformat()}

@router.get("/health/readiness")
async def readiness():
    return {"status": "ready"}
