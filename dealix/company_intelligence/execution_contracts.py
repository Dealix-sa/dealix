"""Persistence-neutral contracts for the Company Intelligence execution spine.

The contracts normalize existing Opportunity and Approval owners without
replacing their storage. Drafts remain approval-first and execution-disabled.

State machines:
  OpportunityStage — research → qualify → … → won | lost | parked
  CanonicalApprovalStatus — pending → granted | rejected | timed_out | withdrawn
  DraftStatus — generated → … → archived (execution_allowed always False)
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class OpportunityStage(StrEnum):
    """Sales pipeline stages aligned with ``dealix.commercial_intelligence``."""

    RESEARCH = "research"
    QUALIFY = "qualify"
    APPROVAL = "approval"
    CONVERSATION = "conversation"
    PILOT = "pilot"
    PROOF = "proof"
    COMMERCIAL = "commercial"
    WON = "won"
    LOST = "lost"
    PARKED = "parked"


class CanonicalApprovalStatus(StrEnum):
    """Approval lifecycle aligned with ``dealix.trust.approval``."""

    PENDING = "pending"
    GRANTED = "granted"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"
    WITHDRAWN = "withdrawn"


class DraftStatus(StrEnum):
    """Draft lifecycle aligned with ``distribution_os.draft_factory``.

    Regardless of status, ``execution_allowed`` remains ``False`` and
    ``approval_required`` remains ``True`` on every canonical draft.
    """

    GENERATED = "generated"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_EDIT = "needs_edit"
    COPIED_MANUALLY = "copied_manually"
    SENT_VIA_INTEGRATION = "sent_via_integration"
    REPLIED = "replied"
    ARCHIVED = "archived"


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


# ---------------------------------------------------------------------------
# State machine transition maps
# ---------------------------------------------------------------------------

_OPPORTUNITY_TRANSITIONS: dict[OpportunityStage, frozenset[OpportunityStage]] = {
    OpportunityStage.RESEARCH: frozenset(
        {OpportunityStage.QUALIFY, OpportunityStage.LOST, OpportunityStage.PARKED}
    ),
    OpportunityStage.QUALIFY: frozenset(
        {OpportunityStage.APPROVAL, OpportunityStage.LOST, OpportunityStage.PARKED}
    ),
    OpportunityStage.APPROVAL: frozenset(
        {OpportunityStage.CONVERSATION, OpportunityStage.LOST, OpportunityStage.PARKED}
    ),
    OpportunityStage.CONVERSATION: frozenset(
        {OpportunityStage.PILOT, OpportunityStage.LOST, OpportunityStage.PARKED}
    ),
    OpportunityStage.PILOT: frozenset(
        {OpportunityStage.PROOF, OpportunityStage.LOST, OpportunityStage.PARKED}
    ),
    OpportunityStage.PROOF: frozenset(
        {OpportunityStage.COMMERCIAL, OpportunityStage.LOST, OpportunityStage.PARKED}
    ),
    OpportunityStage.COMMERCIAL: frozenset(
        {OpportunityStage.WON, OpportunityStage.LOST, OpportunityStage.PARKED}
    ),
    OpportunityStage.WON: frozenset(),  # terminal
    OpportunityStage.LOST: frozenset({OpportunityStage.PARKED}),
    OpportunityStage.PARKED: frozenset(
        {OpportunityStage.RESEARCH, OpportunityStage.QUALIFY}
    ),
}

_APPROVAL_TRANSITIONS: dict[
    CanonicalApprovalStatus, frozenset[CanonicalApprovalStatus]
] = {
    CanonicalApprovalStatus.PENDING: frozenset(
        {
            CanonicalApprovalStatus.GRANTED,
            CanonicalApprovalStatus.REJECTED,
            CanonicalApprovalStatus.TIMED_OUT,
            CanonicalApprovalStatus.WITHDRAWN,
        }
    ),
    CanonicalApprovalStatus.GRANTED: frozenset(),  # terminal
    CanonicalApprovalStatus.REJECTED: frozenset(),  # terminal
    CanonicalApprovalStatus.TIMED_OUT: frozenset(
        {CanonicalApprovalStatus.PENDING}
    ),  # can re-request
    CanonicalApprovalStatus.WITHDRAWN: frozenset(),  # terminal
}

_DRAFT_TRANSITIONS: dict[DraftStatus, frozenset[DraftStatus]] = {
    DraftStatus.GENERATED: frozenset(
        {
            DraftStatus.PENDING_APPROVAL,
            DraftStatus.NEEDS_EDIT,
            DraftStatus.REJECTED,
            DraftStatus.ARCHIVED,
        }
    ),
    DraftStatus.PENDING_APPROVAL: frozenset(
        {DraftStatus.APPROVED, DraftStatus.REJECTED, DraftStatus.NEEDS_EDIT}
    ),
    DraftStatus.APPROVED: frozenset(
        {
            DraftStatus.COPIED_MANUALLY,
            DraftStatus.SENT_VIA_INTEGRATION,
            DraftStatus.ARCHIVED,
        }
    ),
    DraftStatus.REJECTED: frozenset({DraftStatus.ARCHIVED}),
    DraftStatus.NEEDS_EDIT: frozenset(
        {DraftStatus.GENERATED, DraftStatus.ARCHIVED}
    ),
    DraftStatus.COPIED_MANUALLY: frozenset(
        {DraftStatus.REPLIED, DraftStatus.ARCHIVED}
    ),
    DraftStatus.SENT_VIA_INTEGRATION: frozenset(
        {DraftStatus.REPLIED, DraftStatus.ARCHIVED}
    ),
    DraftStatus.REPLIED: frozenset({DraftStatus.ARCHIVED}),
    DraftStatus.ARCHIVED: frozenset(),  # terminal
}


def _normalize_evidence(source_evidence: list[str]) -> list[str]:
    """Return deterministic, non-empty, de-duplicated evidence references."""

    evidence = sorted({item.strip() for item in source_evidence if item.strip()})
    if not evidence:
        raise ValueError("source_evidence requires at least one non-empty reference")
    return evidence


def _draft_digest(
    *,
    tenant_id: str,
    action_id: str,
    opportunity_id: str,
    channel: DraftChannel,
    content: str,
    lawful_contact_basis: LawfulContactBasis,
    source_evidence: list[str],
    risk_level: str,
    is_manual_task: bool,
) -> str:
    """Hash content together with every safety-significant draft attribute."""

    payload = {
        "action_id": action_id.strip(),
        "channel": channel.value,
        "content": content.strip(),
        "is_manual_task": is_manual_task,
        "lawful_contact_basis": lawful_contact_basis.value,
        "opportunity_id": opportunity_id.strip(),
        "risk_level": risk_level.strip(),
        "source_evidence": _normalize_evidence(source_evidence),
        "tenant_id": tenant_id.strip(),
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


class CanonicalOpportunity(BaseModel):
    """Read-only normalized view over the existing opportunity owner."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    opportunity_id: NonEmptyString
    company_id: NonEmptyString
    company_name: str = ""
    offer_id: NonEmptyString
    stage: OpportunityStage
    score: int = Field(..., ge=0, le=100)
    score_reasons: dict[str, Any] = Field(default_factory=dict)
    signal_ids: list[str] = Field(default_factory=list)
    confidence_band: str = "low"
    blockers: list[str] = Field(default_factory=list)
    next_action: NonEmptyString
    proof_target: NonEmptyString
    approval_required: bool = True
    external_action_allowed: bool = False

    @model_validator(mode="after")
    def deny_external_execution_authority(self) -> CanonicalOpportunity:
        if self.external_action_allowed:
            raise ValueError("canonical opportunities never authorize external execution")
        return self


