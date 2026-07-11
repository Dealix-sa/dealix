"""Tenant-isolated persistence models for Dealix's Commercial Universe.

These tables connect existing canonical accounts, contacts, conversations,
meetings, approvals, and deals. They do not duplicate those entities.
"""

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


class CommercialObjectiveRecord(Base):
    """One measurable commercial objective owned by a tenant department."""

    __tablename__ = "commercial_objectives"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    department: Mapped[str] = mapped_column(String(32), index=True)
    objective_type: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    success_metric: Mapped[str] = mapped_column(String(500))
    priority: Mapped[int] = mapped_column(Integer, default=50)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    policy: Mapped[dict] = mapped_column(JSON, default=dict)
    owner_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        Index("ix_commercial_objectives_tenant_department", "tenant_id", "department", "status"),
    )


class TenantAccountRelationshipRecord(Base):
    """Tenant-specific commercial meaning attached to a canonical global account."""

    __tablename__ = "tenant_account_relationships"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), index=True)
    contact_id: Mapped[str | None] = mapped_column(ForeignKey("contacts.id"), nullable=True, index=True)
    objective_id: Mapped[str] = mapped_column(
        ForeignKey("commercial_objectives.id", ondelete="CASCADE"), index=True
    )
    department: Mapped[str] = mapped_column(String(32), index=True)
    relationship_type: Mapped[str] = mapped_column(String(48), index=True)
    lifecycle_stage: Mapped[str] = mapped_column(String(32), default="research", index=True)
    permission_status: Mapped[str] = mapped_column(String(32), default="research_only", index=True)
    allowed_use: Mapped[str] = mapped_column(
        String(128), default="business_contact_research_only"
    )
    source_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)
    strategic_fit_score: Mapped[int] = mapped_column(Integer, default=50)
    trust_score: Mapped[int] = mapped_column(Integer, default=50)
    urgency_score: Mapped[int] = mapped_column(Integer, default=50)
    value_exchange: Mapped[dict] = mapped_column(JSON, default=dict)
    offer_match: Mapped[dict] = mapped_column(JSON, default=dict)
    known_needs: Mapped[list] = mapped_column(JSON, default=list)
    known_capabilities: Mapped[list] = mapped_column(JSON, default=list)
    constraints: Mapped[list] = mapped_column(JSON, default=list)
    evidence_refs: Mapped[list] = mapped_column(JSON, default=list)
    next_action: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "account_id",
            "objective_id",
            "relationship_type",
            name="uq_tenant_account_objective_relationship",
        ),
        Index(
            "ix_tenant_relationship_department_stage",
            "tenant_id",
            "department",
            "lifecycle_stage",
        ),
        Index(
            "ix_tenant_relationship_permission",
            "tenant_id",
            "permission_status",
            "status",
        ),
    )


class StrategicOpportunityRecord(Base):
    """One sales, partnership, marketing, exchange, or expansion opportunity."""

    __tablename__ = "strategic_opportunities"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    relationship_id: Mapped[str] = mapped_column(
        ForeignKey("tenant_account_relationships.id", ondelete="CASCADE"), index=True
    )
    objective_id: Mapped[str] = mapped_column(ForeignKey("commercial_objectives.id"), index=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), index=True)
    department: Mapped[str] = mapped_column(String(32), index=True)
    opportunity_type: Mapped[str] = mapped_column(String(32), index=True)
    relationship_type: Mapped[str] = mapped_column(String(48), index=True)
    title: Mapped[str] = mapped_column(String(255))
    counterparty_need: Mapped[list] = mapped_column(JSON, default=list)
    tenant_need: Mapped[list] = mapped_column(JSON, default=list)
    value_offered: Mapped[list] = mapped_column(JSON, default=list)
    value_requested: Mapped[list] = mapped_column(JSON, default=list)
    offer_type: Mapped[str] = mapped_column(String(48), index=True)
    proposed_scope: Mapped[list] = mapped_column(JSON, default=list)
    draft_terms: Mapped[dict] = mapped_column(JSON, default=dict)
    objections: Mapped[list] = mapped_column(JSON, default=list)
    concessions: Mapped[list] = mapped_column(JSON, default=list)
    red_lines: Mapped[list] = mapped_column(JSON, default=list)
    negotiation_posture: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_move: Mapped[str | None] = mapped_column(String(500), nullable=True)
    proof_requirements: Mapped[list] = mapped_column(JSON, default=list)
    evidence_refs: Mapped[list] = mapped_column(JSON, default=list)
    estimated_value_sar: Mapped[float | None] = mapped_column(Float, nullable=True)
    probability: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    owner_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    approval_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        Index("ix_strategic_opportunities_tenant_status", "tenant_id", "status"),
        Index(
            "ix_strategic_opportunities_department_type",
            "tenant_id",
            "department",
            "opportunity_type",
        ),
    )


