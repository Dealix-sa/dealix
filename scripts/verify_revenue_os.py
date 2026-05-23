#!/usr/bin/env python3
"""verify_revenue_os.py — Revenue OS structural + funnel-consistency checks."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "docs/revenue/REVENUE_MODEL.md",
    "docs/revenue/SALES_FUNNEL.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/OUTBOUND_POLICY.md",
    "docs/revenue/QUALIFICATION_RULES.md",
    "docs/revenue/PROPOSAL_RULES.md",
    "docs/revenue/CLOSING_PLAYBOOK.md",
    "docs/revenue/REVENUE_METRICS.md",
]

# Canonical funnel stages — used by SALES_FUNNEL.md and PIPELINE_STAGES.md.
CANONICAL_STAGES = [
    "lead",
    "qualified",
    "contacted",
    "replied",
    "sample",  # "sample_sent" appears as both `Sample Sent` and `sample_sent`
    "call",  # "call_booked"
    "proposal",  # "proposal_sent"
    "paid",
    "delivered",
    "retainer",
]

# Canonical rung names.
CANONICAL_RUNGS = [
    "Free Diagnostic",
    "Revenue Sprint",
    "Data Pack",
    "Managed Ops",
    "Custom AI",
]


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).exists():
            failures.append(f"missing file: {rel}")
            continue

    funnel_path = REPO_ROOT / "docs/revenue/SALES_FUNNEL.md"
    if funnel_path.exists():
        text = funnel_path.read_text(encoding="utf-8").lower()
        for stage in CANONICAL_STAGES:
            if stage not in text:
                failures.append(f"SALES_FUNNEL.md missing canonical stage: {stage}")

    ladder_path = REPO_ROOT / "docs/revenue/OFFER_LADDER.md"
    if ladder_path.exists():
        text = ladder_path.read_text(encoding="utf-8")
        for rung in CANONICAL_RUNGS:
            if rung not in text:
                failures.append(f"OFFER_LADDER.md missing canonical rung: {rung}")

    if failures:
        print("Revenue OS verification FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("Revenue OS verification OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
