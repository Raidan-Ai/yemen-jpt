from __future__ import annotations
from fastapi import Request
from fastapi.responses import JSONResponse
import logging
logger = logging.getLogger(__name__)

async def api_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception at %s", request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
