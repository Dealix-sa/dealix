"""Persistence-neutral contracts for the Company Intelligence execution spine.

The contracts normalize existing Opportunity and Approval owners without
replacing their storage. Drafts remain approval-first and execution-disabled.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DraftChannel(StrEnum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LINKEDIN = "linkedin"
    PROPOSAL = "proposal"


class LawfulContactBasis(StrEnum):
    EXISTING_RELATIONSHIP = "existing_relationship"
    EXPLICIT_OPT_IN = "explicit_opt_in"
    APPROVED_TEMPLATE = "approved_template"
    MANUAL_RESEARCH_ONLY = "manual_research_only"
    NOT_APPLICABLE = "not_applicable"


class CanonicalOpportunity(BaseModel):
    """Read-only normalized view over the existing opportunity owner."""

    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    opportunity_id: str = Field(..., min_length=1)
    company_id: str = Field(..., min_length=1)
    company_name: str = ""
    offer_id: str = Field(..., min_length=1)
    stage: str = Field(..., min_length=1)
    score: int = Field(..., ge=0, le=100)
    score_reasons: dict[str, Any] = Field(default_factory=dict)
    signal_ids: list[str] = Field(default_factory=list)
    confidence_band: str = "low"
    blockers: list[str] = Field(default_factory=list)
    next_action: str = Field(..., min_length=1)
    proof_target: str = Field(..., min_length=1)
    approval_required: bool = True
    external_action_allowed: bool = False

    @model_validator(mode="after")
    def deny_unapproved_external_action(self) -> CanonicalOpportunity:
        if self.external_action_allowed and self.approval_required:
            raise ValueError("external action cannot be allowed while approval is required")
        return self


class CanonicalDraft(BaseModel):
    """One draft contract for channel and proposal content.

    This contract intentionally has no send method and cannot authorize live
    execution. A separate approved action must be recorded by the canonical
    Approval owner before any external operation is considered.
    """

    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    draft_id: str = Field(..., min_length=1)
    action_id: str = Field(..., min_length=1)
    opportunity_id: str = Field(..., min_length=1)
    channel: DraftChannel
    content: str = Field(..., min_length=1)
    content_hash: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    lawful_contact_basis: LawfulContactBasis
    source_evidence: list[str] = Field(..., min_length=1)
    risk_level: str = "medium"
    approval_required: bool = True
    execution_allowed: bool = False
    is_manual_task: bool = False
    status: str = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_channel_safety(self) -> CanonicalDraft:
        if self.execution_allowed:
            raise ValueError("canonical drafts never authorize execution")
        if not self.approval_required:
            raise ValueError("canonical drafts require approval")
        if self.channel is DraftChannel.WHATSAPP and self.lawful_contact_basis not in {
            LawfulContactBasis.EXISTING_RELATIONSHIP,
            LawfulContactBasis.EXPLICIT_OPT_IN,
            LawfulContactBasis.APPROVED_TEMPLATE,
        }:
            raise ValueError("cold WhatsApp is forbidden")
        if self.channel is DraftChannel.LINKEDIN:
            if self.lawful_contact_basis is not LawfulContactBasis.MANUAL_RESEARCH_ONLY:
                raise ValueError("LinkedIn drafts must be manual-research-only")
            if not self.is_manual_task:
                raise ValueError("LinkedIn automation is forbidden")
        return self


class CanonicalApproval(BaseModel):
    """Normalized view over the existing ApprovalRequest contract."""

    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    approval_id: str = Field(..., min_length=1)
    action_id: str = Field(..., min_length=1)
    object_type: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    channel: str | None = None
    risk_level: str = "low"
    status: str = "pending"
    proof_target: str = Field(..., min_length=1)
    audit_ref: str | None = None
    decision_at: datetime | None = None
    execution_allowed: bool = False

    @model_validator(mode="after")
    def require_explicit_execution_decision(self) -> CanonicalApproval:
        if self.execution_allowed and self.status != "approved":
            raise ValueError("execution requires approved status")
        return self


def normalize_opportunity(record: Any) -> CanonicalOpportunity:
    """Adapt ``CommercialOpportunityRecord`` without importing its storage."""

    return CanonicalOpportunity(
        tenant_id=record.tenant_id,
        opportunity_id=record.id,
        company_id=record.account_id,
        company_name=record.company_name,
        offer_id=record.offer_id,
        stage=record.stage,
        score=record.score,
        score_reasons=dict(record.score_components_json or {}),
        signal_ids=list(record.source_signal_ids_json or []),
        confidence_band=record.confidence_band,
        blockers=list(record.blockers_json or []),
        next_action=record.next_action,
        proof_target=record.proof_target,
        approval_required=record.approval_required,
        external_action_allowed=record.external_action_allowed,
    )


def normalize_approval(request: Any, *, tenant_id: str | None = None) -> CanonicalApproval:
    """Adapt ``ApprovalRequest`` and make tenant/action/proof fields mandatory."""

    resolved_tenant = tenant_id or request.customer_id
    if not resolved_tenant:
        raise ValueError("tenant_id is required")
    if not request.action_id:
        raise ValueError("action_id is required")
    if not request.proof_target:
        raise ValueError("proof_target is required")

    status = str(request.status)
    if status.startswith("ApprovalStatus."):
        status = status.rsplit(".", 1)[-1].lower()
    return CanonicalApproval(
        tenant_id=resolved_tenant,
        approval_id=request.approval_id,
        action_id=request.action_id,
        object_type=request.object_type,
        object_id=request.object_id,
        action_type=request.action_type,
        channel=request.channel,
        risk_level=request.risk_level,
        status=status,
        proof_target=request.proof_target,
        audit_ref=request.audit_ref,
        execution_allowed=False,
    )


def build_draft(
    *,
    tenant_id: str,
    action_id: str,
    opportunity_id: str,
    channel: DraftChannel,
    content: str,
    lawful_contact_basis: LawfulContactBasis,
    source_evidence: list[str],
    risk_level: str = "medium",
    is_manual_task: bool = False,
) -> CanonicalDraft:
    """Build a deterministic, idempotent, execution-disabled draft."""

    canonical = "\n".join(
        [tenant_id, action_id, opportunity_id, channel.value, content.strip()]
    )
    digest = sha256(canonical.encode("utf-8")).hexdigest()
    return CanonicalDraft(
        tenant_id=tenant_id,
        draft_id=f"draft_{digest[:16]}",
        action_id=action_id,
        opportunity_id=opportunity_id,
        channel=channel,
        content=content.strip(),
        content_hash=digest,
        lawful_contact_basis=lawful_contact_basis,
        source_evidence=source_evidence,
        risk_level=risk_level,
        approval_required=True,
        execution_allowed=False,
        is_manual_task=is_manual_task,
    )
