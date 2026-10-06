from __future__ import annotations
import uuid
from sqlalchemy import String, Float, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base, TimestampMixin

class EntityModel(Base, TimestampMixin):
    __tablename__ = "entities"
    entity_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    aliases: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    properties: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    case_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    created_event_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    __table_args__ = (Index("ix_entities_case_type", "case_id", "type"),)
