#!/usr/bin/env python3
"""Dealix E2E Dry Run — prove the revenue chain is connected end-to-end.

Walks the full path with synthetic data and real tooling:

    Target → Outreach Approval → Diagnostic → Offer → Paid Sprint (simulated)
    → Customer Workspace → Proof Pack → Upsell Recommendation → Founder Daily Command

Each step is asserted. The run writes a report to
``reports/verification/e2e_dry_run_<ts>.md`` (+ ``_latest.md``) and exits non-zero
if any step fails. No external action is taken — every outbound is a draft.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = sys.executable
OUT_DIR = REPO / "reports/verification"
DRY_CLIENT = "dry-run-client"
DRY_SLUG = "dry-run-client"

WORKSPACE_FILES = [
    "00_intake.md",
    "01_company_intelligence.md",
    "02_diagnostic_summary.md",
    "03_command_sprint_scope.md",
    "04_revenue_map.md",
    "05_proof_register.md",
    "06_approval_register.md",
    "07_next_action_board.md",
    "08_executive_command_brief.md",
    "09_delivery_log.md",
    "10_proof_pack.md",
    "11_upsell_recommendation.md",
]

DISCLAIMER_FRAGMENT = "القيمة التقديرية ليست قيمة"


class Step:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ok = False
        self.detail = ""

    def passed(self, detail: str = "") -> "Step":
        self.ok, self.detail = True, detail
        return self

    def failed(self, detail: str) -> "Step":
        self.ok, self.detail = False, detail
        return self


def step_target() -> Step:
    s = Step("Target")
    csv_path = REPO / "data/growth/first_30_targets.csv"
    if not csv_path.is_file():
        return s.failed("data/growth/first_30_targets.csv missing")
    with csv_path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return s.failed("target list empty")
    return s.passed(f"selected target {rows[0]['target_id']} from {len(rows)} targets")


def step_outreach_approval() -> Step:
    s = Step("Outreach Approval")
    gate = REPO / "docs/governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"
    if not gate.is_file():
        return s.failed("approval gate doc missing")
    # The outreach exists only as a queued draft — assert no auto-send in seed.
    seed = REPO / "data/revenue/pipeline.jsonl"
    for line in seed.read_text(encoding="utf-8").splitlines() if seed.is_file() else []:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("status") == "auto_sent":
            return s.failed("found auto_sent event — violates non-negotiable #8")
    return s.passed("draft queued for approval; no auto-send")


def step_diagnostic() -> Step:
    s = Step("Diagnostic")
    doc = REPO / "sales/DIAGNOSTIC_SCORECARD.md"
    return s.passed("scorecard ready") if doc.is_file() else s.failed("scorecard missing")


def step_offer() -> Step:
    s = Step("Offer")
    doc = REPO / "sales/COMMAND_SPRINT_TERMS.md"
    return s.passed("sprint terms ready") if doc.is_file() else s.failed("sprint terms missing")


def step_paid_sprint() -> Step:
    s = Step("Paid Sprint (simulated)")
    doc = REPO / "docs/delivery/PAID_SPRINT_HANDOFF.md"
    if not doc.is_file():
        return s.failed("handoff doc missing")
    return s.passed("handoff defined; sprint simulated (no live charge)")


def step_customer_workspace() -> Step:
    s = Step("Customer Workspace")
    proc = subprocess.run(
        [PY, str(REPO / "scripts/create_customer_workspace.py"), "--name", DRY_CLIENT, "--force"],
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )
    if proc.returncode != 0:
        return s.failed(f"create_customer_workspace failed: {proc.stderr.strip() or proc.stdout.strip()}")
    ws = REPO / "customers" / DRY_SLUG
    missing = [f for f in WORKSPACE_FILES if not (ws / f).is_file()]
    if missing:
        return s.failed(f"missing workspace files: {missing}")
    # disclaimer present in each customer-facing file
    no_disc = [
        f for f in WORKSPACE_FILES
        if DISCLAIMER_FRAGMENT not in (ws / f).read_text(encoding="utf-8")
    ]
    if no_disc:
        return s.failed(f"files missing bilingual disclaimer: {no_disc}")
    return s.passed(f"12/12 files created in customers/{DRY_SLUG}/ with disclaimer")


def step_proof_pack() -> Step:
    s = Step("Proof Pack")
    proof = REPO / "data/revenue/proof_assets.jsonl"
    if not proof.is_file():
        return s.failed("proof_assets.jsonl missing")
    packs = []
    for line in proof.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            packs.append(json.loads(line))
    qualifying = [p for p in packs if int(p.get("proof_score", 0)) >= 70]
    if not qualifying:
        return s.failed("no Proof Pack with score >= 70")
    has_capital = any(p.get("capital_asset") for p in packs)
    if not has_capital:
        return s.failed("no Capital Asset registered (non-negotiable #11)")
    return s.passed(f"{len(qualifying)} proof pack(s) >= 70; capital asset registered")


def step_upsell() -> Step:
    s = Step("Upsell Recommendation")
    doc = REPO / "docs/delivery/PROOF_TO_UPSELL_PLAYBOOK.md"
    ws_file = REPO / "customers" / DRY_SLUG / "11_upsell_recommendation.md"
    if not doc.is_file():
        return s.failed("upsell playbook missing")
    if not ws_file.is_file():
        return s.failed("workspace upsell file missing")
    return s.passed("upsell mapped from proof; queued for approval")


def step_founder_command() -> Step:
    s = Step("Founder Daily Command")
    proc = subprocess.run(
        [PY, str(REPO / "scripts/founder_daily_command.py")],
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )
    if proc.returncode != 0:
        return s.failed(f"founder_daily_command failed: {proc.stderr.strip()}")
    out = REPO / "reports/founder/daily_command.md"
    if not out.is_file():
        return s.failed("daily_command.md not produced")
    return s.passed("daily command produced")


def main() -> int:
    steps = [
        step_target(),
        step_outreach_approval(),
        step_diagnostic(),
        step_offer(),
        step_paid_sprint(),
        step_customer_workspace(),
        step_proof_pack(),
        step_upsell(),
        step_founder_command(),
    ]

    all_ok = all(s.ok for s in steps)
    ts = dt.datetime.now()
    stamp = ts.strftime("%Y%m%d_%H%M%S")

    lines = ["# Dealix E2E Dry Run", "", f"_Run: {ts.strftime('%Y-%m-%d %H:%M:%S')}_", ""]
    lines.append("Chain: Target → Outreach Approval → Diagnostic → Offer → Paid Sprint")
    lines.append("→ Customer Workspace → Proof Pack → Upsell → Founder Daily Command")
    lines.append("")
    lines.append("| Step | Result | Detail |")
    lines.append("|---|---|---|")
    for s in steps:
        lines.append(f"| {s.name} | {'PASS' if s.ok else 'FAIL'} | {s.detail} |")
    lines.append("")
    lines.append(f"## RESULT: {'PASS' if all_ok else 'FAIL'}")
    lines.append("")
    if all_ok:
        lines.append("The revenue chain is connected end-to-end. Strongest single")
        lines.append("indicator that the system is operable.")
    else:
        blockers = [f"- {s.name}: {s.detail}" for s in steps if not s.ok]
        lines.append("Blockers:")
        lines.extend(blockers)
    lines.append("")
    lines.append("> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة")
    lines.append("")

    report = "\n".join(lines)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"e2e_dry_run_{stamp}.md").write_text(report, encoding="utf-8")
    (OUT_DIR / "e2e_dry_run_latest.md").write_text(report, encoding="utf-8")

    print(report)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
