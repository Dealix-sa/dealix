#!/usr/bin/env python3
"""Bootstrap the Dealix private operating data tree.

Creates the directory structure and CSV headers expected by the Founder
Console runtime reader. Idempotent: existing files are left untouched.

Usage:
    python scripts/bootstrap_private_ops_runtime.py \
        --private-ops /opt/dealix-ops-private
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

# Header definitions must match api.internal.runtime_reader.RUNTIME_FILES.
RUNTIME_HEADERS: dict[str, list[str]] = {
    "intelligence/lead_intelligence_base.csv": [
        "lead_id", "company", "sector", "score", "intent",
        "last_signal", "owner", "status", "updated_at",
    ],
    "outreach/outreach_queue.csv": [
        "outreach_id", "lead_id", "channel", "approval_class",
        "state", "scheduled_at", "approved_by", "updated_at",
    ],
    "outreach/conversation_log.csv": [
        "conversation_id", "lead_id", "direction", "channel",
        "sentiment", "summary", "occurred_at",
    ],
    "outreach/suppression_list.csv": [
        "identifier", "channel", "reason", "added_at",
    ],
    "approvals/approval_queue.csv": [
        "approval_id", "type", "approval_class", "risk_level",
        "summary", "evidence", "recommended_action", "created_at",
    ],
    "trust/approval_decisions.csv": [
        "approval_id", "type", "actor", "decision", "reason",
        "approval_class", "risk_level", "policy_result", "evidence",
        "source_endpoint", "timestamp", "external_action_allowed",
    ],
    "trust/trust_flags.csv": [
        "flag_id", "category", "severity", "summary", "evidence",
        "status", "created_at",
    ],
    "sales/proposal_queue.csv": [
        "proposal_id", "lead_id", "stage", "value_sar",
        "expected_close", "owner", "updated_at",
    ],
    "finance/payment_capture_queue.csv": [
        "invoice_id", "customer", "amount_sar", "due_date",
        "stage", "last_followup_at", "updated_at",
    ],
    "finance/cash_collected.csv": [
        "invoice_id", "customer", "amount_sar", "collected_at",
        "method",
    ],
    "runtime/worker_state.csv": [
        "worker", "last_run", "status", "failures_24h",
        "next_run", "notes",
    ],
    "distribution/channel_scorecard.csv": [
        "channel", "sent", "replies", "positive_replies",
        "samples", "proposals", "payments",
    ],
    "distribution/sector_scorecard.csv": [
        "sector", "pipeline_sar", "wins", "win_rate",
        "avg_cycle_days", "samples",
    ],
    "evals/eval_status.csv": [
        "suite", "passed", "failed", "warn", "last_run",
        "blocking",
    ],
    "product/productization_candidates.csv": [
        "candidate_id", "name", "stage", "evidence", "next_step",
        "updated_at",
    ],
    "security/security_status.csv": [
        "control", "status", "last_checked", "owner", "evidence",
    ],
    "founder/.gitkeep": [],
}


def bootstrap(root: Path) -> dict[str, str]:
    report: dict[str, str] = {}
    for rel, headers in RUNTIME_HEADERS.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            report[str(path)] = "exists"
            continue
        if not headers:
            path.write_text("", encoding="utf-8")
            report[str(path)] = "created_empty"
            continue
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(headers)
        report[str(path)] = "created"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default="/opt/dealix-ops-private",
        help="Private ops root directory (default: /opt/dealix-ops-private)",
    )
    args = parser.parse_args(argv)
    root = Path(args.private_ops).expanduser().resolve()
    try:
        root.mkdir(parents=True, exist_ok=True)
    except PermissionError as exc:
        print(f"ERROR: cannot create {root}: {exc}", file=sys.stderr)
        return 2
    report = bootstrap(root)
    created = sum(1 for v in report.values() if v.startswith("created"))
    exists = sum(1 for v in report.values() if v == "exists")
    print(f"private_ops_root: {root}")
    print(f"created: {created}")
    print(f"already_present: {exists}")
    for path, state in sorted(report.items()):
        print(f"  {state:14s}  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
