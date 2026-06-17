"""Sending ramp — domain-reputation-safe volume planning for outbound email.

250 drafts/day is the production target. 250 *sends*/day from a cold domain is
a reputation risk. This module plans how many approved drafts may actually be
sent today, given the domain's age and health, and refuses to schedule a send
that would breach the ramp, contact a suppressed recipient, exceed the
per-recipient frequency cap, or go out without approval + unsubscribe.

It is a planner only: it returns batches; it never sends. Honors the doctrine
that every external send requires approval and an opt-out.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

# Ramp curve: (min_day_inclusive, max_day_inclusive_or_None, max_per_day, label_ar, label_en)
RAMP_CURVE: tuple[tuple[int, int | None, int, str, str], ...] = (
    (0, 6, 20, "أسبوع 0 — تهيئة", "Week 0 — warm-up"),
    (7, 13, 50, "أسبوع 1", "Week 1"),
    (14, 20, 100, "أسبوع 2", "Week 2"),
    (21, 27, 150, "أسبوع 3", "Week 3"),
    (28, None, 250, "أسبوع 4+ (بصحة سليمة فقط)", "Week 4+ (healthy only)"),
)

# Health states that block all sending until remediated.
BLOCKING_HEALTH: frozenset[str] = frozenset(
    {"unhealthy", "bounce_spike", "spam_warning"}
)
# At week 4+, full 250 is only allowed when healthy; otherwise fall back to 150.
_FULL_VOLUME_FLOOR_WHEN_DEGRADED = 150


@dataclass(frozen=True, slots=True)
class ApprovedDraftRef:
    """The minimal, PII-free view of a draft the ramp needs to schedule it."""

    draft_id: str
    recipient_ref: str
    unsubscribe_included: bool
    approval_status: str  # must be "approved" to be eligible


class RampStage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain_age_days: int
    label_ar: str
    label_en: str
    max_per_day: int


class SendingBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_id: str
    mailbox: str
    send_window: str
    draft_refs: list[str]
    max_volume: int


class SendingPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    mailbox: str
    domain_health: str
    stage: RampStage
    effective_daily_cap: int
    eligible_count: int
    scheduled_count: int
    blocked: bool
    blocked_reason_ar: str = ""
    blocked_reason_en: str = ""
    excluded: dict[str, list[str]] = Field(default_factory=dict)
    batches: list[SendingBatch] = Field(default_factory=list)
    governance_decision: str = "approval_required"
    guardrails: dict[str, bool] = Field(
        default_factory=lambda: {
            "no_send_without_approval": True,
            "no_send_without_unsubscribe": True,
            "suppression_enforced": True,
            "frequency_cap_enforced": True,
            "domain_health_gated": True,
            "ramp_curve_enforced": True,
        }
    )


def ramp_stage_for(domain_age_days: int) -> RampStage:
    """The ramp stage for a domain of the given age (days since first send)."""
    age = max(0, int(domain_age_days))
    for lo, hi, cap, ar, en in RAMP_CURVE:
        if age >= lo and (hi is None or age <= hi):
            return RampStage(domain_age_days=age, label_ar=ar, label_en=en, max_per_day=cap)
    last = RAMP_CURVE[-1]
    return RampStage(
        domain_age_days=age, label_ar=last[3], label_en=last[4], max_per_day=last[2]
    )


def plan_sending_batches(
    *,
    approved: Iterable[ApprovedDraftRef],
    domain_age_days: int,
    domain_health: str = "healthy",
    suppression_refs: Iterable[str] | None = None,
    recently_contacted_refs: Iterable[str] | None = None,
    daily_cap_override: int | None = None,
    mailbox: str = "primary",
    batch_size: int = 25,
    send_window: str = "business_hours_ksa",
) -> SendingPlan:
    """Plan today's safe sending batches from a list of approved drafts."""
    approved = list(approved)
    suppressed = set(suppression_refs or ())
    recent = set(recently_contacted_refs or ())
    health = (domain_health or "healthy").strip().lower()
    stage = ramp_stage_for(domain_age_days)

    # Effective daily cap: ramp max, reduced when degraded, optionally overridden.
    cap = stage.max_per_day
    if stage.max_per_day >= 250 and health != "healthy":
        cap = _FULL_VOLUME_FLOOR_WHEN_DEGRADED
    if daily_cap_override is not None:
        cap = max(0, min(cap, int(daily_cap_override)))

    # Hard block: unhealthy domain → schedule nothing.
    if health in BLOCKING_HEALTH:
        return SendingPlan(
            mailbox=mailbox,
            domain_health=health,
            stage=stage,
            effective_daily_cap=cap,
            eligible_count=0,
            scheduled_count=0,
            blocked=True,
            blocked_reason_ar=f"صحة الدومين «{health}» — يُمنع الإرسال حتى المعالجة.",
            blocked_reason_en=f"Domain health '{health}' — sending blocked until remediated.",
            governance_decision="BLOCK",
        )

    excluded: dict[str, list[str]] = {
        "not_approved": [],
        "missing_unsubscribe": [],
        "suppression_hit": [],
        "frequency_cap": [],
    }
    eligible: list[str] = []
    for d in approved:
        if d.approval_status != "approved":
            excluded["not_approved"].append(d.draft_id)
            continue
        if not d.unsubscribe_included:
            excluded["missing_unsubscribe"].append(d.draft_id)
            continue
        if d.recipient_ref and d.recipient_ref in suppressed:
            excluded["suppression_hit"].append(d.draft_id)
            continue
        if d.recipient_ref and d.recipient_ref in recent:
            excluded["frequency_cap"].append(d.draft_id)
            continue
        eligible.append(d.draft_id)

    scheduled = eligible[:cap]
    batches: list[SendingBatch] = []
    size = max(1, int(batch_size))
    for idx in range(0, len(scheduled), size):
        chunk = scheduled[idx : idx + size]
        batches.append(
            SendingBatch(
                batch_id=f"{mailbox}-{stage.domain_age_days}d-{idx // size + 1}",
                mailbox=mailbox,
                send_window=send_window,
                draft_refs=chunk,
                max_volume=len(chunk),
            )
        )

    return SendingPlan(
        mailbox=mailbox,
        domain_health=health,
        stage=stage,
        effective_daily_cap=cap,
        eligible_count=len(eligible),
        scheduled_count=len(scheduled),
        blocked=False,
        excluded={k: v for k, v in excluded.items() if v},
        batches=batches,
        governance_decision="approval_required",
    )


__all__ = [
    "BLOCKING_HEALTH",
    "RAMP_CURVE",
    "ApprovedDraftRef",
    "RampStage",
    "SendingBatch",
    "SendingPlan",
    "plan_sending_batches",
    "ramp_stage_for",
]
