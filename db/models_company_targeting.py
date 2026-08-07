"""Persistent models for governed company targeting and capability evaluation."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Float, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.utils import utcnow
from db.models import Base


class CompanyDirectoryImportRecord(Base):
    __tablename__ = "company_directory_imports"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    source_name: Mapped[str] = mapped_column(String(255))
    source_file_name: Mapped[str] = mapped_column(String(255))
    source_file_sha256: Mapped[str] = mapped_column(String(64), index=True)
    source_sheet: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(32), default="provided_directory")
    allowed_use: Mapped[str] = mapped_column(
        String(128), default="company_research_and_ranking_only"
    )
    source_terms_status: Mapped[str] = mapped_column(
        String(32), default="unverified", index=True
    )
    consent_status: Mapped[str] = mapped_column(String(32), default="unknown")
    retention_until: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="analyzed", index=True)
    rows_total: Mapped[int] = mapped_column(Integer, default=0)
    rows_unique: Mapped[int] = mapped_column(Integer, default=0)
    rows_duplicate: Mapped[int] = mapped_column(Integer, default=0)
    rows_research_only: Mapped[int] = mapped_column(Integer, default=0)
    rows_target_ready: Mapped[int] = mapped_column(Integer, default=0)
    stats_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "source_file_sha256",
            "source_sheet",
            name="uq_company_directory_import_source",
        ),
    )


class CompanyDirectoryEntryRecord(Base):
    """Organization record; raw contact values are intentionally not stored."""

    __tablename__ = "company_directory_entries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    import_id: Mapped[str] = mapped_column(String(64), index=True)
    promoted_account_id: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), index=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    activity: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    has_valid_email: Mapped[bool] = mapped_column(Boolean, default=False)
    has_valid_phone: Mapped[bool] = mapped_column(Boolean, default=False)
    email_masked: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_masked: Mapped[str | None] = mapped_column(String(32), nullable=True)
    email_hmac: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    phone_hmac: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    source_sheet: Mapped[str] = mapped_column(String(255))
    source_row_number: Mapped[int] = mapped_column(Integer)
    source_fingerprint: Mapped[str] = mapped_column(String(64))
    data_quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    fit_score: Mapped[float] = mapped_column(Float, default=0.0)
    research_priority_score: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    priority: Mapped[str] = mapped_column(String(32), index=True)
    recommended_offer_id: Mapped[str] = mapped_column(String(64), index=True)
    value_angle_ar: Mapped[str] = mapped_column(Text)
    relationship_status: Mapped[str] = mapped_column(String(32), default="unknown")
    consent_status: Mapped[str] = mapped_column(String(32), default="unknown")
    targeting_status: Mapped[str] = mapped_column(
        String(32), default="research_only", index=True
    )
    suppression_reasons_json: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "source_fingerprint",
            name="uq_company_directory_entry_fingerprint",
        ),
        Index(
            "ix_company_directory_target_queue",
            "tenant_id",
            "targeting_status",
            "research_priority_score",
        ),
    )


class AgentCapabilityEvaluationRecord(Base):
    __tablename__ = "agent_capability_evaluations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    agent_name: Mapped[str] = mapped_column(String(64), index=True)
    capability: Mapped[str] = mapped_column(String(64), index=True)
    scenario_id: Mapped[str] = mapped_column(String(128), index=True)
    evaluator_version: Mapped[str] = mapped_column(String(32))
    model_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    dimension_scores_json: Mapped[dict] = mapped_column(JSON, default=dict)
    total_score: Mapped[float] = mapped_column(Float)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    critical_failures_json: Mapped[list] = mapped_column(JSON, default=list)
    evidence_json: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)

    __table_args__ = (
        Index(
            "ix_agent_capability_eval_gate",
            "tenant_id",
            "capability",
            "passed",
        ),
    )


class CommercialCampaignPlanRecord(Base):
    __tablename__ = "commercial_campaign_plans"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255))
    offer_id: Mapped[str] = mapped_column(String(64), index=True)
    mode: Mapped[str] = mapped_column(String(32), default="draft_only")
    status: Mapped[str] = mapped_column(String(32), default="planned", index=True)
    segment_filter_json: Mapped[dict] = mapped_column(JSON, default=dict)
    audience_count: Mapped[int] = mapped_column(Integer, default=0)
    experiment_hypothesis: Mapped[str] = mapped_column(Text)
    success_metric: Mapped[str] = mapped_column(String(128))
    guardrails_json: Mapped[list] = mapped_column(JSON, default=list)
    approval_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class CommercialCampaignItemRecord(Base):
    __tablename__ = "commercial_campaign_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    campaign_id: Mapped[str] = mapped_column(String(64), index=True)
    directory_entry_id: Mapped[str] = mapped_column(String(64), index=True)
    account_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    channel: Mapped[str] = mapped_column(String(32), default="research_only")
    status: Mapped[str] = mapped_column(String(32), default="research_only", index=True)
    qualification_json: Mapped[dict] = mapped_column(JSON, default=dict)
    value_case_json: Mapped[dict] = mapped_column(JSON, default=dict)
    objections_json: Mapped[list] = mapped_column(JSON, default=list)
    negotiation_policy_json: Mapped[dict] = mapped_column(JSON, default=dict)
    draft_json: Mapped[dict] = mapped_column(JSON, default=dict)
    approval_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint(
            "campaign_id",
            "directory_entry_id",
            name="uq_campaign_directory_entry",
        ),
    )
