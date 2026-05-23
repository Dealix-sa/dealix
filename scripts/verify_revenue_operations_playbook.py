#!/usr/bin/env python3
"""Verify the Revenue Operations Playbook artifacts are in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/revenue/REVENUE_OPERATIONS_PLAYBOOK.md",
    "docs/strategy/ICP_OPERATING_SYSTEM.md",
    "docs/acquisition/LEAD_SOURCING_SYSTEM.md",
    "docs/acquisition/LEAD_QUALIFICATION_SCORE.md",
    "docs/acquisition/OUTBOUND_CADENCE_SYSTEM.md",
    "docs/delivery/SAMPLE_OPERATIONS_SYSTEM.md",
    "docs/revenue/PROPOSAL_CONVERSION_SYSTEM.md",
    "docs/finance/PAYMENT_PATH_SYSTEM.md",
    "docs/learning/WIN_LOSS_SYSTEM.md",
]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        p = Path(rel)
        if not p.exists():
            failures.append(f"Missing: {rel}")
        elif p.stat().st_size < 30:
            failures.append(f"Too short: {rel}")
    if failures:
        print("Revenue Operations Playbook verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Revenue Operations Playbook is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
