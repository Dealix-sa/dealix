"""Dealix private-ops audit template.

Copy this file to the root of your **private** ops repo (e.g.
`dealix-ops-private/audit_private_ops.py`) and run it from there. It checks:

1. Required files / directories exist.
2. Pipeline tracker has >= 25 leads (market evidence).
3. Revenue action log has >= 1 action and ideally >= 25 DMs.
4. Optional verifier scripts that live next to it.

This file lives in the **public** repo as a template only. It contains no
customer data, no contact information, no secrets, and no revenue figures.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

REQUIRED: tuple[str, ...] = (
    "founder/daily_brief.md",
    "founder/decision_queue.md",
    "founder/approvals_waiting.md",
    "sprint/current_sprint.md",
    "sprint/sprint_scorecard.csv",
    "stage/current_stage.md",
    "stage/stage_exit_checklist.csv",
    "stage/evidence_report.md",
    "pipeline/pipeline_tracker.csv",
    "revenue/revenue_action_log.csv",
    "offers/revenue_sprint/founder_dm_pack.md",
    "offers/revenue_sprint/sample_pack_template.md",
    "offers/revenue_sprint/proposal_fast_template.md",
    "offers/revenue_sprint/client_intake.md",
    "offers/revenue_sprint/delivery_report_template.md",
    "offers/revenue_sprint/qa_checklist.md",
    "offers/revenue_sprint/handoff_template.md",
    "offers/revenue_sprint/feedback_request.md",
    "offers/revenue_sprint/retainer_ask.md",
    "learning/weekly_intelligence_review.md",
    "weekly_reviews/template.md",
    "metrics_history/weekly_metrics.csv",
)

OPTIONAL_VERIFY: tuple[str, ...] = (
    "verify_private_ops_integrity.py",
    "verify_private_ops_deep.py",
    "verify_priority_sprint.py",
    "verify_daily_gate.py",
    "verify_revenue_actions.py",
    "verify_stage_gate.py",
    "verify_real_execution_evidence.py",
    "verify_revenue_sprint_kit.py",
    "verify_weekly_learning.py",
)

MARKET_EVIDENCE_THRESHOLDS = {
    "leads": 25,
    "dms_sent": 25,
    "samples": 3,
    "proposals_sent": 1,
    "payment_attempts": 1,
}


def _count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8") as f:
        return len(list(csv.DictReader(f)))


def _count_action(path: Path, action_type: str) -> int:
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8") as f:
        return sum(1 for row in csv.DictReader(f) if row.get("action_type") == action_type)


def _count_payment_attempts(path: Path) -> int:
    if not path.exists():
        return 0
    targets = {"payment_link_sent", "po_received", "written_approval", "paid"}
    with path.open(newline="", encoding="utf-8") as f:
        return sum(1 for row in csv.DictReader(f) if row.get("action_type") in targets)


def _count_samples() -> int:
    sample_dir = HERE / "offers" / "revenue_sprint"
    if not sample_dir.exists():
        return 0
    paths = list(sample_dir.glob("sample_pack_*.md")) + list(
        sample_dir.glob("sample_pack_*.pdf")
    )
    return sum(1 for p in paths if p.stem != "sample_pack_template")


def main() -> None:
    print("== Dealix Private Ops Audit ==")
    failures: list[str] = []

    for relative in REQUIRED:
        path = HERE / relative
        if not path.exists():
            failures.append(f"Missing: {relative}")
        elif path.is_file() and path.stat().st_size == 0:
            failures.append(f"Empty: {relative}")

    leads = _count_csv_rows(HERE / "pipeline" / "pipeline_tracker.csv")
    revenue_log = HERE / "revenue" / "revenue_action_log.csv"
    actions = _count_csv_rows(revenue_log)
    dms_sent = _count_action(revenue_log, "dm_sent")
    proposals_sent = _count_action(revenue_log, "proposal_sent")
    payment_attempts = _count_payment_attempts(revenue_log)
    samples = _count_samples()

    print(f"Lead count:         {leads}")
    print(f"Revenue actions:    {actions}")
    print(f"DMs sent:           {dms_sent}")
    print(f"Sample packs:       {samples}")
    print(f"Proposals sent:     {proposals_sent}")
    print(f"Payment attempts:   {payment_attempts}")

    if leads < MARKET_EVIDENCE_THRESHOLDS["leads"]:
        failures.append(f"Market evidence: need {MARKET_EVIDENCE_THRESHOLDS['leads']} leads, found {leads}")
    if actions < 1:
        failures.append("Market evidence: need at least 1 revenue action")
    if dms_sent < MARKET_EVIDENCE_THRESHOLDS["dms_sent"]:
        failures.append(
            f"Market evidence: need {MARKET_EVIDENCE_THRESHOLDS['dms_sent']} dm_sent rows, "
            f"found {dms_sent}"
        )
    if samples < MARKET_EVIDENCE_THRESHOLDS["samples"]:
        failures.append(
            f"Market evidence: need {MARKET_EVIDENCE_THRESHOLDS['samples']} sample packs, "
            f"found {samples}"
        )
    if proposals_sent < MARKET_EVIDENCE_THRESHOLDS["proposals_sent"]:
        failures.append(
            f"Market evidence: need {MARKET_EVIDENCE_THRESHOLDS['proposals_sent']} proposal, "
            f"found {proposals_sent}"
        )
    if payment_attempts < MARKET_EVIDENCE_THRESHOLDS["payment_attempts"]:
        failures.append(
            f"Market evidence: need {MARKET_EVIDENCE_THRESHOLDS['payment_attempts']} payment attempt, "
            f"found {payment_attempts}"
        )

    for script in OPTIONAL_VERIFY:
        path = HERE / script
        if path.exists():
            print(f"\n== Running {script} ==")
            result = subprocess.run([sys.executable, str(path)])
            if result.returncode != 0:
                failures.append(f"Verifier failed: {script}")

    if failures:
        print("\nPRIVATE OPS AUDIT FAILED:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("\nPASS: Dealix private ops audit passed.")


if __name__ == "__main__":
    main()
