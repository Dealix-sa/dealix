"""Win/Loss Learning — every outcome teaches the system.

Records outcomes (won / lost / no_response / nurture) with a reason + lesson,
then aggregates them into a weekly-style learning summary (by sector, channel,
reason) plus suggested next changes. No invented data — summaries are pure
counts over what was recorded.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from dealix.distribution.ledger import append_record, new_id, now_iso, read_records
from dealix.distribution.paths import WIN_LOSS_LEDGER
from dealix.distribution.schemas import assert_valid

VALID_OUTCOMES = {"won", "lost", "no_response", "nurture"}


def record_outcome(
    *,
    company: str,
    outcome: str,
    reason: str,
    sector: str = "",
    objection: str = "",
    offer: str = "",
    channel: str = "",
    lesson: str = "",
    ledger: Path | None = None,
) -> dict[str, Any]:
    """Append a validated win/loss record."""
    if outcome not in VALID_OUTCOMES:
        raise ValueError(f"outcome must be one of {sorted(VALID_OUTCOMES)}")
    rec: dict[str, Any] = {
        "id": new_id("wl"),
        "company": company,
        "sector": sector,
        "outcome": outcome,
        "reason": reason,
        "objection": objection,
        "offer": offer,
        "lesson": lesson,
        "created_at": now_iso(),
    }
    if channel:
        rec["channel"] = channel
    assert_valid(rec, "win_loss")
    return append_record(ledger or WIN_LOSS_LEDGER, rec)


def _suggest_changes(by_reason: Counter, by_outcome: Counter) -> list[str]:
    out: list[str] = []
    losses = by_outcome.get("lost", 0)
    no_resp = by_outcome.get("no_response", 0)
    if no_resp and no_resp >= losses:
        out.append("ردود قليلة: راجع زاوية الرسالة الأولى والقطاع المستهدف")
    top = [r for r, _ in by_reason.most_common(3) if r]
    for r in top:
        rl = r.lower()
        if "price" in rl or "سعر" in r:
            out.append("اعتراض السعر متكرر: قدّم Diagnostic أصغر كنقطة دخول قبل العرض الكبير")
        elif "trust" in rl or "ثقة" in r:
            out.append("ضعف الثقة: ابدأ بـ Proof Pack ومرجع قبل أي التزام")
        elif "timing" in rl or "توقيت" in r:
            out.append("التوقيت: ضعهم في nurture بمتابعة مجدولة بدل الإغلاق المبكر")
        elif "pain" in rl or "ألم" in r:
            out.append("لا ألم واضح: أعد تأهيل القطاع/الحساب قبل الصرف عليه")
    if not out:
        out.append("استمر: لا نمط خسارة واضح بعد — كبّر العينة قبل تغيير الاستراتيجية")
    # de-dup, keep order
    seen: set[str] = set()
    return [x for x in out if not (x in seen or seen.add(x))]


def learning_summary(
    records: list[dict[str, Any]] | None = None, *, ledger: Path | None = None
) -> dict[str, Any]:
    """Aggregate outcomes into a learning summary."""
    recs = records if records is not None else read_records(ledger or WIN_LOSS_LEDGER)
    by_outcome = Counter(str(r.get("outcome") or "") for r in recs)
    by_sector = Counter(str(r.get("sector") or "") for r in recs if r.get("sector"))
    by_channel = Counter(str(r.get("channel") or "") for r in recs if r.get("channel"))
    by_reason = Counter(str(r.get("reason") or "") for r in recs if r.get("reason"))
    won = by_outcome.get("won", 0)
    decided = won + by_outcome.get("lost", 0)
    win_rate = round(100 * won / decided, 1) if decided else None
    return {
        "total": len(recs),
        "by_outcome": dict(by_outcome),
        "by_sector": dict(by_sector),
        "by_channel": dict(by_channel),
        "top_reasons": by_reason.most_common(5),
        "win_rate_pct": win_rate,
        "lessons": [str(r.get("lesson")) for r in recs if r.get("lesson")][:10],
        "next_changes": _suggest_changes(by_reason, by_outcome),
    }


__all__ = ["VALID_OUTCOMES", "learning_summary", "record_outcome"]
