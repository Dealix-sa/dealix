#!/usr/bin/env python3
"""Verify the Dealix Wave 6 Revenue Operating Rhythm is fully scaffolded.

The data/ ledgers hold runtime customer data and are gitignored by doctrine
(NEVER commit prospect/customer data). This gate therefore *bootstraps* the
empty runtime ledgers idempotently, then validates the committed structure.

Checks:
  1. Ensure the (gitignored) runtime ledgers exist — create empty if missing.
  2. Every tracked Wave 6 structure file exists (docs/sales/reports/scripts).
  3. Every *.jsonl ledger parses line-by-line (empty is OK).
  4. Doctrine guard-strings are present in the key docs (no auto-send,
     founder approval, no guaranteed revenue).
  5. The two generator scripts run --help without error.

Prints WAVE6_READY=true|false and MISSING_FILES=<n>; exit 0 on pass, 1 on fail.

Usage:
  python scripts/verify_wave6_revenue_rhythm.py

Reference: docs/05_founder/REVENUE_COMMAND_CENTER.md
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Gitignored runtime ledgers — bootstrapped empty if missing (hold customer data).
RUNTIME_JSONL: tuple[str, ...] = (
    "data/revenue/pipeline.jsonl",
    "data/revenue/outreach_queue.jsonl",
    "data/revenue/diagnostics.jsonl",
    "data/revenue/offers.jsonl",
    "data/revenue/payments.jsonl",
    "data/revenue/upsells.jsonl",
    "data/customers/customer_health.jsonl",
)
# Gitignored runtime CSV — bootstrapped with header only.
RUNTIME_CSV = "data/growth/first_30_targets.csv"
CSV_HEADER = (
    "company_name,website,city,sector,why_target,pain_hypothesis,evidence_url,"
    "recommended_angle,recommended_offer,outreach_status,next_action,owner,notes\n"
)

# Tracked structure — must be committed in the repo.
REQUIRED_FILES: tuple[str, ...] = (
    # docs
    "docs/05_founder/REVENUE_COMMAND_CENTER.md",
    "docs/05_founder/WEEKLY_CEO_REVIEW.md",
    "docs/06_growth/FIRST_30_TARGETS_PLAYBOOK.md",
    "docs/04_delivery/PAID_SPRINT_HANDOFF.md",
    "docs/04_delivery/DELIVERY_DAILY_RHYTHM.md",
    "docs/04_delivery/PROOF_TO_UPSELL_PLAYBOOK.md",
    "docs/04_delivery/CUSTOMER_SUCCESS_LITE_OS.md",
    # sales
    "sales/FIRST_OUTREACH_PACK.md",
    "sales/DIAGNOSTIC_SCRIPT.md",
    "sales/DIAGNOSTIC_SCORECARD.md",
    "sales/COMMAND_SPRINT_TERMS.md",
    "sales/PROPOSAL_TEMPLATE.md",
    "sales/MANAGED_BUSINESS_OS_OFFER.md",
    # reports
    "reports/revenue/daily_revenue_brief.md",
    "reports/revenue/outreach_approval_queue.md",
    "reports/revenue/diagnostic_brief_template.md",
    "reports/revenue/open_offers.md",
    "reports/revenue/upsell_opportunities.md",
    "reports/growth/first_30_targets_review.md",
    "reports/delivery/active_sprints.md",
    "reports/delivery/daily_delivery_brief.md",
    "reports/customers/customer_health_brief.md",
    # scripts
    "scripts/create_customer_workspace.py",
    "scripts/founder_daily_command.py",
)

# All jsonl ledgers (runtime) are validated for parseability.
JSONL_FILES: tuple[str, ...] = RUNTIME_JSONL


def bootstrap_runtime_ledgers() -> None:
    """Create the gitignored runtime ledgers empty if missing (idempotent)."""
    for rel in RUNTIME_JSONL:
        path = REPO_ROOT / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
    csv_path = REPO_ROOT / RUNTIME_CSV
    if not csv_path.exists():
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_path.write_text(CSV_HEADER, encoding="utf-8")

# file -> list of substrings that must all appear (doctrine guards)
DOCTRINE_GUARDS: dict[str, tuple[str, ...]] = {
    "docs/05_founder/REVENUE_COMMAND_CENTER.md": ("no auto-send", "founder approval", "no guaranteed revenue"),
    "sales/COMMAND_SPRINT_TERMS.md": ("founder approval", "ضمان إيراد"),
    "sales/MANAGED_BUSINESS_OS_OFFER.md": ("ضمان إيراد",),
    "reports/revenue/outreach_approval_queue.md": ("approval_status", "approved"),
}

GENERATOR_SCRIPTS: tuple[str, ...] = (
    "scripts/create_customer_workspace.py",
    "scripts/founder_daily_command.py",
)


def _missing(paths: tuple[str, ...]) -> list[str]:
    return [p for p in paths if not (REPO_ROOT / p).is_file()]


def _bad_jsonl() -> list[str]:
    bad: list[str] = []
    for rel in JSONL_FILES:
        path = REPO_ROOT / rel
        if not path.is_file():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError:
                bad.append(f"{rel}:{i}")
    return bad


def _missing_guards() -> list[str]:
    out: list[str] = []
    for rel, needles in DOCTRINE_GUARDS.items():
        path = REPO_ROOT / rel
        if not path.is_file():
            out.append(f"{rel} (file missing)")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                out.append(f"{rel} :: missing guard {needle!r}")
    return out


def _scripts_run() -> list[str]:
    failures: list[str] = []
    for rel in GENERATOR_SCRIPTS:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / rel), "--help"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False,
        )
        if proc.returncode != 0:
            failures.append(f"{rel} --help exit {proc.returncode}: {proc.stderr.strip()[:120]}")
    return failures


def main() -> int:
    ok = False  # definite binding before any use (satisfies static analysis)
    bootstrap_runtime_ledgers()
    missing_files = _missing(REQUIRED_FILES)
    bad_jsonl = _bad_jsonl()
    missing_guards = _missing_guards()
    script_failures = _scripts_run()

    ok = not (missing_files or bad_jsonl or missing_guards or script_failures)

    print(f"WAVE6_FILES_TOTAL={len(REQUIRED_FILES)}")
    print(f"MISSING_FILES={len(missing_files)}")
    for p in missing_files:
        print(f"  MISSING: {p}")
    print(f"BAD_JSONL={len(bad_jsonl)}")
    for p in bad_jsonl:
        print(f"  BAD_JSONL: {p}")
    print(f"MISSING_DOCTRINE_GUARDS={len(missing_guards)}")
    for p in missing_guards:
        print(f"  GUARD: {p}")
    print(f"SCRIPT_FAILURES={len(script_failures)}")
    for p in script_failures:
        print(f"  SCRIPT: {p}")
    print(f"WAVE6_READY={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
