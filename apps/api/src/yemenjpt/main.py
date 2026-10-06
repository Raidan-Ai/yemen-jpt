"""YemenJPT API — main entry point."""
from __future__ import annotations
import logging, sys, os
from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'packages', 'contracts', 'src'))

from .config.settings import get_settings
from .routes import health, cases, events, entities, research, missions, reports, graph
from .exceptions.exceptions import api_exception_handler

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    s = get_settings()
    logging.basicConfig(level=getattr(logging, s.LOG_LEVEL, logging.INFO))
    logger.info("Starting YemenJPT API v%s", s.APP_VERSION)
    from yemenjpt_contracts.services.event_bus import get_event_bus
    bus = get_event_bus()
    await bus.start()
    from .agents import register_all_handlers
    register_all_handlers(bus)
    yield
    await bus.stop()
    logger.info("YemenJPT API shutdown")

def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.APP_NAME, version=s.APP_VERSION, description="YemenJPT Sovereign Intelligence Platform", docs_url="/docs", redoc_url="/redoc", openapi_url="/api/v1/openapi.json", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=s.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(health.router)
    for r in [cases, events, entities, research, missions, reports, graph]:
        app.include_router(r.router, prefix="/api/v1")
    app.add_exception_handler(Exception, api_exception_handler)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    s = get_settings()
    uvicorn.run("yemenjpt.main:app", host=s.APP_HOST, port=s.APP_PORT, reload=True)
