"""Follow-up engine — deterministic cadence that builds a due queue.

Cadence: Day 0 first outreach, +2 days follow-up 1, +2 days follow-up 2,
+3 days breakup. A reply switches the prospect to a discovery invite. Sent
proposals get a 48h nudge; sent payment handoffs get a 24h nudge.

The engine only *generates* a queue of suggested follow-ups for the founder
to approve — nothing is sent automatically.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.models import (
    Channel,
    Draft,
    DraftStatus,
    DraftType,
    Followup,
    FollowupStatus,
    PaymentHandoff,
    PaymentHandoffStatus,
    Proposal,
    ProposalStatus,
    Prospect,
    now_iso,
)

# gap (in days) from the previous step before the next step is due
GAP_FOLLOWUP_1 = 2
GAP_FOLLOWUP_2 = 2
GAP_BREAKUP = 3
GAP_PROPOSAL = 2
GAP_PAYMENT = 1


def _parse(iso: str) -> datetime | None:
    try:
        ts = datetime.fromisoformat(iso)
    except Exception:
        return None
    return ts.replace(tzinfo=UTC) if ts.tzinfo is None else ts


def _age_days(iso: str, now: datetime) -> float:
    ts = _parse(iso)
    if ts is None:
        return -1.0
    return (now - ts).total_seconds() / 86400.0


def _latest(drafts: Sequence[Draft], dtype: str) -> Draft | None:
    cands = [d for d in drafts if d.draft_type == dtype]
    return max(cands, key=lambda d: d.created_at) if cands else None


def _mk(prospect: Prospect, reason: str, dtype: str, channel: str = Channel.EMAIL) -> Followup:
    ts = now_iso()
    return Followup(
        followup_id=f"fup_{uuid4().hex[:18]}",
        prospect_id=prospect.prospect_id,
        reason=reason,
        channel=channel,
        suggested_draft_type=dtype,
        due_date=ts,
        status=FollowupStatus.DUE,
        created_at=ts,
    )


def due_followups_for_prospect(
    prospect: Prospect,
    drafts: Sequence[Draft],
    *,
    proposals: Sequence[Proposal] = (),
    handoffs: Sequence[PaymentHandoff] = (),
    now: datetime | None = None,
) -> list[Followup]:
    """Return the follow-ups due *now* for one prospect (pure, no persistence)."""
    now = now or datetime.now(UTC)
    out: list[Followup] = []

    replied = any(d.status == DraftStatus.REPLIED for d in drafts)
    has_discovery = any(d.draft_type == DraftType.DISCOVERY_INVITE for d in drafts)
    if replied and not has_discovery:
        out.append(_mk(prospect, "prospect_replied", DraftType.DISCOVERY_INVITE))
    elif not replied:
        first = _latest(drafts, DraftType.OUTREACH_FIRST)
        f1 = _latest(drafts, DraftType.OUTREACH_FOLLOWUP_1)
        f2 = _latest(drafts, DraftType.OUTREACH_FOLLOWUP_2)
        breakup = _latest(drafts, DraftType.BREAKUP)
        if first and not f1 and _age_days(first.created_at, now) >= GAP_FOLLOWUP_1:
            out.append(_mk(prospect, "no_reply_day2", DraftType.OUTREACH_FOLLOWUP_1))
        elif f1 and not f2 and _age_days(f1.created_at, now) >= GAP_FOLLOWUP_2:
            out.append(_mk(prospect, "no_reply_day4", DraftType.OUTREACH_FOLLOWUP_2))
        elif f2 and not breakup and _age_days(f2.created_at, now) >= GAP_BREAKUP:
            out.append(_mk(prospect, "no_reply_day7", DraftType.BREAKUP))

    open_props = [
        p for p in proposals if p.status in (ProposalStatus.SENT, ProposalStatus.PENDING_APPROVAL)
    ]
    latest_prop = max(open_props, key=lambda p: p.created_at) if open_props else None
    if latest_prop and _age_days(latest_prop.created_at, now) >= GAP_PROPOSAL:
        out.append(_mk(prospect, "proposal_followup_48h", DraftType.PAYMENT_FOLLOWUP))

    sent_handoffs = [h for h in handoffs if h.status == PaymentHandoffStatus.SENT]
    latest_handoff = max(sent_handoffs, key=lambda h: h.created_at) if sent_handoffs else None
    if latest_handoff and _age_days(latest_handoff.created_at, now) >= GAP_PAYMENT:
        out.append(_mk(prospect, "payment_link_24h", DraftType.PAYMENT_FOLLOWUP))

    return out


def build_followup_queue(*, now: datetime | None = None, persist: bool = False) -> list[Followup]:
    """Compose the due follow-up queue across all prospects from the stores."""
    now = now or datetime.now(UTC)
    all_drafts = stores.DRAFTS.list(limit=100_000)
    all_props = stores.PROPOSALS.list(limit=100_000)
    all_handoffs = stores.PAYMENT_HANDOFFS.list(limit=100_000)
    drafts_by_p: dict[str, list[Draft]] = {}
    props_by_p: dict[str, list[Proposal]] = {}
    handoffs_by_p: dict[str, list[PaymentHandoff]] = {}
    for d in all_drafts:
        drafts_by_p.setdefault(d.prospect_id, []).append(d)
    for p in all_props:
        props_by_p.setdefault(p.prospect_id, []).append(p)
    for h in all_handoffs:
        handoffs_by_p.setdefault(h.prospect_id, []).append(h)

    queue: list[Followup] = []
    for prospect in stores.PROSPECTS.list(limit=100_000):
        queue.extend(
            due_followups_for_prospect(
                prospect,
                drafts_by_p.get(prospect.prospect_id, []),
                proposals=props_by_p.get(prospect.prospect_id, []),
                handoffs=handoffs_by_p.get(prospect.prospect_id, []),
                now=now,
            )
        )
    if persist:
        stores.FOLLOWUPS.add_many(queue)
    return queue


__all__ = [
    "GAP_BREAKUP",
    "GAP_FOLLOWUP_1",
    "GAP_FOLLOWUP_2",
    "GAP_PAYMENT",
    "GAP_PROPOSAL",
    "build_followup_queue",
    "due_followups_for_prospect",
]
