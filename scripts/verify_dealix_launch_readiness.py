#!/usr/bin/env python3
"""Wave 5/7 gate — Dealix launch-readiness verification.

Aggregates the operating layer that has to exist before a Private Manual Launch:
governance approval gate, founder command docs, delivery rhythm, sales pack, the
revenue/growth seed data, and the customer-workspace tooling.

Prints a readiness score (0-100) and a band. Exits 0 if score >= PASS_THRESHOLD.
External-action safety: also asserts the pipeline seed contains no auto-sent
external events (non-negotiable #8).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PASS_THRESHOLD = 85

CHECKS: tuple[tuple[str, str], ...] = (
    # (label, repo-relative path)
    ("Governance: approval gate", "docs/governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"),
    ("Founder: revenue command center", "docs/founder/REVENUE_COMMAND_CENTER.md"),
    ("Founder: weekly CEO review", "docs/founder/WEEKLY_CEO_REVIEW.md"),
    ("Delivery: paid sprint handoff", "docs/delivery/PAID_SPRINT_HANDOFF.md"),
    ("Delivery: daily rhythm", "docs/delivery/DELIVERY_DAILY_RHYTHM.md"),
    ("Delivery: proof to upsell", "docs/delivery/PROOF_TO_UPSELL_PLAYBOOK.md"),
    ("Sales: first outreach pack", "sales/FIRST_OUTREACH_PACK.md"),
    ("Sales: diagnostic scorecard", "sales/DIAGNOSTIC_SCORECARD.md"),
    ("Sales: command sprint terms", "sales/COMMAND_SPRINT_TERMS.md"),
    ("Sales: managed business OS offer", "sales/MANAGED_BUSINESS_OS_OFFER.md"),
    ("Data: revenue pipeline seed", "data/revenue/pipeline.jsonl"),
    ("Data: proof assets seed", "data/revenue/proof_assets.jsonl"),
    ("Data: first 30 targets", "data/growth/first_30_targets.csv"),
    ("Tooling: customer workspace", "scripts/create_customer_workspace.py"),
    ("Tooling: founder daily command", "scripts/founder_daily_command.py"),
    ("Tooling: e2e dry run", "scripts/run_dealix_e2e_dry_run.py"),
)


def assert_no_auto_send() -> list[str]:
    """Non-negotiable #8 guard against the revenue seed."""
    problems: list[str] = []
    seed = REPO / "data/revenue/pipeline.jsonl"
    if not seed.is_file():
        return problems
    for i, line in enumerate(seed.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            problems.append(f"pipeline.jsonl line {i}: invalid JSON")
            continue
        status = str(rec.get("status", ""))
        decision = str(rec.get("governance_decision", ""))
        if status == "auto_sent" or decision == "auto_sent":
            problems.append(f"pipeline.jsonl line {i}: auto_sent external event (violates #8)")
    return problems


def main() -> int:
    print("== Dealix Launch Readiness Verification ==")
    present = 0
    for label, rel in CHECKS:
        ok = (REPO / rel).is_file()
        print(f"  {'ok ' if ok else 'MISS'}  {label:<36} {rel}")
        if ok:
            present += 1

    total = len(CHECKS)
    score = round(present / total * 100)

    print("\n[governance guard — non-negotiable #8]")
    guard_problems = assert_no_auto_send()
    if guard_problems:
        for p in guard_problems:
            print(f"  VIOLATION  {p}")
    else:
        print("  ok   no auto-sent external events in revenue seed")

    band = (
        "READY for Private Manual Launch"
        if score >= PASS_THRESHOLD and not guard_problems
        else "NOT READY"
    )
    print(f"\nReadiness score: {score}/100 ({present}/{total} checks)")
    print(f"RESULT: {band}")

    if score < PASS_THRESHOLD or guard_problems:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
