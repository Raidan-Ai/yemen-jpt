from __future__ import annotations
import uuid
from sqlalchemy import String, Text, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base, TimestampMixin

class ClaimModel(Base, TimestampMixin):
    __tablename__ = "claims"
    claim_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    taxonomy: Mapped[str] = mapped_column(String(32), nullable=False, default="CLAIM", index=True)
    verification_status: Mapped[str] = mapped_column(String(32), nullable=False, default="unverified", index=True)
    entity_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    case_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    supporting_evidence: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    contradicting_evidence: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_event_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
