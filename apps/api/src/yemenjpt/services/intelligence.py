"""Intelligence service stub for future model integration."""

from typing import Any


class IntelligenceService:
    """Stub intelligence service — will be wired to LLM provider in later phases."""

    async def analyze(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"status": "not_implemented", "payload": payload}


intelligence_service = IntelligenceService()