#!/usr/bin/env python3
"""Wave 4 gate — Dealix growth-asset verification.

Confirms the growth operating assets (playbooks + the first target list) are
present and that the target list is real (>= 30 rows, expected columns).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = (
    "docs/growth/GROWTH_MACHINE.md",
    "docs/growth/DAILY_OUTREACH_PLAN.md",
    "docs/growth/LEAD_SCORING_RULES.md",
    "docs/growth/PROOF_TO_UPSELL_MAP.md",
)

TARGETS_CSV = "data/growth/first_30_targets.csv"
EXPECTED_COLUMNS = {
    "target_id",
    "sector",
    "warm_path",
    "priority",
    "suggested_offer",
}
MIN_TARGETS = 30


def main() -> int:
    print("== Dealix Growth Assets Verification ==")
    failures: list[str] = []

    print("\n[growth playbooks]")
    for rel in REQUIRED_DOCS:
        ok = (REPO / rel).is_file()
        print(f"  {'ok ' if ok else 'MISS'}  {rel}")
        if not ok:
            failures.append(f"missing {rel}")

    print("\n[first target list]")
    csv_path = REPO / TARGETS_CSV
    if not csv_path.is_file():
        failures.append(f"missing {TARGETS_CSV}")
        print(f"  MISS  {TARGETS_CSV}")
    else:
        with csv_path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            cols = set(reader.fieldnames or [])
            rows = list(reader)
        missing_cols = EXPECTED_COLUMNS - cols
        if missing_cols:
            failures.append(f"{TARGETS_CSV} missing columns: {sorted(missing_cols)}")
            print(f"  FAIL  columns missing: {sorted(missing_cols)}")
        if len(rows) < MIN_TARGETS:
            failures.append(f"{TARGETS_CSV} has {len(rows)} rows (< {MIN_TARGETS})")
            print(f"  FAIL  only {len(rows)} targets (need >= {MIN_TARGETS})")
        else:
            print(f"  ok   {len(rows)} targets, columns present")

    if failures:
        print("\nRESULT: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\nRESULT: PASS — growth assets present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
