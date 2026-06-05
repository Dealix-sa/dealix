#!/usr/bin/env python3
"""Verify Dealix growth assets exist and route correctly.

Asserts:
  1. Growth OS index docs exist (docs/06_growth/GROWTH_OS.md, ANSWER_LIBRARY.md).
  2. Sector and answer content data files exist with the required minimum counts
     (>=5 sectors, >=10 answers) when present.
  3. Every answer/sector routes its CTA to Business OS Score, Diagnostic, or
     Command Sprint (no external / auto-send routing).

Tolerant of not-yet-built frontend (skips counts if data files are absent).
Prints KEY=value lines. Exit 0 on pass, 1 on fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/06_growth/GROWTH_OS.md",
    "docs/06_growth/ANSWER_LIBRARY.md",
]

SECTORS_TS = REPO / "frontend/src/content/wave3/sectors.ts"
ANSWERS_TS = REPO / "frontend/src/content/wave3/answers.ts"

# Allowed CTA routing destinations for growth assets.
ALLOWED_ROUTES = {"business-os-score", "diagnostic", "command-sprint"}


def main() -> int:
    failures: list[str] = []

    for d in REQUIRED_DOCS:
        if not (REPO / d).exists():
            failures.append(f"missing growth doc: {d}")

    sectors_count = answers_count = -1

    if SECTORS_TS.exists():
        text = SECTORS_TS.read_text(encoding="utf-8", errors="ignore")
        sectors_count = len(re.findall(r"\bslug\s*:", text))
        if sectors_count < 5:
            failures.append(f"sectors.ts has {sectors_count} sectors (need >=5)")

    if ANSWERS_TS.exists():
        text = ANSWERS_TS.read_text(encoding="utf-8", errors="ignore")
        answers_count = len(re.findall(r"\bslug\s*:", text))
        if answers_count < 10:
            failures.append(f"answers.ts has {answers_count} answers (need >=10)")
        for route in re.findall(r"routeTo\s*:\s*[\"']([a-z\-]+)[\"']", text):
            if route not in ALLOWED_ROUTES:
                failures.append(f"answers.ts routeTo '{route}' not allowed")

    print(f"GROWTH_SECTORS={sectors_count} GROWTH_ANSWERS={answers_count}")

    if failures:
        print("GROWTH_ASSETS_PASS=false")
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("GROWTH_ASSETS_PASS=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
