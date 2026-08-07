"""Generate a Daily Decision record for the Company Brain OS.

Every decision produced must include all required fields:

    decision, why_now, assumption, confidence, owner, next_action,
    success_metric, review_date, risk_if_delayed

Decisions are appended to ``ledgers/decisions_log.csv`` and returned to the
caller. The confidence field is one of: low, medium, high. No decision claims
guaranteed outcomes.
"""
from __future__ import annotations

import csv
import os
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from scripts.brain import DECISION_REQUIRED_FIELDS

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER_PATH = os.path.join(REPO_ROOT, "ledgers", "decisions_log.csv")

CONFIDENCE_LEVELS = ("low", "medium", "high")

# CSV header order (id + required fields).
FIELDNAMES = ["id", "date"] + list(DECISION_REQUIRED_FIELDS)


def generate_daily_decision(
    decision: str,
    why_now: str,
    assumption: str,
    confidence: str,
    owner: str,
    next_action: str,
    success_metric: str,
    review_date: str,
    risk_if_delayed: str,
    ledger_path: str | None = None,
) -> dict[str, Any]:
    """Create, validate, and log a decision record.

    Raises ``ValueError`` if any required field is empty or if confidence is
    invalid.
    """
    if confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"confidence must be one of {CONFIDENCE_LEVELS}, got {confidence}")

    record: dict[str, Any] = {
        "id": f"DEC-{uuid.uuid4().hex[:8].upper()}",
        "date": datetime.now(UTC).date().isoformat(),
        "decision": decision,
        "why_now": why_now,
        "assumption": assumption,
        "confidence": confidence,
        "owner": owner,
        "next_action": next_action,
        "success_metric": success_metric,
        "review_date": review_date,
        "risk_if_delayed": risk_if_delayed,
    }

    # Validate every required field is present and non-empty.
    for field in DECISION_REQUIRED_FIELDS:
        val = record.get(field)
        if not val or not str(val).strip():
            raise ValueError(f"decision missing required field '{field}'")

    _append_decision(record, ledger_path or LEDGER_PATH)
    return record


def _append_decision(record: dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_header = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow({k: record.get(k, "") for k in FIELDNAMES})


def default_review_date(days: int = 14) -> str:
    """Return an ISO date string ``days`` from today — useful for review_date."""
    return (datetime.now(UTC).date() + timedelta(days=days)).isoformat()


if __name__ == "__main__":
    import json

    rec = generate_daily_decision(
        decision="Pilot a weekly decision review with the founding team.",
        why_now="Decision backlog is growing and several items are past review date.",
        assumption="Founders will attend a 30-minute review weekly.",
        confidence="medium",
        owner="CEO",
        next_action="Schedule recurring 30-min slot and share decisions log.",
        success_metric=">=80% of decisions reviewed within their review_date window.",
        review_date=default_review_date(14),
        risk_if_delayed="Unreviewed decisions accumulate; assumptions go stale and compound risk.",
    )
    print(json.dumps(rec, indent=2))
