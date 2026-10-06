"""Graph API"""
from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("")
async def get_graph():
    from ..agents.knowledge_graph import get_graph_state
    return get_graph_state()
