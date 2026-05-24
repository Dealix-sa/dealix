"""Autonomous loops — pure-compute scheduling units.

Four loops:
    - morning_loop: 6am AST daily
    - evening_loop: 8pm AST daily
    - weekly_loop: Sunday 6pm AST
    - monthly_loop: Day 1 of month

Each loop is a *pure* function that takes a snapshot dict and returns a
result dataclass. The cron-style scripts in /scripts call these functions
with live data and write the markdown outputs.

No external I/O happens here. No sends, no DB writes. Calling a loop is
safe and idempotent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.friction_log import FrictionAggregate


def _utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Morning loop
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class MorningLoopResult:
    """Output of the daily morning loop (6am AST)."""

    governance_decision: GovernanceDecision
    leads_refreshed: int
    leads_scored: int
    drafts_queued: int  # always DRAFT-ONLY, awaiting approval_center
    high_priority_actions: tuple[str, ...]
    founder_digest_ar: str
    founder_digest_en: str
    timestamp: str


def morning_loop(
    *,
    leads_inbound: int = 0,
    leads_scored: int = 0,
    drafts_pending: int = 0,
    war_room_signals: dict[str, Any] | None = None,
) -> MorningLoopResult:
    """Daily morning refresh — pipeline + scoring + draft queue.

    All outreach drafts queued by this loop are routed to approval_center.
    No external send occurs.
    """
    signals = war_room_signals or {}
    actions: list[str] = []

    if leads_inbound > 0:
        actions.append(f"score_{leads_inbound}_inbound_leads")
    if drafts_pending > 0:
        actions.append(f"founder_approve_{drafts_pending}_drafts")
    if signals.get("paid_invoices_pending"):
        actions.append("confirm_paid_invoices_with_moyasar")
    if signals.get("sprint_in_flight"):
        actions.append("check_sprint_kickoff_readiness")
    if not actions:
        actions.append("warm_list_outreach_drafts_for_founder_review")

    digest_ar = (
        f"صباح اليوم: {leads_inbound} لِيد جديد، {leads_scored} مُسجَّل، "
        f"{drafts_pending} مسودة بانتظار موافقتك. لن يُرسل أي شيء بدون مراجعتك."
    )
    digest_en = (
        f"This morning: {leads_inbound} new leads, {leads_scored} scored, "
        f"{drafts_pending} drafts awaiting your approval. Nothing will be sent without your review."
    )

    return MorningLoopResult(
        governance_decision=GovernanceDecision.REQUIRE_APPROVAL,
        leads_refreshed=leads_inbound,
        leads_scored=leads_scored,
        drafts_queued=drafts_pending,
        high_priority_actions=tuple(actions),
        founder_digest_ar=digest_ar,
        founder_digest_en=digest_en,
        timestamp=_utc_now_iso(),
    )


# ---------------------------------------------------------------------------
# Evening loop
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class EveningLoopResult:
    """Output of the daily evening loop (8pm AST)."""

    governance_decision: GovernanceDecision
    revenue_today_sar: float
    leads_in_pipeline: int
    friction_events_today: int
    high_severity_frictions: int
    tomorrow_top_4: tuple[str, ...]
    founder_digest_ar: str
    founder_digest_en: str
    timestamp: str


def evening_loop(
    *,
    revenue_today_sar: float = 0.0,
    leads_in_pipeline: int = 0,
    friction: FrictionAggregate | None = None,
    overdue_proof_packs: int = 0,
    upcoming_sprints: int = 0,
    retainer_due: int = 0,
) -> EveningLoopResult:
    """Daily evening refresh — KPIs + friction review + tomorrow priorities."""
    fevents = 0
    fhigh = 0
    if friction is not None:
        fevents = int(getattr(friction, "total", 0))
        fhigh = int(friction.by_severity.get("high", 0) if hasattr(friction, "by_severity") else 0)

    actions: list[str] = []
    if fhigh > 0:
        actions.append(f"resolve_{fhigh}_high_severity_friction_events")
    if overdue_proof_packs > 0:
        actions.append(f"finish_{overdue_proof_packs}_overdue_proof_packs")
    if retainer_due > 0:
        actions.append(f"propose_{retainer_due}_retainer_offers")
    if upcoming_sprints > 0:
        actions.append(f"prepare_{upcoming_sprints}_sprint_kickoffs")
    if not actions:
        actions.append("continue_warm_list_outreach_drafts")

    top_4 = tuple(actions[:4])

    digest_ar = (
        f"مساء اليوم: إيرادات اليوم={revenue_today_sar:.0f} ريال، "
        f"خط الأنابيب={leads_in_pipeline}، احتكاكات={fevents} (شديدة={fhigh}). "
        f"أهم 4 مهام للغد جاهزة."
    )
    digest_en = (
        f"Tonight: revenue today={revenue_today_sar:.0f} SAR, "
        f"pipeline={leads_in_pipeline}, frictions={fevents} (high={fhigh}). "
        f"Top 4 tasks for tomorrow ready."
    )

    return EveningLoopResult(
        governance_decision=GovernanceDecision.ALLOW,
        revenue_today_sar=revenue_today_sar,
        leads_in_pipeline=leads_in_pipeline,
        friction_events_today=fevents,
        high_severity_frictions=fhigh,
        tomorrow_top_4=top_4,
        founder_digest_ar=digest_ar,
        founder_digest_en=digest_en,
        timestamp=_utc_now_iso(),
    )


# ---------------------------------------------------------------------------
# Weekly loop
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class WeeklyLoopResult:
    """Output of the Sunday weekly loop."""

    governance_decision: GovernanceDecision
    retainers_eligible: int
    capital_assets_added: int
    proof_packs_completed: int
    revenue_week_sar: float
    mrr_sar: float
    one_time_week_sar: float
    week_over_week_pct: float
    next_week_focus_ar: str
    next_week_focus_en: str
    timestamp: str


def weekly_loop(
    *,
    retainers_eligible: int = 0,
    capital_assets_added: int = 0,
    proof_packs_completed: int = 0,
    revenue_week_sar: float = 0.0,
    revenue_last_week_sar: float = 0.0,
    mrr_sar: float = 0.0,
    one_time_week_sar: float = 0.0,
) -> WeeklyLoopResult:
    """Weekly executive cycle — retainer eligibility + capital reconciliation."""
    if revenue_last_week_sar > 0:
        wow = (revenue_week_sar - revenue_last_week_sar) / revenue_last_week_sar * 100.0
    else:
        wow = 0.0 if revenue_week_sar == 0 else 100.0

    if revenue_week_sar < 1000 and mrr_sar == 0:
        focus_ar = "التركيز: تفعيل أول دفعة عبر Moyasar + تحضير 5 تشخيصات مجانية."
        focus_en = "Focus: first Moyasar charge + prep 5 free diagnostics."
    elif retainers_eligible > 0:
        focus_ar = f"التركيز: عرض {retainers_eligible} retainer جاهز للترقية."
        focus_en = f"Focus: propose {retainers_eligible} retainer ready for upgrade."
    elif proof_packs_completed > 0:
        focus_ar = "التركيز: نشر Proof Packs المعتمدة + استخراج Capital Assets."
        focus_en = "Focus: publish approved Proof Packs + extract Capital Assets."
    else:
        focus_ar = "التركيز: تسريع warm-list + تحضير محتوى LinkedIn (drafts فقط)."
        focus_en = "Focus: accelerate warm-list + prep LinkedIn content (drafts only)."

    return WeeklyLoopResult(
        governance_decision=GovernanceDecision.REQUIRE_APPROVAL,
        retainers_eligible=retainers_eligible,
        capital_assets_added=capital_assets_added,
        proof_packs_completed=proof_packs_completed,
        revenue_week_sar=revenue_week_sar,
        mrr_sar=mrr_sar,
        one_time_week_sar=one_time_week_sar,
        week_over_week_pct=round(wow, 2),
        next_week_focus_ar=focus_ar,
        next_week_focus_en=focus_en,
        timestamp=_utc_now_iso(),
    )


# ---------------------------------------------------------------------------
# Monthly loop
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class MonthlyLoopResult:
    """Output of the Day-1-of-month strategic loop."""

    governance_decision: GovernanceDecision
    month_phase: str  # "activation" | "expansion" | "compounding"
    cumulative_revenue_sar: float
    active_retainers: int
    capital_assets_total: int
    milestone_verdict: str  # "ahead" | "on_track" | "behind"
    decisions_for_founder: tuple[str, ...]
    rationale_ar: str
    rationale_en: str
    timestamp: str


def monthly_loop(
    *,
    day_count_since_launch: int,
    cumulative_revenue_sar: float = 0.0,
    active_retainers: int = 0,
    capital_assets_total: int = 0,
    doctrine_violations: int = 0,
) -> MonthlyLoopResult:
    """Monthly strategic review — 30/60/90 milestone + gate re-assessment."""
    if day_count_since_launch <= 30:
        phase = "activation"
        target_revenue = 5000.0
        target_retainers = 0
    elif day_count_since_launch <= 60:
        phase = "expansion"
        target_revenue = 20000.0
        target_retainers = 1
    elif day_count_since_launch <= 90:
        phase = "compounding"
        target_revenue = 40000.0
        target_retainers = 3
    else:
        phase = "scaling"
        target_revenue = 60000.0
        target_retainers = 5

    if cumulative_revenue_sar >= target_revenue * 1.2 and active_retainers >= target_retainers:
        verdict = "ahead"
    elif cumulative_revenue_sar >= target_revenue * 0.8:
        verdict = "on_track"
    else:
        verdict = "behind"

    decisions: list[str] = []
    if doctrine_violations > 0:
        decisions.append(f"address_{doctrine_violations}_doctrine_violations_critical")
    if verdict == "behind" and day_count_since_launch >= 60:
        decisions.append("halt_new_offer_dev_focus_sales_motion")
    if phase == "compounding" and verdict == "ahead":
        decisions.append("propose_wave_3_enterprise_trust")
    if active_retainers < target_retainers:
        decisions.append("retainer_proposal_blitz_this_month")
    if capital_assets_total < day_count_since_launch / 18:
        decisions.append("audit_engagements_for_missed_capital_assets")
    if not decisions:
        decisions.append("maintain_current_cadence")

    gov = GovernanceDecision.BLOCK if doctrine_violations > 0 else GovernanceDecision.REQUIRE_APPROVAL

    rationale_ar = (
        f"المرحلة: {phase} (يوم {day_count_since_launch}). الإيراد التراكمي="
        f"{cumulative_revenue_sar:.0f} ريال (الهدف={target_revenue:.0f}). "
        f"احتفاظات نشطة={active_retainers}/{target_retainers}. الحُكم: {verdict}."
    )
    rationale_en = (
        f"Phase: {phase} (day {day_count_since_launch}). Cumulative revenue="
        f"{cumulative_revenue_sar:.0f} SAR (target={target_revenue:.0f}). "
        f"Active retainers={active_retainers}/{target_retainers}. Verdict: {verdict}."
    )

    return MonthlyLoopResult(
        governance_decision=gov,
        month_phase=phase,
        cumulative_revenue_sar=cumulative_revenue_sar,
        active_retainers=active_retainers,
        capital_assets_total=capital_assets_total,
        milestone_verdict=verdict,
        decisions_for_founder=tuple(decisions),
        rationale_ar=rationale_ar,
        rationale_en=rationale_en,
        timestamp=_utc_now_iso(),
    )


__all__ = [
    "EveningLoopResult",
    "MonthlyLoopResult",
    "MorningLoopResult",
    "WeeklyLoopResult",
    "evening_loop",
    "monthly_loop",
    "morning_loop",
    "weekly_loop",
]
