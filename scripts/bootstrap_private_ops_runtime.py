"""Bootstrap the private_ops runtime tree.

Creates the directory tree expected by the generators, with empty
header-only CSVs and a README. Idempotent — safe to re-run; never
overwrites existing data.

Usage:
    python scripts/bootstrap_private_ops_runtime.py --private-ops /opt/dealix-ops-private
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

TREE: dict[str, list[tuple[str, list[str]]]] = {
    "founder": [
        ("ceo_daily_brief.md", []),
        ("ceo_weekly_review.md", []),
        ("decision_log.csv", ["id", "date", "decision", "owner", "outcome"]),
        ("strategic_assumptions.csv",
         ["id", "assumption", "status", "evidence_for", "evidence_against", "owner", "review_date"]),
        ("delegation_queue.csv", ["id", "task", "owner", "due", "status"]),
        ("founder_time_audit.csv", ["date", "block", "category", "minutes", "note"]),
    ],
    "approvals": [
        ("approval_queue.csv",
         ["id", "ts", "agent", "approval_class", "action", "summary", "status"]),
    ],
    "trust": [
        ("approval_decisions.csv",
         ["id", "ts", "approval_queue_id", "decision", "decided_by", "note"]),
        ("trust_flags.csv", ["id", "ts", "source", "severity", "summary", "status"]),
        ("incidents.csv", ["id", "ts", "severity", "summary", "status", "owner"]),
        ("customer_trust_packet.csv", ["customer_id", "packet_url", "issued_at"]),
    ],
    "outreach": [
        ("outreach_queue.csv",
         ["id", "ts", "channel", "recipient_handle", "draft_id", "approval_class", "status"]),
        ("suppression_list.csv", ["channel", "handle", "reason", "added_at"]),
        ("followup_queue.csv", ["id", "ts", "thread_id", "next_action", "due"]),
        ("reply_routing_queue.csv", ["id", "ts", "inbound_id", "route_to", "status"]),
        ("nurture_queue.csv", ["id", "contact_id", "next_touch", "playbook"]),
    ],
    "finance": [
        ("payment_capture_queue.csv",
         ["id", "ts", "amount_sar", "customer_id", "method", "status"]),
        ("cash_collected.csv", ["date", "amount_sar", "customer_id", "invoice_id"]),
        ("revenue_forecast.md", []),
        ("capital_allocation.csv", ["bucket", "allocated_sar", "spent_sar"]),
        ("roi_priority_matrix.csv",
         ["initiative", "owner", "cost_sar", "expected_return_sar", "horizon_weeks"]),
    ],
    "graph": [
        ("accounts.csv",
         ["id", "name", "stage", "expected_value_sar", "close_probability", "close_date"]),
        ("contacts.csv", ["id", "account_id", "name", "channel", "handle", "consent_status"]),
        ("signals.csv", ["id", "account_id", "ts", "type", "source", "summary"]),
        ("messages.csv", ["id", "thread_id", "ts", "direction", "channel", "summary"]),
        ("offers.csv", ["id", "name", "list_price_sar", "scope"]),
        ("objections.csv", ["id", "account_id", "objection", "response"]),
        ("learnings.csv", ["id", "date", "topic", "learning", "source", "tag"]),
    ],
    "market_attack": [
        ("beachhead_sector_scorecard.csv",
         ["sector", "wedge_score", "urgency", "wtp", "rationale"]),
        ("strategic_accounts.csv",
         ["account_id", "name", "sector", "wedge_fit", "next_action"]),
        ("offer_market_fit_tests.csv",
         ["test_id", "offer", "sample_size", "conversion_rate", "verdict"]),
    ],
    "runtime": [
        ("worker_state.csv", ["worker_id", "last_run", "last_status", "note"]),
    ],
    "ai_governance": [
        ("ai_system_inventory.csv",
         ["id", "name", "owner", "vendor", "data_class", "risk_tier"]),
        ("ai_risk_register.csv", ["id", "system_id", "risk", "severity", "mitigation", "owner"]),
        ("governance_board_pack.csv", ["date", "topic", "decision", "owner"]),
    ],
    "legal": [
        ("commercial_guardrails.csv", ["id", "topic", "rule", "owner"]),
    ],
    "customer_success": [
        ("client_health.csv",
         ["customer_id", "health_score", "last_touch", "next_review", "owner"]),
        ("expansion_opportunities.csv",
         ["customer_id", "opportunity", "expected_value_sar", "owner"]),
        ("referral_queue.csv", ["id", "customer_id", "referee", "status"]),
    ],
    "metrics": [
        ("hypergrowth_metrics.csv", ["date", "metric", "value", "owner"]),
    ],
}

README = """# Dealix Private Ops Runtime

This directory is INTENTIONALLY OUTSIDE the GitHub repository.
It holds operational ledgers (CSV / Markdown) that must never reach
a public surface or third-party SaaS without an approval+audit trail.

DO NOT commit this directory to git. The path is referenced by the
DEALIX_PRIVATE_OPS environment variable.

Re-bootstrap (safe, idempotent):

    python scripts/bootstrap_private_ops_runtime.py \\
        --private-ops $DEALIX_PRIVATE_OPS
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="bootstrap_private_ops_runtime")
    p.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.private_ops)
    if args.dry_run:
        print(f"[dry-run] would bootstrap {root}")
    root.mkdir(parents=True, exist_ok=True)
    readme = root / "README.md"
    if not readme.exists() and not args.dry_run:
        readme.write_text(README, encoding="utf-8")

    created: list[str] = []
    for sub, files in TREE.items():
        subdir = root / sub
        if not args.dry_run:
            subdir.mkdir(parents=True, exist_ok=True)
        for name, headers in files:
            path = subdir / name
            if path.exists():
                continue
            if args.dry_run:
                created.append(str(path))
                continue
            if name.endswith(".csv"):
                with path.open("w", encoding="utf-8", newline="") as f:
                    if headers:
                        csv.writer(f).writerow(headers)
            else:
                path.write_text("", encoding="utf-8")
            created.append(str(path))

    print(f"private_ops root: {root}")
    print(f"created {len(created)} files")
    for p in created[:20]:
        print(f"  + {p}")
    if len(created) > 20:
        print(f"  + ... and {len(created) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
