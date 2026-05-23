#!/usr/bin/env python3
"""Bootstrap the Dealix private operations runtime.

Creates the CSV ledgers (and a couple of markdown scorecards) used by the
Dealix worker scripts and the founder operating loop. The destination root
defaults to ``/opt/dealix-ops-private`` but can be overridden with --root.

The script is idempotent: existing files are left untouched. Missing files
are created with the documented header row only.

Usage:
    python scripts/bootstrap_private_ops_runtime.py --root /opt/dealix-ops-private
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# (relative path, header columns) — used for CSV files only.
CSV_LEDGERS: Dict[str, List[str]] = {
    "intelligence/lead_intelligence_base.csv": [
        "lead_id", "captured_at", "source", "company_name", "sector",
        "country", "evidence_id", "score", "status", "owner",
    ],
    "outreach/outreach_queue.csv": [
        "queue_id", "created_at", "target_id", "channel", "message_id",
        "status", "approval_class", "approved_by", "approved_at", "evidence_id",
    ],
    "outreach/conversation_log.csv": [
        "entry_id", "logged_at", "target_id", "direction", "channel",
        "summary", "next_action", "owner",
    ],
    "outreach/suppression_list.csv": [
        "suppression_id", "added_at", "email_hash", "phone_hash", "reason",
        "added_by",
    ],
    "approvals/approval_queue.csv": [
        "approval_id", "requested_at", "agent_id", "action", "approval_class",
        "severity", "evidence_id", "status", "decided_at", "decided_by", "notes",
    ],
    "trust/approval_decisions.csv": [
        "decision_id", "decided_at", "approval_id", "outcome", "decided_by",
        "notes",
    ],
    "trust/trust_flags.csv": [
        "flag_id", "raised_at", "rule_id", "severity", "agent_id", "context",
        "status", "resolved_at",
    ],
    "trust/incidents.csv": [
        "incident_id", "opened_at", "severity", "summary", "owner", "status",
        "closed_at",
    ],
    "sales/proposal_queue.csv": [
        "proposal_id", "created_at", "client_id", "offer_id", "amount", "currency",
        "status", "approved_by", "evidence_id",
    ],
    "finance/payment_capture_queue.csv": [
        "capture_id", "created_at", "client_id", "amount", "currency", "method",
        "status", "captured_at",
    ],
    "finance/cash_collected.csv": [
        "entry_id", "collected_at", "client_id", "amount", "currency", "source",
        "evidence_id",
    ],
    "finance/ai_unit_economics.csv": [
        "period", "model", "tokens_in", "tokens_out", "cost", "revenue_attributed",
        "margin_pct",
    ],
    "runtime/worker_state.csv": [
        "entry_id", "recorded_at", "worker", "status", "notes",
    ],
    "distribution/channel_scorecard.csv": [
        "period", "channel", "leads", "qualified", "proposals", "closed_won",
        "revenue", "cac",
    ],
    "distribution/sector_scorecard.csv": [
        "period", "sector", "leads", "qualified", "proposals", "closed_won",
        "revenue",
    ],
    "evals/eval_status.csv": [
        "run_id", "ran_at", "suite_id", "score", "pass", "notes",
    ],
    "product/productization_candidates.csv": [
        "candidate_id", "identified_at", "service_name", "evidence_ids",
        "readiness_score", "owner", "status",
    ],
    "product/offer_ladder.csv": [
        "offer_id", "rung", "name_en", "name_ar", "price", "currency",
        "commitment", "approval_class",
    ],
    "product/product_distribution.csv": [
        "row_id", "product_id", "channel", "status", "owner",
        "last_cycle_metric", "updated_at",
    ],
    "security/security_status.csv": [
        "check_id", "ran_at", "status", "evidence", "owner",
    ],
    "brand/brand_assets_registry.csv": [
        "asset_id", "registered_at", "kind", "location", "version", "owner",
    ],
    "marketing/content_calendar.csv": [
        "entry_id", "scheduled_for", "surface", "title", "language",
        "proof_id", "status", "owner",
    ],
    "marketing/campaigns.csv": [
        "campaign_id", "start", "end", "hypothesis", "icp", "channels",
        "offer_id", "proof_id", "success_metric", "status",
    ],
    "marketing/content_ideas.csv": [
        "idea_id", "captured_at", "title", "intent_match", "proof_strength",
        "differentiation", "score", "owner", "status",
    ],
    "growth/target_segments.csv": [
        "segment_id", "name", "sector", "geo", "size_estimate", "owner",
    ],
    "growth/sector_targets.csv": [
        "sector", "headline_en", "headline_ar", "subhead_1", "subhead_2",
        "subhead_3", "approved_by",
    ],
    "growth/account_scores.csv": [
        "account_id", "scored_at", "score", "evidence_ids", "next_action",
        "owner",
    ],
    "growth/distribution_machines.csv": [
        "machine_id", "kind", "name", "owner", "status", "last_metric",
    ],
    "customer_success/client_health.csv": [
        "client_id", "scored_at", "health", "next_action", "owner",
    ],
    "customer_success/referral_queue.csv": [
        "referral_id", "captured_at", "client_id", "target", "status", "owner",
    ],
    "proof/proof_library.csv": [
        "proof_id", "captured_at", "kind", "summary", "evidence_location",
        "visibility", "approval_status", "owner",
    ],
    "proof/proof_approval_queue.csv": [
        "request_id", "requested_at", "proof_id", "visibility", "status",
        "decided_at", "decided_by",
    ],
}

# (relative path, body) — used for markdown placeholder files.
MD_FILES: Dict[str, str] = {
    "founder/operating_scorecard.md": (
        "# Operating Scorecard\n\n"
        "_Populated by `scripts/run_operating_scorecard_worker.py`._\n"
    ),
    "founder/sovereign_readiness.md": (
        "# Sovereign Readiness\n\n"
        "_Populated by sovereign-stack verifiers._\n"
    ),
}


def ensure_csv(path: Path, header: List[str]) -> Tuple[bool, str]:
    """Create the CSV file with the given header if it does not exist."""
    if path.exists():
        return False, f"exists  {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
    return True, f"created {path}"


def ensure_markdown(path: Path, body: str) -> Tuple[bool, str]:
    """Create the markdown file with the given body if it does not exist."""
    if path.exists():
        return False, f"exists  {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return True, f"created {path}"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default="/opt/dealix-ops-private",
        help="Destination root directory for the private ops ledgers.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0
    log_lines: List[str] = []

    for rel, header in CSV_LEDGERS.items():
        was_created, line = ensure_csv(root / rel, header)
        log_lines.append(line)
        if was_created:
            created += 1
        else:
            skipped += 1

    for rel, body in MD_FILES.items():
        was_created, line = ensure_markdown(root / rel, body)
        log_lines.append(line)
        if was_created:
            created += 1
        else:
            skipped += 1

    print("\n".join(log_lines))
    print()
    print(f"Dealix private ops runtime at: {root}")
    print(f"  created: {created}")
    print(f"  exists : {skipped}")
    print(f"  total  : {created + skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
