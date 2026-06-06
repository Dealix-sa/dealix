#!/usr/bin/env python3
"""Verify Dealix growth assets exist and are safe (no spam, no auto-send).

Dependency-free (stdlib only). Part of the Dealix launch gates.

PASS criteria:
  1. Self-Growth OS doc exists.
  2. Diagnostic script exists.
  3. First-30 targets CSV exists with the required columns and >= 10 rows.
  4. Outreach approval queue exists and asserts founder-approval / no-auto-send.

Exit 0 on PASS, non-zero on FAIL.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GROWTH_OS = ROOT / "docs/06_growth/SELF_GROWTH_OS.md"
DIAGNOSTIC = ROOT / "sales/DIAGNOSTIC_SCRIPT.md"
TARGETS = ROOT / "data/growth/first_30_targets.csv"
QUEUE = ROOT / "reports/revenue/outreach_approval_queue.md"

REQUIRED_CSV_COLS = {"company", "sector", "source", "consent_basis", "shortlist"}
SAFETY_PHRASES = ["founder approval", "no auto-send"]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"PASS: {msg}")


def main() -> int:
    print("== Dealix Growth Assets Verifier ==")
    failures = 0

    for label, path in [
        ("Self-Growth OS", GROWTH_OS),
        ("Diagnostic script", DIAGNOSTIC),
        ("Outreach approval queue", QUEUE),
    ]:
        if path.is_file():
            ok(f"{label} present ({path.relative_to(ROOT)})")
        else:
            fail(f"{label} missing ({path.relative_to(ROOT)})")
            failures += 1

    # Targets CSV.
    if not TARGETS.is_file():
        fail(f"First-30 targets CSV missing ({TARGETS.relative_to(ROOT)})")
        failures += 1
    else:
        with TARGETS.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            cols = {c.strip().lower() for c in (reader.fieldnames or [])}
            rows = list(reader)
        missing = REQUIRED_CSV_COLS - cols
        if missing:
            fail(f"targets CSV missing columns: {sorted(missing)}")
            failures += 1
        else:
            ok(f"targets CSV has required columns ({len(REQUIRED_CSV_COLS)})")
        if len(rows) >= 10:
            ok(f"targets CSV has {len(rows)} rows (>= 10)")
        else:
            fail(f"targets CSV has only {len(rows)} rows (need >= 10)")
            failures += 1
        # No scraped sources permitted.
        bad = [r for r in rows if "scrap" in (r.get("source", "").lower())]
        if bad:
            fail(f"{len(bad)} target rows have a 'scraped' source (forbidden)")
            failures += 1
        else:
            ok("no scraped sources in targets CSV")

    # Safety language in the outreach queue.
    if QUEUE.is_file():
        text = QUEUE.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in SAFETY_PHRASES:
            if phrase in text:
                ok(f"outreach queue asserts: {phrase!r}")
            else:
                fail(f"outreach queue missing safety assertion: {phrase!r}")
                failures += 1

    print()
    if failures:
        print(f"RESULT: FAIL ({failures} issue(s))")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
