"""Verify Stage 1 (Revenue) scaffolding.

Checks:
- docs/revenue/ has 8 required files.
- OFFER_LADDER.md mentions the five rungs.
- PIPELINE_STAGES.md mentions all nine stages.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_REVENUE_FILES = [
    "OFFER_LADDER.md",
    "PIPELINE_STAGES.md",
    "PRICING_AND_PACKAGING.md",
    "INVOICE_FLOW.md",
    "PAYMENT_RECONCILIATION.md",
    "REVENUE_READINESS.md",
    "REVENUE_COMMAND_CENTER.md",
    "REVENUE_CONTROL_SYSTEM.md",
]

# OFFER_LADDER must reference all five rungs (rung labels we expect)
RUNG_KEYWORDS = [
    ["Free Diagnostic", "Diagnostic"],
    ["Revenue Sprint", "Sprint"],
    ["Data Pack", "Managed Retainer", "Managed"],
    ["Managed Ops", "Embedded Ops", "Retainer"],
    ["Custom AI", "Strategic Partnership", "Custom"],
]

# PIPELINE_STAGES must reference all nine stages by keyword
PIPELINE_KEYWORDS = [
    ["Lead", "Sourced"],
    ["DM", "Qualified", "Reached"],
    ["Reply", "Responded"],
    ["Sample", "Sampled"],
    ["Proposal", "Proposed"],
    ["Payment", "PO", "Negotiating", "Negotiation"],
    ["Delivery", "Delivered", "Closed Won", "Closed-Won"],
    ["Feedback", "Handoff", "Hand-off", "Retro"],
    ["Retainer", "Renewal", "Expansion"],
]


def check_files() -> tuple[bool, list[str]]:
    base = REPO_ROOT / "docs" / "revenue"
    missing = [f for f in REQUIRED_REVENUE_FILES if not (base / f).exists()]
    return (not missing, missing)


def check_offer_ladder() -> tuple[bool, list[int]]:
    p = REPO_ROOT / "docs" / "revenue" / "OFFER_LADDER.md"
    if not p.exists():
        return False, list(range(1, 6))
    text = p.read_text(encoding="utf-8")
    missing: list[int] = []
    for i, keywords in enumerate(RUNG_KEYWORDS, start=1):
        if not any(k in text for k in keywords):
            missing.append(i)
    return (not missing, missing)


def check_pipeline_stages() -> tuple[bool, list[int]]:
    p = REPO_ROOT / "docs" / "revenue" / "PIPELINE_STAGES.md"
    if not p.exists():
        return False, list(range(1, 10))
    text = p.read_text(encoding="utf-8")
    missing: list[int] = []
    for i, keywords in enumerate(PIPELINE_KEYWORDS, start=1):
        if not any(k in text for k in keywords):
            missing.append(i)
    return (not missing, missing)


def main() -> int:
    failures: list[str] = []

    ok, missing = check_files()
    if ok:
        print(f"PASS docs/revenue/ — all {len(REQUIRED_REVENUE_FILES)} files present")
    else:
        print(f"FAIL docs/revenue/ — missing: {missing}")
        failures.append("revenue_files")

    ok, missing_rungs = check_offer_ladder()
    if ok:
        print("PASS OFFER_LADDER.md — five rungs present")
    else:
        print(f"FAIL OFFER_LADDER.md — missing rungs: {missing_rungs}")
        failures.append("offer_ladder")

    ok, missing_stages = check_pipeline_stages()
    if ok:
        print("PASS PIPELINE_STAGES.md — nine stages present")
    else:
        print(f"FAIL PIPELINE_STAGES.md — missing stages: {missing_stages}")
        failures.append("pipeline_stages")

    if failures:
        print(f"\nverify_tier1_revenue: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_tier1_revenue: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
