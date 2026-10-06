"""Canonical Event envelope — 03_EVENT_AND_DATA_CONTRACTS.md §1"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, field_validator


class EventClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"

class ConfidenceLabel(str, Enum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class FactTaxonomy(str, Enum):
    FACT = "FACT"
    CLAIM = "CLAIM"
    INTERPRETATION = "INTERPRETATION"
    INFERENCE = "INFERENCE"
    PREDICTION = "PREDICTION"

class VerificationStatus(str, Enum):
    TRUE = "true"
    FALSE = "false"
    MIXED = "mixed"
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"

class SourceType(str, Enum):
    OFFICIAL = "official"
    MEDIA = "media"
    SOCIAL = "social"
    SATELLITE = "satellite"
    DOCUMENT = "document"
    API = "api"
    OTHER = "other"

class EvidenceType(str, Enum):
    DOCUMENT = "document"
    QUOTE = "quote"
    IMAGE = "image"
    VIDEO = "video"
    DATASET = "dataset"
    OBSERVATION = "observation"
    EVENT = "event"

class EntityType(str, Enum):
    PERSON = "Person"
    ORGANIZATION = "Organization"
    LOCATION = "Location"
    EVENT = "Event"
    DOCUMENT = "Document"
    NEWS_ITEM = "NewsItem"
    CLAIM = "Claim"
    STATEMENT = "Statement"
    SOURCE = "Source"
    NARRATIVE = "Narrative"
    SIGNAL = "Signal"
    CASE = "Case"

class RelationshipType(str, Enum):
    PARTICIPATED_IN = "PARTICIPATED_IN"
    LOCATED_IN = "LOCATED_IN"
    AFFILIATED_WITH = "AFFILIATED_WITH"
    SAID = "SAID"
    REPORTED = "REPORTED"
    RELATED_TO = "RELATED_TO"
    CONTRADICTS = "CONTRADICTS"
    SUPPORTS = "SUPPORTS"
    OCCURRED_BEFORE = "OCCURRED_BEFORE"
    FOLLOWED_BY = "FOLLOWED_BY"

class Confidence(BaseModel):
    score: float = Field(ge=0.0, le=1.0, default=0.0)
    label: ConfidenceLabel = ConfidenceLabel.UNKNOWN
    rationale: str | None = None

class SourceRef(BaseModel):
    source_id: str
    source_type: SourceType = SourceType.OTHER
    uri: str | None = None
    name: str | None = None
    classification: EventClassification = EventClassification.PUBLIC

class Producer(BaseModel):
    agent_id: str
    agent_version: str = "1.0"

class EvidenceRef(BaseModel):
    evidence_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: EvidenceType = EvidenceType.DOCUMENT
    source_id: str
    locator: str | None = None
    captured_at: datetime | None = None
    content_hash: str | None = None
    excerpt: str | None = None

class ProvenanceEntry(BaseModel):
    event_id: str
    agent_id: str
    agent_version: str = "1.0"
    transformation: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    evidence_ids: list[str] = Field(default_factory=list)

class CanonicalEvent(BaseModel):
    """The canonical Event envelope for all inter-agent communication."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    event_version: str = "1.0"
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: SourceRef
    case_id: str | None = None
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    producer: Producer
    payload: dict[str, Any] = Field(default_factory=dict)
    evidence: list[EvidenceRef] = Field(default_factory=list)
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    confidence: Confidence = Field(default_factory=Confidence)
    classification: EventClassification = EventClassification.INTERNAL
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("event_type")
    @classmethod
    def event_type_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("event_type must not be empty")
        return v

BaseEvent = CanonicalEvent
IntelligenceEvent = CanonicalEvent
