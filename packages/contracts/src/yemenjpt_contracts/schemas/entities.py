"""Entity schemas — 03_EVENT_AND_DATA_CONTRACTS.md §5"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field
from .events import Confidence, ProvenanceEntry, VerificationStatus, FactTaxonomy, EntityType, RelationshipType, EvidenceRef

class BaseEntity(BaseModel):
    entity_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: EntityType
    name: str
    aliases: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: Confidence = Field(default_factory=Confidence)
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    properties: dict[str, Any] = Field(default_factory=dict)
    case_id: str | None = None

class PersonEntity(BaseEntity):
    type: EntityType = EntityType.PERSON
    role: str | None = None
    affiliation: str | None = None
    nationality: str | None = None

class OrganizationEntity(BaseEntity):
    type: EntityType = EntityType.ORGANIZATION
    org_type: str | None = None
    country: str | None = None

class LocationEntity(BaseEntity):
    type: EntityType = EntityType.LOCATION
    lat: float | None = None
    lon: float | None = None
    admin_level: str | None = None
    country: str = "YE"

class Relationship(BaseModel):
    rel_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_entity_id: str
    target_entity_id: str
    type: RelationshipType
    confidence: Confidence = Field(default_factory=Confidence)
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    temporal_context: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Claim(BaseModel):
    claim_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    taxonomy: FactTaxonomy = FactTaxonomy.CLAIM
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    entity_id: str | None = None
    case_id: str | None = None
    confidence: Confidence = Field(default_factory=Confidence)
    supporting_evidence: list[EvidenceRef] = Field(default_factory=list)
    contradicting_evidence: list[EvidenceRef] = Field(default_factory=list)
    reasoning: str | None = None
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class VerificationResult(BaseModel):
    claim: str
    status: VerificationStatus
    supporting_evidence: list[EvidenceRef] = Field(default_factory=list)
    contradicting_evidence: list[EvidenceRef] = Field(default_factory=list)
    confidence: Confidence = Field(default_factory=Confidence)
    reasoning_summary: str = ""
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    verified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Narrative(BaseModel):
    narrative_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str | None = None
    sources: list[str] = Field(default_factory=list)
    confidence: Confidence = Field(default_factory=Confidence)
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    case_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Signal(BaseModel):
    signal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    description: str
    risk_score: float = Field(ge=0.0, le=1.0, default=0.0)
    confidence: Confidence = Field(default_factory=Confidence)
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    case_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Case(BaseModel):
    case_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str | None = None
    status: str = "active"
    research_question: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str | None = None

class Mission(BaseModel):
    mission_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    objective: str
    case_id: str | None = None
    status: str = "pending"
    agent_id: str = "orchestrator"
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parameters: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] | None = None
    error_message: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    completed_at: datetime | None = None

class Report(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    case_id: str
    title: str
    content: str
    confidence: Confidence = Field(default_factory=Confidence)
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

Entity = BaseEntity
Source = BaseEntity
Actor = PersonEntity
