"""Persistent records for the governed Commercial Intelligence graph."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.utils import utcnow
from db.models import Base


class CommercialSourceRecord(Base):
    __tablename__ = "commercial_intelligence_sources"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255))
    kind: Mapped[str] = mapped_column(String(32), index=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    policy_status: Mapped[str] = mapped_column(String(32), index=True)
    allowed_use: Mapped[str] = mapped_column(String(255))
    authority_score: Mapped[int] = mapped_column(Integer, default=50)
    verifiability_score: Mapped[int] = mapped_column(Integer, default=50)
    freshness_days: Mapped[int] = mapped_column(Integer, default=30)
    retention_days: Mapped[int] = mapped_column(Integer, default=365)
    terms_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_commercial_intel_source_name"),
    )


class CommercialSignalRecord(Base):
    __tablename__ = "commercial_intelligence_signals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    account_id: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(
        ForeignKey("commercial_intelligence_sources.id", ondelete="RESTRICT"),
        index=True,
    )
    signal_type: Mapped[str] = mapped_column(String(64), index=True)
    claim: Mapped[str] = mapped_column(Text)
    evidence_ref: Mapped[str] = mapped_column(String(1000))
    evidence_level: Mapped[str] = mapped_column(String(32), index=True)
    confidence: Mapped[int] = mapped_column(Integer)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "account_id", "source_id", "evidence_ref",
            name="uq_commercial_intel_signal_evidence",
        ),
        Index(
            "ix_commercial_intel_signal_account_active",
            "tenant_id", "account_id", "status", "observed_at",
        ),
    )


class DepartmentObjectiveRecord(Base):
    __tablename__ = "commercial_department_objectives"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    department: Mapped[str] = mapped_column(String(64), index=True)
    objective: Mapped[str] = mapped_column(Text)
    metric: Mapped[str] = mapped_column(String(128))
    target_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    horizon: Mapped[str] = mapped_column(String(32), default="quarter")
    priority: Mapped[int] = mapped_column(Integer, default=50, index=True)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    evidence_required: Mapped[str] = mapped_column(
        String(32), default="l3_first_party"
    )
    owner_role: Mapped[str] = mapped_column(String(64), default="department_owner")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "department", "metric",
            name="uq_commercial_department_objective_metric",
        ),
    )


class StrategicRelationshipRecord(Base):
    __tablename__ = "commercial_strategic_relationships"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    account_id: Mapped[str] = mapped_column(String(64), index=True)
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    relationship_type: Mapped[str] = mapped_column(String(64), index=True)
    stage: Mapped[str] = mapped_column(String(32), default="research", index=True)
    permission_state: Mapped[str] = mapped_column(String(32), default="research_only")
    mutual_value: Mapped[str] = mapped_column(Text)
    relationship_strength: Mapped[int] = mapped_column(Integer, default=0, index=True)
    owner_role: Mapped[str] = mapped_column(String(64), default="partnerships")
    evidence_refs_json: Mapped[list] = mapped_column(JSON, default=list)
    last_interaction_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    next_review_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "account_id", "relationship_type",
            name="uq_commercial_strategic_relationship",
        ),
    )


class CommercialOpportunityRecord(Base):
    __tablename__ = "commercial_intelligence_opportunities"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    account_id: Mapped[str] = mapped_column(String(64), index=True)
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    title: Mapped[str] = mapped_column(String(255))
    department_objective_id: Mapped[str] = mapped_column(
        ForeignKey("commercial_department_objectives.id", ondelete="RESTRICT"),
        index=True,
    )
    relationship_id: Mapped[str | None] = mapped_column(
        ForeignKey("commercial_strategic_relationships.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    offer_id: Mapped[str] = mapped_column(String(64), index=True)
    stage: Mapped[str] = mapped_column(String(32), default="research", index=True)
    evidence_level: Mapped[str] = mapped_column(String(32), index=True)
    source_signal_ids_json: Mapped[list] = mapped_column(JSON, default=list)
    score_components_json: Mapped[dict] = mapped_column(JSON, default=dict)
    score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    confidence_band: Mapped[str] = mapped_column(String(16), default="low", index=True)
    blockers_json: Mapped[list] = mapped_column(JSON, default=list)
    next_action: Mapped[str] = mapped_column(Text)
    proof_target: Mapped[str] = mapped_column(Text)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    external_action_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "account_id", "department_objective_id", "offer_id",
            name="uq_commercial_intel_opportunity",
        ),
        Index(
            "ix_commercial_intel_opportunity_queue",
            "tenant_id", "status", "stage", "score",
        ),
    )


class CommercialOpportunitySignalRecord(Base):
    """A real, queryable evidence edge between an opportunity and a signal."""

    __tablename__ = "commercial_opportunity_signals"

    opportunity_id: Mapped[str] = mapped_column(
        ForeignKey("commercial_intelligence_opportunities.id", ondelete="CASCADE"),
        primary_key=True,
    )
    signal_id: Mapped[str] = mapped_column(
        ForeignKey("commercial_intelligence_signals.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    __table_args__ = (
        Index(
            "ix_commercial_opportunity_signal_tenant_opportunity",
            "tenant_id",
            "opportunity_id",
        ),
    )


__all__ = [
    "CommercialOpportunityRecord",
    "CommercialOpportunitySignalRecord",
    "CommercialSignalRecord",
    "CommercialSourceRecord",
    "DepartmentObjectiveRecord",
    "StrategicRelationshipRecord",
]
