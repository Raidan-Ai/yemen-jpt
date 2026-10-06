"""SQLAlchemy 2.x async declarative base and session factory."""
from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from ..config.settings import get_settings

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Base(DeclarativeBase):
    pass

_engine = None
_sf = None

def get_engine():
    global _engine
    if _engine is None:
        s = get_settings()
        _engine = create_async_engine(s.DATABASE_URL, pool_size=s.DB_POOL_SIZE, max_overflow=s.DB_MAX_OVERFLOW, echo=s.DEBUG, future=True)
    return _engine

def get_session_factory():
    global _sf
    if _sf is None:
        _sf = async_sessionmaker(get_engine(), expire_on_commit=False, class_=AsyncSession)
    return _sf

async def get_db_session():
    async with get_session_factory()() as session:
        yield session
