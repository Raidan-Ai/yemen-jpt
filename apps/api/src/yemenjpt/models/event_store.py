from __future__ import annotations
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class EventStore(Base):
    __tablename__ = "events"
    event_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    event_version: Mapped[str] = mapped_column(String(16), nullable=False, default="1.0")
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    source_agent_id: Mapped[str] = mapped_column(String(128), nullable=False)
    case_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    correlation_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, default=lambda: str(uuid.uuid4()), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    evidence: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    confidence_label: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    processing_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", index=True)
    dead_letter_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (Index("ix_events_case_type", "case_id", "event_type"),)
