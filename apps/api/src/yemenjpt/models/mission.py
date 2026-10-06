from __future__ import annotations
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class MissionModel(Base):
    __tablename__ = "missions"
    mission_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    objective: Mapped[str] = mapped_column(String(1024), nullable=False)
    case_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", index=True)
    agent_id: Mapped[str] = mapped_column(String(128), nullable=False, default="orchestrator")
    correlation_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, default=lambda: str(uuid.uuid4()))
    parameters: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
