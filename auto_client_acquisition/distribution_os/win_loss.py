"""Win/Loss Learning — record every outcome + the weekly learning questions."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso


class Outcome(StrEnum):
    WON = "won"
    LOST = "lost"
    NO_DECISION = "no_decision"


# The weekly learning questions (plan section 13).
WEEKLY_QUESTIONS: tuple[str, ...] = (
    "أفضل قطاع؟ / Best sector?",
    "أفضل رسالة؟ / Best message?",
    "أفضل قناة؟ / Best channel?",
    "أكثر اعتراض؟ / Most common objection?",
    "أين نخسر؟ / Where do we lose?",
    "هل السعر غلط؟ / Is the price wrong?",
    "هل الشخص غلط؟ / Is it the wrong person?",
    "هل proof ناقص؟ / Is proof missing?",
    "وش نغير الأسبوع القادم؟ / What do we change next week?",
)


@dataclass
class WinLoss:
    id: str = field(default_factory=lambda: f"wl_{uuid4().hex[:12]}")
    company: str = ""
    sector: str = ""
    offer: str = ""  # catalog product id or name
    channel: str = ""
    outcome: str = Outcome.NO_DECISION.value
    reason: str = ""
    objection: str = ""
    lesson: str = ""
    next_change: str = ""
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(env_var="DEALIX_WIN_LOSS_PATH", default_rel="var/win_loss.jsonl", id_field="id")


def record(
    *,
    company: str,
    sector: str = "",
    offer: str = "",
    channel: str = "",
    outcome: str | Outcome = Outcome.NO_DECISION,
    reason: str = "",
    objection: str = "",
    lesson: str = "",
    next_change: str = "",
) -> WinLoss:
    value = outcome.value if isinstance(outcome, Outcome) else str(outcome)
    if value not in {o.value for o in Outcome}:
        raise ValueError(f"invalid_outcome:{value}")
    entry = WinLoss(
        company=company,
        sector=sector,
        offer=offer,
        channel=channel,
        outcome=value,
        reason=reason,
        objection=objection,
        lesson=lesson,
        next_change=next_change,
    )
    _store.append(entry.to_dict())
    return entry


def list_entries(*, outcome: str | None = None, sector: str | None = None) -> list[WinLoss]:
    def _match(rec: dict[str, Any]) -> bool:
        return (outcome is None or rec.get("outcome") == outcome) and (
            sector is None or rec.get("sector") == sector
        )

    return [WinLoss(**rec) for rec in _store.list(predicate=_match)]


def summarize() -> dict[str, Any]:
    """Aggregate wins/losses by sector, channel, and top objections."""
    entries = list_entries()
    by_outcome: dict[str, int] = {}
    by_sector_won: dict[str, int] = {}
    objections: dict[str, int] = {}
    for e in entries:
        by_outcome[e.outcome] = by_outcome.get(e.outcome, 0) + 1
        if e.outcome == Outcome.WON.value and e.sector:
            by_sector_won[e.sector] = by_sector_won.get(e.sector, 0) + 1
        if e.objection:
            objections[e.objection] = objections.get(e.objection, 0) + 1
    wins = by_outcome.get(Outcome.WON.value, 0)
    losses = by_outcome.get(Outcome.LOST.value, 0)
    decided = wins + losses
    return {
        "total": len(entries),
        "by_outcome": by_outcome,
        "win_rate": round(wins / decided, 3) if decided else 0.0,
        "best_sector": max(by_sector_won, key=by_sector_won.get) if by_sector_won else "",
        "top_objection": max(objections, key=objections.get) if objections else "",
    }


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "WEEKLY_QUESTIONS",
    "Outcome",
    "WinLoss",
    "clear_for_test",
    "list_entries",
    "record",
    "summarize",
]
