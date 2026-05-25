#!/usr/bin/env python3
"""score_lead_batch.py — Assign A/B/C priority from fit_score in a batch CSV.

Rules:
    fit_score >= 80 -> A
    fit_score >= 70 -> B
    fit_score <  70 -> C

Rewrites the `priority` column in place. Pure stdlib.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def priority_for(score: int) -> str:
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    return "C"


def rescore(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        print(f"empty batch: {path}", file=sys.stderr)
        return 1
    changes = 0
    for row in rows:
        try:
            score = int(row.get("fit_score", "0") or 0)
        except ValueError:
            score = 0
        new_priority = priority_for(score)
        if row.get("priority") != new_priority:
            row["priority"] = new_priority
            changes += 1
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"rescored {len(rows)} rows ({changes} priority changes) in {path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to batch CSV.")
    args = parser.parse_args()
    return rescore(Path(args.file))


if __name__ == "__main__":
    sys.exit(main())
