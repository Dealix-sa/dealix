#!/usr/bin/env python3
"""Soft launch revenue motion — meetings tracker + evidence cadence."""

from __future__ import annotations

import csv
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "docs/commercial/operations/soft_launch_meetings_tracker.yaml"
EVIDENCE = ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
GOAL_MIN = 3


def main() -> int:
    failures: list[str] = []
    scheduled = 0
    if TRACKER.is_file():
        data = yaml.safe_load(TRACKER.read_text(encoding="utf-8")) or {}
        meetings = data.get("meetings") or []
        scheduled = sum(
            1
            for m in meetings
            if str(m.get("status", "")).lower() in {"scheduled", "done", "completed"}
        )
    else:
        failures.append("missing soft_launch_meetings_tracker.yaml")

    evidence_7d = 0
    if EVIDENCE.is_file():
        cutoff = datetime.now(UTC) - timedelta(days=7)
        with EVIDENCE.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                raw = (row.get("date") or "")[:10]
                if not raw:
                    continue
                try:
                    dt = datetime.strptime(raw, "%Y-%m-%d").replace(tzinfo=UTC)
                    if dt >= cutoff:
                        evidence_7d += 1
                except ValueError:
                    pass

    print("== soft launch motion ==")
    print(f"  scheduled meetings: {scheduled}")
    print(f"  evidence (7d): {evidence_7d}")

    if scheduled < GOAL_MIN:
        failures.append(f"meetings {scheduled} < {GOAL_MIN}")
    if evidence_7d < 1:
        failures.append("no evidence in 7d — founder_evening -Append")

    if failures:
        print("SOFT_LAUNCH_MOTION=WARN")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("SOFT_LAUNCH_MOTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
