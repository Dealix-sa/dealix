"""Win/Loss learning — record outcomes and aggregate weekly lessons.

Records carry no PII beyond company/sector (which are business attributes, not
personal data). The weekly aggregation answers: which sector/channel/offer is
converting, what objections recur, and what to change next week.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.models import (
    Channel,
    Outcome,
    WinLoss,
    now_iso,
)


def record_outcome(
    *,
    prospect_id: str = "",
    company: str = "",
    sector: str = "",
    channel: str = Channel.EMAIL,
    offer_key: str = "",
    outcome: str = Outcome.OPEN,
    reason: str = "",
    objection: str = "",
    lesson: str = "",
    next_change: str = "",
) -> WinLoss:
    """Persist a win/loss/open record."""
    rec = WinLoss(
        record_id=f"wl_{uuid4().hex[:18]}",
        prospect_id=prospect_id,
        company=company,
        sector=sector,
        channel=channel,
        offer_key=offer_key,
        outcome=outcome,
        reason=reason,
        objection=objection,
        lesson=lesson,
        next_change=next_change,
        created_at=now_iso(),
    )
    return stores.WIN_LOSS.add(rec)


def _within(iso: str, *, window_days: int, now: datetime) -> bool:
    try:
        ts = datetime.fromisoformat(iso)
    except Exception:
        return False
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=UTC)
    return (now - ts).total_seconds() <= window_days * 86400.0


def _top(counter: Counter[str]) -> str:
    return counter.most_common(1)[0][0] if counter else "n/a"


def weekly_learning(
    records: Sequence[WinLoss] | None = None,
    *,
    window_days: int = 7,
    now: datetime | None = None,
) -> dict[str, object]:
    """Aggregate win/loss records into a learning summary (pure when records given)."""
    now = now or datetime.now(UTC)
    if records is None:
        records = [
            r
            for r in stores.WIN_LOSS.list(limit=100_000)
            if _within(r.created_at, window_days=window_days, now=now)
        ]
    won = [r for r in records if r.outcome == Outcome.WON]
    lost = [r for r in records if r.outcome == Outcome.LOST]
    decided = len(won) + len(lost)
    close_rate = (len(won) / decided) if decided else 0.0
    return {
        "window_days": window_days,
        "total": len(records),
        "won": len(won),
        "lost": len(lost),
        "open": sum(1 for r in records if r.outcome == Outcome.OPEN),
        "close_rate": round(close_rate, 3),
        "best_sector": _top(Counter(r.sector for r in won if r.sector)),
        "best_channel": _top(Counter(r.channel for r in won if r.channel)),
        "best_offer": _top(Counter(r.offer_key for r in won if r.offer_key)),
        "top_objections": [
            o for o, _ in Counter(r.objection for r in lost if r.objection).most_common(5)
        ],
        "lessons": [r.lesson for r in records if r.lesson][:10],
        "next_changes": [r.next_change for r in records if r.next_change][:10],
    }


__all__ = ["record_outcome", "weekly_learning"]
