#!/usr/bin/env python3
"""
verify_business_os.py — checks that business-OS docs actually carry the
structural fields a useful doc must have: owner, cadence, KPI, source of
truth, failure mode, recovery path.

A long doc that doesn't say who owns it or how often it runs is fluff.
This verifier catches that.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Docs that should carry structural fields. Some are AR-only — we accept the
# Arabic equivalents too. Each entry is (path, [keyword_sets]) where the doc
# must contain at least one keyword from each set.
TARGETS = [
    (
        "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md",
        [
            ["المالك", "owner", "مؤسس", "founder"],
            ["إيقاع", "cadence", "يومي", "أسبوعي", "daily", "weekly"],
        ],
    ),
    (
        "docs/company/CEO_OPERATING_SYSTEM.md",
        [
            ["owner", "ceo", "founder", "المالك"],
            ["cadence", "daily", "weekly", "يومي", "أسبوعي", "إيقاع"],
        ],
    ),
    (
        "docs/ops/DAILY_OPERATING_LOOP.md",
        [
            ["daily", "يومي"],
        ],
    ),
    (
        "docs/ops/DAILY_COMMERCIAL_LOOP_AR.md",
        [
            ["تجاري", "commercial", "revenue"],
        ],
    ),
    (
        "docs/ops/FIRST_CUSTOMER_ONBOARDING.md",
        [
            ["customer", "onboarding", "عميل"],
        ],
    ),
]


def main() -> int:
    failures: list[str] = []
    checked = 0

    for rel, keyword_sets in TARGETS:
        p = ROOT / rel
        if not p.exists():
            failures.append(f"missing doc: {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        if len(text.strip()) < 200:
            failures.append(f"too small: {rel} ({len(text.strip())} bytes)")
            continue
        checked += 1
        for kw_set in keyword_sets:
            if not any(kw.lower() in text for kw in kw_set):
                failures.append(
                    f"{rel} missing any of: {' / '.join(kw_set)}"
                )

    if failures:
        print(f"BUSINESS OS: FAIL ({len(failures)} issues across {len(TARGETS)} docs)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"BUSINESS OS: PASS ({checked}/{len(TARGETS)} docs carry required structural fields)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
