"""Entities API — /api/v1/entities"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
router = APIRouter(prefix="/entities", tags=["entities"])
_entities: dict[str, dict] = {}
_relationships: list[dict] = []

@router.get("")
async def list_entities(limit: int = 50, offset: int = 0):
    items = list(_entities.values())
    return {"total": len(items), "items": items[offset:offset+limit]}

@router.get("/{entity_id}")
async def get_entity(entity_id: str):
    if entity_id not in _entities:
        raise HTTPException(404, f"Entity {entity_id} not found")
    return _entities[entity_id]

@router.get("/{entity_id}/relationships")
async def get_entity_relationships(entity_id: str):
    if entity_id not in _entities:
        raise HTTPException(404)
    rels = [r for r in _relationships if r["source_entity_id"] == entity_id or r["target_entity_id"] == entity_id]
    return {"entity_id": entity_id, "relationships": rels}

@router.get("/{entity_id}/timeline")
async def get_entity_timeline(entity_id: str):
    if entity_id not in _entities:
        raise HTTPException(404)
    return {"entity_id": entity_id, "events": []}

def store_entity(e: dict) -> None:
    _entities[e["entity_id"]] = e

def store_relationship(r: dict) -> None:
    _relationships.append(r)

def get_all_entities() -> list[dict]:
    return list(_entities.values())