class CanonicalDraft(BaseModel):
    """One draft contract for channel and proposal content.

    This contract intentionally has no send method and cannot authorize live
    execution. A separate approved action must be recorded by the canonical
    Approval owner before any external operation is considered.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    draft_id: NonEmptyString
    action_id: NonEmptyString
    opportunity_id: NonEmptyString
    channel: DraftChannel
    content: NonEmptyString
    content_hash: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    lawful_contact_basis: LawfulContactBasis
    source_evidence: list[NonEmptyString] = Field(..., min_length=1)
    risk_level: NonEmptyString = "medium"
    approval_required: bool = True
    execution_allowed: bool = False
    is_manual_task: bool = False
    status: DraftStatus = DraftStatus.GENERATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_channel_safety_and_integrity(self) -> CanonicalDraft:
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

        normalized_evidence = _normalize_evidence(self.source_evidence)
        if self.source_evidence != normalized_evidence:
            raise ValueError("source_evidence must be sorted and unique")
        expected_hash = _draft_digest(
            tenant_id=self.tenant_id,
            action_id=self.action_id,
            opportunity_id=self.opportunity_id,
            channel=self.channel,
            content=self.content,
            lawful_contact_basis=self.lawful_contact_basis,
            source_evidence=self.source_evidence,
            risk_level=self.risk_level,
            is_manual_task=self.is_manual_task,
        )
        if self.content_hash != expected_hash:
            raise ValueError("content_hash does not match the canonical draft payload")
        if self.draft_id != f"draft_{expected_hash[:16]}":
            raise ValueError("draft_id does not match content_hash")
        return self


class CanonicalApproval(BaseModel):
    """Normalized view over the existing ApprovalRequest contract."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    approval_id: NonEmptyString
    action_id: NonEmptyString
    object_type: NonEmptyString
    object_id: NonEmptyString
    action_type: NonEmptyString
    channel: str | None = None
    risk_level: str = "low"
    status: CanonicalApprovalStatus = CanonicalApprovalStatus.PENDING
    proof_target: NonEmptyString
    audit_ref: str | None = None
    decision_at: datetime | None = None
    execution_allowed: bool = False

    @model_validator(mode="after")
    def require_explicit_execution_decision(self) -> CanonicalApproval:
        if self.execution_allowed and self.status != CanonicalApprovalStatus.GRANTED:
            raise ValueError("execution requires granted status")
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

    normalized_evidence = _normalize_evidence(source_evidence)
    digest = _draft_digest(
        tenant_id=tenant_id,
        action_id=action_id,
        opportunity_id=opportunity_id,
        channel=channel,
        content=content,
        lawful_contact_basis=lawful_contact_basis,
        source_evidence=normalized_evidence,
        risk_level=risk_level,
        is_manual_task=is_manual_task,
    )
    return CanonicalDraft(
        tenant_id=tenant_id,
        draft_id=f"draft_{digest[:16]}",
        action_id=action_id,
        opportunity_id=opportunity_id,
        channel=channel,
        content=content,
        content_hash=digest,
        lawful_contact_basis=lawful_contact_basis,
        source_evidence=normalized_evidence,
        risk_level=risk_level,
        approval_required=True,
        execution_allowed=False,
        is_manual_task=is_manual_task,
        status=DraftStatus.GENERATED,
    )


