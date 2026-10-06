from fastapi import APIRouter

router = APIRouter(prefix="/intelligence", tags=["intelligence"])

@router.get("/status")
async def intelligence_status():
    return {"status": "not_implemented", "note": "Intelligence endpoints will be added in subsequent phases."}
