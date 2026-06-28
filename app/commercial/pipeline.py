"""Pipeline state machine for the Commercial Growth OS.

Stages are ordered. Transitions into approval-gated stages (approved, sent,
proposal_sent, won, lost, delivery_handoff) require an explicit approval flag;
otherwise the transition is rejected and the account stays put with a reason.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.commercial.schemas import APPROVAL_GATED_STAGES, PIPELINE_STAGES, PipelineEvent


class PipelineError(ValueError):
    """Raised for an invalid or unauthorised stage transition."""


def _now() -> str:
    return datetime.now(UTC).isoformat()


def requires_approval(stage: str) -> bool:
    return stage in APPROVAL_GATED_STAGES


def transition(
    account_id: str,
    previous_stage: str,
    next_stage: str,
    *,
    approved: bool = False,
    evidence: str = "",
    owner: str = "unassigned",
    event_index: int = 0,
) -> PipelineEvent:
    """Build a PipelineEvent for a stage transition.

    Raises :class:`PipelineError` if the target stage is unknown, or if it is
    approval-gated and ``approved`` is not True.
    """
    if next_stage not in PIPELINE_STAGES:
        raise PipelineError(f"unknown stage: {next_stage}")
    if requires_approval(next_stage) and not approved:
        raise PipelineError(
            f"stage '{next_stage}' is approval-gated and requires explicit approval"
        )

    return PipelineEvent(
        event_id=f"evt_{account_id}_{event_index:03d}",
        account_id=account_id,
        stage=next_stage,
        previous_stage=previous_stage,
        next_stage="",
        evidence=evidence or f"transition {previous_stage} → {next_stage}",
        owner=owner,
        created_at=_now(),
    )


def initial_event(account: Any, event_index: int = 0) -> PipelineEvent:
    """Record where an account enters the pipeline after sourcing."""
    account_id = getattr(account, "account_id", None) or account.get("account_id")
    verified = (getattr(account, "verification_status", None) or account.get("verification_status")) == "verified"
    stage = "verified" if verified else "researched"
    return PipelineEvent(
        event_id=f"evt_{account_id}_{event_index:03d}",
        account_id=account_id,
        stage=stage,
        previous_stage="",
        next_stage="",
        evidence="sourced & validated" if verified else "sourced, pending verification",
        owner=getattr(account, "owner", None) or account.get("owner") or "unassigned",
        created_at=_now(),
    )