# ---------------------------------------------------------------------------
# Opportunity transition helpers
# ---------------------------------------------------------------------------


def valid_opportunity_transitions_from(
    stage: OpportunityStage,
) -> frozenset[OpportunityStage]:
    """Return the set of stages reachable from *stage*."""
    return _OPPORTUNITY_TRANSITIONS.get(stage, frozenset())


def is_valid_opportunity_transition(
    from_stage: OpportunityStage,
    to_stage: OpportunityStage,
) -> bool:
    """Check whether *from_stage* → *to_stage* is a valid transition."""
    return to_stage in valid_opportunity_transitions_from(from_stage)


def transition_opportunity(
    opportunity: CanonicalOpportunity,
    *,
    to_stage: OpportunityStage,
) -> CanonicalOpportunity:
    """Return a new opportunity with *to_stage* applied.

    Raises ``ValueError`` if the transition is invalid.
    """
    if not is_valid_opportunity_transition(opportunity.stage, to_stage):
        raise ValueError(
            f"invalid opportunity transition: "
            f"{opportunity.stage.value} → {to_stage.value}"
        )
    return opportunity.model_copy(update={"stage": to_stage})


# ---------------------------------------------------------------------------
# Approval transition helpers
# ---------------------------------------------------------------------------


def valid_approval_transitions_from(
    status: CanonicalApprovalStatus,
) -> frozenset[CanonicalApprovalStatus]:
    """Return the set of statuses reachable from *status*."""
    return _APPROVAL_TRANSITIONS.get(status, frozenset())


def is_valid_approval_transition(
    from_status: CanonicalApprovalStatus,
    to_status: CanonicalApprovalStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_approval_transitions_from(from_status)


def transition_approval(
    approval: CanonicalApproval,
    *,
    to_status: CanonicalApprovalStatus,
    decision_at: datetime | None = None,
) -> CanonicalApproval:
    """Return a new approval with *to_status* applied.

    When transitioning to ``GRANTED``, ``decision_at`` is auto-set if not
    provided. Raises ``ValueError`` if the transition is invalid.
    """
    if not is_valid_approval_transition(approval.status, to_status):
        raise ValueError(
            f"invalid approval transition: "
            f"{approval.status.value} → {to_status.value}"
        )
    updates: dict[str, Any] = {"status": to_status}
    if to_status == CanonicalApprovalStatus.GRANTED or to_status in (
        CanonicalApprovalStatus.REJECTED,
        CanonicalApprovalStatus.WITHDRAWN,
    ):
        updates["decision_at"] = decision_at or datetime.now(UTC)
    return approval.model_copy(update=updates)


# ---------------------------------------------------------------------------
# Draft transition helpers
# ---------------------------------------------------------------------------


def valid_draft_transitions_from(
    status: DraftStatus,
) -> frozenset[DraftStatus]:
    """Return the set of statuses reachable from *status*."""
    return _DRAFT_TRANSITIONS.get(status, frozenset())


def is_valid_draft_transition(
    from_status: DraftStatus,
    to_status: DraftStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_draft_transitions_from(from_status)


def transition_draft(
    draft: CanonicalDraft,
    *,
    to_status: DraftStatus,
) -> CanonicalDraft:
    """Return a new draft with *to_status* applied.

    The safety invariants ``execution_allowed=False`` and
    ``approval_required=True`` are preserved regardless of status.
    Raises ``ValueError`` if the transition is invalid.
    """
    if not is_valid_draft_transition(draft.status, to_status):
        raise ValueError(
            f"invalid draft transition: "
            f"{draft.status.value} → {to_status.value}"
        )
    return draft.model_copy(update={"status": to_status})
