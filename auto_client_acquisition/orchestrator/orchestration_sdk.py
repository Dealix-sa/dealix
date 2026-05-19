"""Agent Orchestration SDK (M5) — one governed surface for agents.

Everything built across Phases 1-4 — the approval queue, the lead
lifecycle state machine, the sequencing engine, the governance log, the
governed-day entrypoint — is reachable here through one small, typed,
documented import. An agent does not need to know which module owns which
capability; it imports this SDK and stays inside the governed rails.

The cardinal rule this SDK enforces by construction: an agent can *draft*,
*schedule*, *advance state*, and *record* — but it can never *send*. Every
outbound path returns an :class:`ApprovalRequest` for the founder.

    from auto_client_acquisition.orchestrator import orchestration_sdk as sdk

    appr = sdk.queue_draft(action_type="draft_email", object_type="outreach",
                           object_id="msg_1", channel="email", lead_id="lead_9")
    plan = sdk.plan_follow_ups(channel="email")
    move = sdk.advance_lead(lead_id="lead_9", current=sdk.Stage.CAPTURED,
                            target=sdk.Stage.QUALIFIED)
    day  = sdk.run_day()
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.approval_center import ApprovalRequest
from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)
from auto_client_acquisition.governance_os import governance_log
from auto_client_acquisition.orchestrator.governed_day import (
    GovernedDayResult,
    run_governed_day,
)
from auto_client_acquisition.sales_os.draft_approval_bridge import (
    queue_draft_for_approval,
    queue_follow_up_for_approval,
)
from auto_client_acquisition.sales_os.lead_lifecycle import (
    LeadLifecycleStage,
    TransitionResult,
    advance,
    next_stages,
)
from auto_client_acquisition.sales_os.sequencing_engine import (
    PlannedTask,
    plan_cadence,
)

# Re-export the lifecycle enum so agents need only this one import.
Stage = LeadLifecycleStage


# ─── Draft → governed queue ──────────────────────────────────────

def queue_draft(
    *,
    action_type: str,
    object_type: str,
    object_id: str,
    summary_ar: str = "",
    summary_en: str = "",
    channel: str | None = None,
    risk_level: str = "low",
    lead_id: str | None = None,
    content: str = "",
) -> ApprovalRequest:
    """Put an agent draft into the governed approval queue (never sends)."""
    return queue_draft_for_approval(
        action_type=action_type,
        object_type=object_type,
        object_id=object_id,
        summary_ar=summary_ar,
        summary_en=summary_en,
        channel=channel,
        risk_level=risk_level,
        lead_id=lead_id,
        content=content,
    )


def queue_follow_up(
    *,
    task_id: str,
    lead_id: str,
    attempt: int,
    channel: str,
    draft_ar: str = "",
    draft_en: str = "",
) -> ApprovalRequest:
    """Queue one follow-up touch for founder approval."""
    return queue_follow_up_for_approval(
        task_id=task_id,
        lead_id=lead_id,
        attempt=attempt,
        channel=channel,
        draft_ar=draft_ar,
        draft_en=draft_en,
    )


def pending_approvals() -> list[ApprovalRequest]:
    """Everything currently awaiting the founder."""
    return get_default_approval_store().list_pending()


# ─── Lead lifecycle ──────────────────────────────────────────────

def advance_lead(
    *,
    lead_id: str,
    current: LeadLifecycleStage,
    target: LeadLifecycleStage,
    actor: str = "system",
    note: str = "",
) -> TransitionResult:
    """Validate a lifecycle transition (forward-only). Pure — caller persists."""
    return advance(lead_id=lead_id, current=current, target=target, actor=actor, note=note)


def lead_next_stages(current: LeadLifecycleStage) -> list[LeadLifecycleStage]:
    """Every stage legally reachable from ``current``."""
    return next_stages(current)


# ─── Sequencing ──────────────────────────────────────────────────

def plan_follow_ups(*, channel: str = "email", touches: int = 4) -> list[PlannedTask]:
    """Plan a follow-up cadence (pure — materialize via sequencing_engine)."""
    return plan_cadence(channel=channel, touches=touches)


# ─── Governance ──────────────────────────────────────────────────

def log_blocked(*, action_type: str, reason: str, actor: str = "system") -> None:
    """Record that a governance gate stopped an action."""
    governance_log.record_blocked(action_type=action_type, reason=reason, actor=actor)


def governance_events(limit: int = 100) -> list[dict[str, Any]]:
    """Recent governance events, newest first."""
    return governance_log.query_recent(limit=limit)


# ─── The day ─────────────────────────────────────────────────────

def run_day(*, dry_run: bool = False) -> GovernedDayResult:
    """Run one observable governed day."""
    return run_governed_day(dry_run=dry_run)


__all__ = [
    "Stage",
    "queue_draft",
    "queue_follow_up",
    "pending_approvals",
    "advance_lead",
    "lead_next_stages",
    "plan_follow_ups",
    "log_blocked",
    "governance_events",
    "run_day",
]