class CommercialActionEnvelopeRecord(Base):
    """Persistent internal/approval action card; never a live sender."""

    __tablename__ = "commercial_action_envelopes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    department: Mapped[str] = mapped_column(String(32), index=True)
    relationship_id: Mapped[str] = mapped_column(
        ForeignKey("tenant_account_relationships.id", ondelete="CASCADE"), index=True
    )
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), index=True)
    contact_id: Mapped[str | None] = mapped_column(ForeignKey("contacts.id"), nullable=True, index=True)
    opportunity_id: Mapped[str | None] = mapped_column(
        ForeignKey("strategic_opportunities.id"), nullable=True, index=True
    )
    meeting_plan_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    action_type: Mapped[str] = mapped_column(String(64), index=True)
    action_mode: Mapped[str] = mapped_column(String(32), index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)
    summary_ar: Mapped[str] = mapped_column(Text)
    rationale: Mapped[str] = mapped_column(Text)
    draft_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    evidence_refs: Mapped[list] = mapped_column(JSON, default=list)
    risk_level: Mapped[str] = mapped_column(String(16), default="low", index=True)
    proof_target: Mapped[str] = mapped_column(String(255))
    approval_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    external_action_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_commercial_actions_tenant_status", "tenant_id", "status", "due_at"),
        Index(
            "ix_commercial_actions_department_mode",
            "tenant_id",
            "department",
            "action_mode",
        ),
    )


class CommercialMeetingPlanRecord(Base):
    """Meeting intelligence linked to the existing canonical MeetingRecord."""

    __tablename__ = "commercial_meeting_plans"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    relationship_id: Mapped[str] = mapped_column(
        ForeignKey("tenant_account_relationships.id", ondelete="CASCADE"), index=True
    )
    opportunity_id: Mapped[str | None] = mapped_column(
        ForeignKey("strategic_opportunities.id"), nullable=True, index=True
    )
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), index=True)
    meeting_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    department: Mapped[str] = mapped_column(String(32), index=True)
    objective: Mapped[str] = mapped_column(Text)
    agenda: Mapped[list] = mapped_column(JSON, default=list)
    participants: Mapped[list] = mapped_column(JSON, default=list)
    discovery_questions: Mapped[list] = mapped_column(JSON, default=list)
    negotiation_plan: Mapped[list] = mapped_column(JSON, default=list)
    required_evidence: Mapped[list] = mapped_column(JSON, default=list)
    proposed_slots: Mapped[list] = mapped_column(JSON, default=list)
    booking_requires_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    approval_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_commercial_meetings_tenant_status", "tenant_id", "status"),
    )


class CommercialInteractionMemoryRecord(Base):
    """Structured memory over existing conversations/meetings, without raw duplication."""

    __tablename__ = "commercial_interaction_memory"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    relationship_id: Mapped[str] = mapped_column(
        ForeignKey("tenant_account_relationships.id", ondelete="CASCADE"), index=True
    )
    opportunity_id: Mapped[str | None] = mapped_column(
        ForeignKey("strategic_opportunities.id"), nullable=True, index=True
    )
    conversation_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    meeting_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    department: Mapped[str] = mapped_column(String(32), index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)
    direction: Mapped[str] = mapped_column(String(16), default="internal")
    intent: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    sentiment: Mapped[str | None] = mapped_column(String(32), nullable=True)
    summary: Mapped[str] = mapped_column(Text)
    objections: Mapped[list] = mapped_column(JSON, default=list)
    commitments: Mapped[list] = mapped_column(JSON, default=list)
    decisions: Mapped[list] = mapped_column(JSON, default=list)
    next_actions: Mapped[list] = mapped_column(JSON, default=list)
    evidence_refs: Mapped[list] = mapped_column(JSON, default=list)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    __table_args__ = (
        Index(
            "ix_commercial_memory_tenant_relationship",
            "tenant_id",
            "relationship_id",
            "occurred_at",
        ),
    )
