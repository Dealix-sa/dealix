"""Evidence tracker CSV helpers (founder commercial ops)."""

from __future__ import annotations

import csv
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from dealix.commercial_ops.paths import EVIDENCE_TRACKER_CSV

PLACEHOLDER_COMPANY_PREFIXES = ("REPLACE:", "Example", "مثال")


def is_placeholder_evidence_row(row: dict[str, str]) -> bool:
    company = (row.get("company") or "").strip()
    if not company:
        return True
    for prefix in PLACEHOLDER_COMPANY_PREFIXES:
        if company.startswith(prefix):
            return True
    notes = (row.get("notes") or "").lower()
    return "training" in notes or "مثال تدريبي" in notes or "template_funnel_seed" in notes


def real_evidence_rows(rows: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    data = rows if rows is not None else load_evidence_rows()
    return [r for r in data if not is_placeholder_evidence_row(r)]


def load_evidence_rows(path: Path | None = None) -> list[dict[str, str]]:
    p = path or EVIDENCE_TRACKER_CSV
    if not p.is_file():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def count_evidence_events(
    rows: list[dict[str, str]] | None = None,
    *,
    on_date: date | None = None,
    since_days: int | None = None,
    exclude_placeholders: bool = False,
) -> dict[str, Any]:
    data = rows if rows is not None else load_evidence_rows()
    if exclude_placeholders:
        data = real_evidence_rows(data)
    today = on_date or datetime.now(UTC).date()
    week_start = today - timedelta(days=6)
    today_counts: Counter[str] = Counter()
    week_counts: Counter[str] = Counter()
    for row in data:
        et = (row.get("event_type") or "").strip()
        if not et:
            continue
        raw_date = (row.get("event_date") or "").strip()[:10]
        try:
            ed = date.fromisoformat(raw_date) if raw_date else None
        except ValueError:
            ed = None
        if ed == today:
            today_counts[et] += 1
        if ed is not None and week_start <= ed <= today:
            week_counts[et] += 1
    return {
        "date": today.isoformat(),
        "today_total": sum(today_counts.values()),
        "week_total": sum(week_counts.values()),
        "today_by_type": dict(today_counts),
        "week_by_type": dict(week_counts),
    }
