#!/usr/bin/env python3
"""Bootstrap the private ops runtime layout.

Creates the CSV scaffolding the Founder Console / internal API reads from.
Default root is /opt/dealix-ops-private; override with --root or PRIVATE_OPS env.

Usage:
    python scripts/bootstrap_private_ops_runtime.py --root /opt/dealix-ops-private

Safe to re-run: existing files are left untouched; only missing files and
directories are created.
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

# Each entry: (relative path, headers).
CSV_SCHEMAS: list[tuple[str, list[str]]] = [
    # intelligence
    ("intelligence/target_sectors.csv", ["sector", "saudi_relevance", "ticket_size", "score", "notes"]),
    ("intelligence/icp_segments.csv", ["segment", "industry", "company_size", "buyer_role", "score"]),
    ("intelligence/buyer_personas.csv", ["persona_id", "title", "pain", "trigger", "channel"]),
    ("intelligence/account_scores.csv", [
        "account_id", "name", "saudi_relevance", "b2b_fit", "high_ticket_potential",
        "buyer_clarity", "pain_urgency", "outreach_fit", "proof_fit",
        "partner_potential", "delivery_complexity", "trust_risk", "final_priority",
    ]),
    ("intelligence/trigger_events.csv", ["account_id", "event_type", "detected_at", "source", "confidence"]),
    # outreach
    ("outreach/outbound_queue.csv", ["draft_id", "account_id", "channel", "owner", "score", "created_at", "status"]),
    ("outreach/linkedin_queue.csv", ["draft_id", "account_id", "owner", "created_at", "status"]),
    ("outreach/email_queue.csv", ["draft_id", "account_id", "subject", "owner", "created_at", "status"]),
    ("outreach/contact_form_queue.csv", ["draft_id", "account_id", "form_url", "owner", "created_at", "status"]),
    ("outreach/followup_queue.csv", ["followup_id", "draft_id", "owner", "due_at", "status"]),
    ("outreach/conversation_log.csv", ["conversation_id", "account_id", "channel", "owner", "ts", "direction", "summary"]),
    # approvals
    ("approvals/approval_queue.csv", ["item_id", "action_type", "approval_class", "owner", "submitted_at", "evidence_attached", "status"]),
    ("approvals/approval_decisions.csv", ["item_id", "decided_at", "decided_by", "decision", "rationale"]),
    # trust
    ("trust/trust_flags.csv", ["flag_id", "source", "rule_id", "severity", "opened_at", "status", "owner"]),
    ("trust/policy_results.csv", ["evaluation_id", "rule_id", "decision", "evaluated_at", "subject"]),
    # finance
    ("finance/finance_summary.csv", [
        "as_of", "cash_collected", "mrr", "pipeline_weighted", "proposal_value",
        "payment_followups", "ai_cost_per_lead", "ai_cost_per_proposal",
        "ai_cost_per_paid_client", "runway_months",
    ]),
    ("finance/finance_events.csv", ["event_id", "type", "amount", "currency", "account_id", "ts"]),
    # runtime
    ("runtime/worker_state.csv", ["worker", "last_run", "status", "failures_24h", "next_run", "notes"]),
    ("runtime/ceo_summary.csv", [
        "as_of", "pipeline_weighted", "cash_collected", "approvals_pending",
        "trust_flags_open", "workers_fresh",
    ]),
    ("runtime/sales_funnel.csv", [
        "as_of", "leads_researched", "a_leads", "approved_outreach", "sent_actions",
        "replies", "positive_replies", "samples_sent", "proposals_sent",
    ]),
    ("runtime/operating_scorecard.csv", ["as_of", "score", "brand", "distribution", "revenue", "trust"]),
    ("runtime/audit_events.csv", ["event_id", "ts", "actor", "type", "class", "policy", "outcome"]),
    ("runtime/agent_registry_state.csv", ["agent_id", "state", "last_invocation", "violations_24h"]),
    ("runtime/eval_results.csv", ["suite_id", "status", "score", "when"]),
    ("runtime/risk_register.csv", ["risk_id", "title", "severity", "owner", "status", "opened_at"]),
    ("runtime/engagements.csv", ["engagement_id", "client", "stage", "owner", "risk"]),
    ("runtime/clients.csv", ["client_id", "name", "status", "owner"]),
    ("runtime/proof_candidates.csv", ["candidate_id", "client_id", "status", "owner", "updated_at"]),
    ("runtime/productization_candidates.csv", ["candidate_id", "origin", "stage", "owner"]),
    ("runtime/experiments.csv", ["experiment_id", "hypothesis", "owner", "status", "decision_date"]),
    ("runtime/content_drafts.csv", ["draft_id", "channel", "owner", "status"]),
    ("runtime/security_findings.csv", ["finding_id", "source", "severity", "found_at", "owner", "status"]),
    # distribution
    ("distribution/sector_targets.csv", ["sector", "priority", "owner"]),
    ("distribution/abm_strategic_accounts.csv", ["account_id", "name", "priority", "owner"]),
    ("distribution/partner_pipeline.csv", ["partner_id", "name", "stage", "owner"]),
    # marketing
    ("marketing/content_calendar.csv", ["asset_id", "channel", "scheduled_for", "owner", "status"]),
    # growth
    ("growth/experiment_backlog.csv", ["experiment_id", "hypothesis", "owner", "stage"]),
    ("growth/learning_loop.csv", ["learning_id", "experiment_id", "outcome", "when"]),
    # product
    ("product/offer_ladder.csv", ["rung", "name", "buyer", "price_band", "status"]),
    # security
    ("security/secret_scans.csv", ["scan_id", "when", "findings_count"]),
    # brand
    ("brand/brand_violations.csv", ["violation_id", "asset_id", "rule", "severity", "status"]),
]


def ensure_csv(root: Path, rel: str, headers: list[str]) -> str:
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return "exists"
    with target.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Dealix private ops runtime.")
    parser.add_argument(
        "--root",
        default=os.environ.get("PRIVATE_OPS")
        or os.environ.get("PRIVATE_OPS_ROOT")
        or "/opt/dealix-ops-private",
        help="Private ops root directory (default /opt/dealix-ops-private).",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    created = 0
    existing = 0
    for rel, headers in CSV_SCHEMAS:
        outcome = ensure_csv(root, rel, headers)
        if outcome == "created":
            created += 1
        else:
            existing += 1

    print(f"[bootstrap] root: {root}")
    print(f"[bootstrap] created: {created}  existing: {existing}  total: {len(CSV_SCHEMAS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
