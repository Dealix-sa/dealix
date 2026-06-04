#!/usr/bin/env python3
"""Validate the manual revenue events ledger (manual recording only).

Checks every event record for required fields, allowed event_type, allowed
pipeline stages, and unique event_id. This NEVER sends anything — it only
validates a human-maintained JSONL ledger.

Usage:
    python scripts/revenue_manual_events_validate.py [path]

Default path: data/revenue_manual_events.example.jsonl

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _v7_revenue_common import (
    DATA,
    MANUAL_EVENT_TYPES,
    PIPELINE_STAGES,
    read_jsonl,
)

REQUIRED_FIELDS = (
    "event_id",
    "created_at",
    "event_type",
    "company",
    "vertical",
    "source_draft_id",
    "channel",
    "amount_sar",
    "stage_before",
    "stage_after",
    "notes",
    "founder_initials",
)


def validate(path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not path.exists():
        return False, [f"ledger not found: {path}"]

    rows = read_jsonl(path)
    if not rows:
        return False, [f"ledger is empty: {path}"]

    seen_ids: set[str] = set()
    for i, row in enumerate(rows, start=1):
        for field in REQUIRED_FIELDS:
            if field not in row:
                errors.append(f"row {i}: missing field '{field}'")
        etype = row.get("event_type")
        if etype is not None and etype not in MANUAL_EVENT_TYPES:
            errors.append(f"row {i}: invalid event_type '{etype}'")
        for stage_key in ("stage_before", "stage_after"):
            stage = row.get(stage_key)
            if stage is not None and stage not in PIPELINE_STAGES:
                errors.append(f"row {i}: invalid {stage_key} '{stage}'")
        amount = row.get("amount_sar")
        if amount is not None and not isinstance(amount, (int, float)):
            errors.append(f"row {i}: amount_sar must be numeric")
        eid = row.get("event_id")
        if eid in seen_ids:
            errors.append(f"row {i}: duplicate event_id '{eid}'")
        if eid is not None:
            seen_ids.add(eid)

    return (not errors), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DATA / "revenue_manual_events.example.jsonl"),
    )
    args = parser.parse_args()
    ok, errors = validate(Path(args.path))
    if ok:
        print(f"[manual_events] PASS — {args.path} is valid (manual recording only).")
        return 0
    print(f"[manual_events] FAIL — {len(errors)} issue(s):")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
