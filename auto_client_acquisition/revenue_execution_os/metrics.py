"""Distribution metrics — honest counts derived from the JSONL stores.

No invented numbers: every figure is a count or ratio over recorded entities.
Pipeline value is explicitly an *estimate* from offer floors, not booked
revenue.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.followup_engine import build_followup_queue
from auto_client_acquisition.revenue_execution_os.models import (
    APPROVED_DRAFT_STATUSES,
    OPEN_DRAFT_STATUSES,
    DraftStatus,
    Outcome,
    ProposalStatus,
)
from auto_client_acquisition.revenue_execution_os.offers import offer_by_key
from auto_client_acquisition.revenue_execution_os.win_loss import weekly_learning


def _today_str(now: datetime) -> str:
    return now.date().isoformat()


def _created_today(created_at: str, today: str) -> bool:
    return str(created_at)[:10] == today


def _within(created_at: str, *, cutoff: datetime) -> bool:
    try:
        ts = datetime.fromisoformat(created_at)
    except Exception:
        return False
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=UTC)
    return ts >= cutoff


def daily_metrics(now: datetime | None = None) -> dict[str, object]:
    """Today's activity counts plus current open/due counts."""
    now = now or datetime.now(UTC)
    today = _today_str(now)
    prospects = stores.PROSPECTS.list(limit=1_000_000)
    drafts = stores.DRAFTS.list(limit=1_000_000)
    proposals = stores.PROPOSALS.list(limit=1_000_000)
    handoffs = stores.PAYMENT_HANDOFFS.list(limit=1_000_000)
    win_loss = stores.WIN_LOSS.list(limit=1_000_000)

    return {
        "date": today,
        "prospects_added": sum(1 for p in prospects if _created_today(p.created_at, today)),
        "drafts_generated": sum(1 for d in drafts if _created_today(d.created_at, today)),
        "drafts_open": sum(1 for d in drafts if d.status in OPEN_DRAFT_STATUSES),
        "drafts_approved": sum(1 for d in drafts if d.status in APPROVED_DRAFT_STATUSES),
        "drafts_copied": sum(1 for d in drafts if d.status == DraftStatus.COPIED_MANUALLY),
        "followups_due": len(build_followup_queue(now=now)),
        "proposals_generated": sum(1 for p in proposals if _created_today(p.created_at, today)),
        "payment_handoffs": sum(1 for h in handoffs if _created_today(h.created_at, today)),
        "won_today": sum(
            1 for r in win_loss if r.outcome == Outcome.WON and _created_today(r.created_at, today)
        ),
        "lost_today": sum(
            1 for r in win_loss if r.outcome == Outcome.LOST and _created_today(r.created_at, today)
        ),
    }


def _pipeline_estimate_sar(open_proposals) -> float:
    total = 0.0
    for p in open_proposals:
        try:
            offer = offer_by_key(p.offer_key)
        except KeyError:
            continue
        if offer.one_time_max > 0:
            total += offer.one_time_min
        elif offer.monthly_max > 0:
            total += offer.monthly_min * 12
    return total


def weekly_metrics(now: datetime | None = None, *, window_days: int = 7) -> dict[str, object]:
    """Rates over a rolling window plus an estimated pipeline value."""
    now = now or datetime.now(UTC)
    cutoff = now - timedelta(days=window_days)
    drafts = [
        d for d in stores.DRAFTS.list(limit=1_000_000) if _within(d.created_at, cutoff=cutoff)
    ]
    prospects = [
        p for p in stores.PROSPECTS.list(limit=1_000_000) if _within(p.created_at, cutoff=cutoff)
    ]
    proposals_all = stores.PROPOSALS.list(limit=1_000_000)
    proposals_window = [p for p in proposals_all if _within(p.created_at, cutoff=cutoff)]
    open_proposals = [
        p
        for p in proposals_all
        if p.status
        in (ProposalStatus.PENDING_APPROVAL, ProposalStatus.SENT, ProposalStatus.APPROVED)
    ]

    total_drafts = len(drafts)
    approved = sum(1 for d in drafts if d.status in APPROVED_DRAFT_STATUSES)
    replied = sum(1 for d in drafts if d.status == DraftStatus.REPLIED)
    learning = weekly_learning(window_days=window_days, now=now)

    return {
        "window_days": window_days,
        "prospects_added": len(prospects),
        "drafts_generated": total_drafts,
        "approval_rate": round(approved / total_drafts, 3) if total_drafts else 0.0,
        "reply_rate": round(replied / total_drafts, 3) if total_drafts else 0.0,
        "proposals_generated": len(proposals_window),
        "proposal_rate": round(len(proposals_window) / len(prospects), 3) if prospects else 0.0,
        "close_rate": learning["close_rate"],
        "won": learning["won"],
        "lost": learning["lost"],
        "best_sector": learning["best_sector"],
        "best_channel": learning["best_channel"],
        "best_offer": learning["best_offer"],
        "top_objections": learning["top_objections"],
        "pipeline_value_estimated_sar": round(_pipeline_estimate_sar(open_proposals), 0),
    }


__all__ = ["daily_metrics", "weekly_metrics"]
