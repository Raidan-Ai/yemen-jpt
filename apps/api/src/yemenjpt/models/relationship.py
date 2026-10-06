from __future__ import annotations
import uuid
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base, TimestampMixin

class RelationshipModel(Base, TimestampMixin):
    __tablename__ = "relationships"
    rel_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_entity_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)
    target_entity_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    temporal_context: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    metadata_col: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    created_event_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
