#!/usr/bin/env python3
"""Verify the Dealix marketing OS: docs, calendar seeds, and banned voice."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MARKETING_DOCS = [
    "docs/marketing/DEALIX_MARKETING_OS.md",
    "docs/marketing/CONTENT_CALENDAR_SYSTEM.md",
    "docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md",
    "docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md",
    "docs/marketing/COPYWRITING_RULES.md",
    "docs/marketing/BRAND_VOICE_EXAMPLES.md",
    "docs/marketing/EMAIL_OUTREACH_GUIDE.md",
    "docs/marketing/LINKEDIN_OUTREACH_GUIDE.md",
    "docs/marketing/PARTNER_OUTREACH_GUIDE.md",
]

SEED_CSVS = [
    "data/private_ops_seed/marketing/content_calendar.csv",
    "data/private_ops_seed/marketing/campaigns.csv",
    "data/private_ops_seed/marketing/content_ideas.csv",
]

PERFORMANCE_DOCS = [
    "docs/performance/PERFORMANCE_IMPROVEMENT_OS.md",
    "docs/performance/REVENUE_KPI_TREE.md",
    "docs/performance/CONVERSION_DIAGNOSTICS.md",
    "docs/performance/EXPERIMENT_BACKLOG.md",
    "docs/performance/LEARNING_LOOP.md",
]

BANNED = [
    r"guarantee[d]?\s+(revenue|sales|leads|results|pipeline|roi)",
    r"\d+x\s+(your|in)\s+(sales|revenue|pipeline|leads|growth)",
    r"fully\s+autonomous\s+(outbound|sales|sending|posting)",
    r"set\s+(it|and)\s+forget\s*(it)?",
]


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []
    for rel in MARKETING_DOCS + PERFORMANCE_DOCS + SEED_CSVS:
        p = REPO_ROOT / rel
        if not p.exists() or p.stat().st_size == 0:
            failures.append(f"missing: {rel}")
        else:
            passes.append(rel)

    for rel in MARKETING_DOCS + PERFORMANCE_DOCS:
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for pattern in BANNED:
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                snippet = text[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
                if "❌" in snippet or "Banned" in snippet or "banned" in snippet or "Forbidden" in snippet or "forbidden" in snippet.lower() or "```" in snippet or "regex" in snippet.lower():
                    continue
                failures.append(f"banned voice in {rel}: …{snippet}…")

    print("=== Dealix Marketing System Verifier ===")
    print(f"checks passed: {len(passes)}")
    if failures:
        for f in failures:
            print(f"  - {f}")
        print("\nVERDICT: FAIL")
        return 1
    print("\nVERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
