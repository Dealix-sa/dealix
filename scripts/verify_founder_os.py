#!/usr/bin/env python3
"""verify_founder_os.py — Founder Command OS structural checks."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "docs/founder/CEO_OPERATING_SYSTEM.md",
    "docs/founder/DAILY_COMMAND_BRIEF.md",
    "docs/founder/WEEKLY_CEO_REVIEW.md",
    "docs/founder/DECISION_LOG.md",
    "docs/founder/FOCUS_POLICY.md",
    "docs/founder/RISK_REGISTER.md",
    "docs/founder/KILL_DEFER_BUILD_RULES.md",
    "docs/founder/BOARD_MEMO_TEMPLATE.md",
]

REQUIRED_SECTIONS = {
    "docs/founder/DAILY_COMMAND_BRIEF.md": [
        "## 1. Money",
        "## 2. Pipeline",
        "## 3. Delivery",
        "## 4. Trust",
        "## 5. CEO Decisions",
        "## 6. One Focus Today",
    ],
    "docs/founder/WEEKLY_CEO_REVIEW.md": [
        "## Revenue",
        "## GTM",
        "## Delivery",
        "## Product",
        "## Trust",
        "## Learning",
        "## CEO Decision This Week",
    ],
    "docs/founder/RISK_REGISTER.md": [
        "## Format",
        "## Current Risks",
    ],
}


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).exists():
            failures.append(f"missing file: {rel}")

    for rel, sections in REQUIRED_SECTIONS.items():
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for section in sections:
            if section not in text:
                failures.append(f"{rel}: missing section header '{section}'")

    if failures:
        print("Founder OS verification FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Founder OS verification OK ({len(REQUIRED_FILES)} files, "
          f"{sum(len(v) for v in REQUIRED_SECTIONS.values())} sections checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
