"""Follow-up Engine — surfaces who the founder should re-contact today.

Pure scheduling: it reads prospects' ``last_contact`` + ``status`` and emits
``due`` follow-up records. It never sends — it reminds. ``today`` is injectable
so the logic is deterministic and unit-testable.

Cadence:
  - ``new`` with no ``last_contact``          → first touch, priority high
  - ``contacted`` / ``qualified`` / ``proposal`` → due after DUE_AFTER_DAYS
  - ``nurture``                                → due after NURTURE_AFTER_DAYS
  - ``won`` / ``lost``                          → never due
Priority by overdue age: ≥14d high · 7–13d medium · else low.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from dealix.distribution.ledger import (
    append_record,
    new_id,
    now_iso,
    read_records,
    update_status,
)
from dealix.distribution.paths import FOLLOWUPS_LEDGER
from dealix.distribution.prospects import load_prospects

DUE_AFTER_DAYS = 4
NURTURE_AFTER_DAYS = 30
ACTIVE_STATUSES = {"contacted", "qualified", "proposal"}


def _parse_date(value: Any) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _priority(days: int) -> str:
    if days >= 14:
        return "high"
    if days >= 7:
        return "medium"
    return "low"


def compute_due(
    prospects: list[dict[str, Any]],
    *,
    today: date | None = None,
) -> list[dict[str, Any]]:
    """Return due follow-up records (not yet persisted)."""
    day = today or datetime.now(UTC).date()
    out: list[dict[str, Any]] = []
    for pr in prospects:
        status = str(pr.get("status") or "new")
        if status in ("won", "lost"):
            continue
        last = _parse_date(pr.get("last_contact"))
        base = {
            "id": new_id("followup"),
            "prospect_id": str(pr.get("id") or ""),
            "company": str(pr.get("company") or ""),
            "sector": str(pr.get("sector") or ""),
            "channel": str(pr.get("channel") or "email"),
            "last_contact": pr.get("last_contact"),
            "status": "due",
            "created_at": now_iso(),
        }
        if last is None and status == "new":
            out.append(
                {
                    **base,
                    "due_date": day.isoformat(),
                    "days_since_contact": None,
                    "priority": "high",
                    "reason": "first_touch",
                }
            )
            continue
        if last is None:
            continue
        days = (day - last).days
        threshold = NURTURE_AFTER_DAYS if status == "nurture" else DUE_AFTER_DAYS
        if status not in ACTIVE_STATUSES and status != "nurture":
            continue
        if days < threshold:
            continue
        out.append(
            {
                **base,
                "due_date": (day).isoformat(),
                "days_since_contact": days,
                "priority": _priority(days),
                "reason": f"no_contact_{days}d",
            }
        )
    out.sort(key=lambda f: (f["priority"] != "high", f["priority"] != "medium"))
    return out


def run_generation(
    prospects_path: Path | None = None,
    *,
    today: date | None = None,
    ledger: Path | None = None,
) -> dict[str, Any]:
    """Compute due follow-ups and append new ones (dedupe per open prospect)."""
    led = ledger or FOLLOWUPS_LEDGER
    prospects = load_prospects(prospects_path)
    existing = read_records(led)
    open_pids = {str(f.get("prospect_id")) for f in existing if f.get("status") == "due"}
    due = compute_due(prospects, today=today)
    new_items = [f for f in due if str(f.get("prospect_id")) not in open_pids]
    for f in new_items:
        append_record(led, f)
    return {
        "prospects": len(prospects),
        "due_total": len(due),
        "new_followups": len(new_items),
        "already_open": len(due) - len(new_items),
        "by_priority": {
            p: sum(1 for f in due if f["priority"] == p) for p in ("high", "medium", "low")
        },
    }


def complete_followup(followup_id: str, ledger: Path | None = None) -> dict[str, Any] | None:
    return update_status(ledger or FOLLOWUPS_LEDGER, followup_id, "completed")


def due_followups(ledger: Path | None = None) -> list[dict[str, Any]]:
    return [f for f in read_records(ledger or FOLLOWUPS_LEDGER) if f.get("status") == "due"]


__all__ = [
    "DUE_AFTER_DAYS",
    "NURTURE_AFTER_DAYS",
    "complete_followup",
    "compute_due",
    "due_followups",
    "run_generation",
]
