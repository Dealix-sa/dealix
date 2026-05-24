#!/usr/bin/env python3
"""Bootstrap the private ops workspace.

Creates the full directory tree and seeds empty CSV/MD files with headers
under DEALIX_PRIVATE_OPS (default: /opt/dealix-ops-private). Idempotent.

Usage:
    python scripts/bootstrap_private_ops_runtime.py [--root PATH]
"""
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

DEFAULT_ROOT = os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private")

DIRECTORIES: list[str] = [
    "founder",
    "intelligence",
    "outreach",
    "approvals",
    "trust",
    "sales",
    "finance",
    "growth",
    "market_attack",
    "campaigns",
    "graph",
    "proof",
    "partners",
    "product",
    "customer_success",
    "runtime",
    "evals",
    "security",
    "legal",
    "people",
    "learning",
    "metrics",
]

CSV_FILES: dict[str, list[str]] = {
    # founder
    "founder/decision_log.csv": ["decided_at", "decision", "rationale", "owner"],
    "founder/strategic_assumptions.csv": ["assumption", "validation_state", "evidence"],
    "founder/delegation_queue.csv": ["task", "to", "due_date", "state"],
    "founder/founder_time_audit.csv": ["date", "hours_block", "category", "roi_estimate"],
    # intelligence
    "intelligence/lead_intelligence_base.csv": ["account", "sector", "signal", "source", "freshness_iso"],
    # outreach
    "outreach/outreach_queue.csv": ["queued_at", "account", "draft_text", "approval_state"],
    "outreach/conversation_log.csv": ["account", "contact", "channel", "message_at", "summary"],
    "outreach/suppression_list.csv": ["account", "reason", "since"],
    "outreach/linkedin_queue.csv": ["account", "contact", "draft", "approval_state"],
    "outreach/contact_form_queue.csv": ["account", "url", "draft", "approval_state"],
    "outreach/followup_queue.csv": ["account", "due_at", "next_step", "approval_state"],
    "outreach/reply_routing_queue.csv": ["account", "reply_at", "router_label", "approval_state"],
    "outreach/nurture_queue.csv": ["account", "nurture_track", "next_touch_at", "approval_state"],
    # approvals
    "approvals/approval_queue.csv": ["id", "action_id", "reason", "payload", "queued_at", "decision", "external_action_allowed"],
    # trust
    "trust/approval_decisions.csv": ["id", "decided_at", "decision", "approver"],
    "trust/trust_flags.csv": ["flagged_at", "flag", "subject", "severity"],
    "trust/incidents.csv": ["opened_at", "summary", "severity", "status"],
    "trust/customer_trust_packet.csv": ["customer", "evidence_url", "approved_for_external"],
    # sales
    "sales/proposal_queue.csv": ["account", "draft", "approval_state"],
    "sales/sample_queue.csv": ["account", "sample_type", "approval_state"],
    "sales/sales_asset_registry.csv": ["asset_id", "title", "kind", "approved_for_external"],
    # finance
    "finance/payment_capture_queue.csv": ["customer", "amount_sar", "approval_state"],
    "finance/cash_collected.csv": ["received_at", "customer", "amount_sar", "source"],
    "finance/ai_unit_economics.csv": ["unit", "cost_sar", "revenue_sar", "margin"],
    "finance/capital_allocation.csv": ["category", "decision", "rationale"],
    "finance/roi_priority_matrix.csv": ["item", "roi_score", "decision"],
    "finance/resource_allocation.csv": ["resource", "allocation_pct", "rationale"],
    # growth
    "growth/target_segments.csv": ["segment", "score", "decision"],
    "growth/sector_targets.csv": ["sector", "score", "decision"],
    "growth/account_scores.csv": ["account", "score", "rationale"],
    "growth/distribution_machines.csv": ["machine", "state", "kill_switch"],
    "growth/message_performance.csv": ["message_id", "angle", "reply_rate", "convert_rate"],
    # market_attack
    "market_attack/beachhead_sector_scorecard.csv": ["sector", "score", "rationale"],
    "market_attack/strategic_accounts.csv": ["account", "priority", "rationale"],
    "market_attack/offer_market_fit_tests.csv": ["test_id", "offer", "result"],
    "market_attack/objection_library.csv": ["objection", "response", "approved"],
    # campaigns
    "campaigns/campaign_registry.csv": ["campaign_id", "name", "owner", "state"],
    "campaigns/campaign_assets.csv": ["asset_id", "campaign_id", "kind", "approval_state"],
    "campaigns/campaign_queue.csv": ["campaign_id", "queued_at", "approval_state"],
    "campaigns/campaign_results.csv": ["campaign_id", "metric", "value"],
    # graph
    "graph/accounts.csv": ["account_id", "name", "sector"],
    "graph/contacts.csv": ["contact_id", "account_id", "role"],
    "graph/signals.csv": ["signal_id", "account_id", "kind", "ts"],
    "graph/messages.csv": ["message_id", "account_id", "angle", "ts"],
    "graph/offers.csv": ["offer_id", "name", "price_sar"],
    "graph/objections.csv": ["objection_id", "account_id", "objection"],
    "graph/proof_edges.csv": ["proof_id", "account_id"],
    "graph/partner_edges.csv": ["partner_id", "account_id"],
    "graph/learnings.csv": ["learning_id", "summary", "ts"],
    # proof
    "proof/proof_library.csv": ["proof_id", "customer", "result", "evidence_url", "approved_for_external"],
    "proof/proof_approval_queue.csv": ["proof_id", "queued_at", "approval_state"],
    "proof/case_study_candidates.csv": ["customer", "result", "approval_state"],
    "proof/proof_to_demand_assets.csv": ["proof_id", "asset_id", "approval_state"],
    # partners
    "partners/partner_pipeline.csv": ["partner_id", "stage", "next_step"],
    "partners/partner_ecosystem.csv": ["partner_id", "category", "state"],
    "partners/co_sell_opportunities.csv": ["partner_id", "account_id", "state"],
    "partners/white_label_pipeline.csv": ["partner_id", "state", "next_step"],
    "partners/partner_priority.csv": ["partner_id", "priority", "rationale"],
    # product
    "product/offer_ladder.csv": ["rung", "name", "price_sar", "cycle"],
    "product/product_distribution.csv": ["product_id", "channel", "state"],
    "product/productization_candidates.csv": ["candidate", "evidence", "decision"],
    "product/productization_pipeline.csv": ["candidate", "stage", "next_step"],
    # customer_success
    "customer_success/client_health.csv": ["customer", "score", "risks"],
    "customer_success/referral_queue.csv": ["customer", "referral_target", "approval_state"],
    "customer_success/expansion_opportunities.csv": ["customer", "opportunity", "approval_state"],
    "customer_success/renewal_risk.csv": ["customer", "risk_level", "next_action"],
    "customer_success/expansion_map.csv": ["customer", "expansion_path", "approval_state"],
    # runtime
    "runtime/worker_state.csv": ["worker_id", "last_run_iso", "status", "kill_switch"],
    # evals
    "evals/eval_status.csv": ["eval_id", "gate", "result", "freshness_iso"],
    # security
    "security/security_status.csv": ["item", "state", "owner"],
    # legal
    "legal/commercial_guardrails.csv": ["clause", "rule", "owner"],
    # people
    "people/role_scorecards.csv": ["role", "kpi", "current"],
    "people/hiring_triggers.csv": ["role", "trigger_metric", "threshold"],
    "people/contractor_bench.csv": ["contractor", "skill", "availability"],
    "people/talent_gap.csv": ["gap", "severity", "next_step"],
    # learning
    "learning/company_memory.csv": ["recorded_at", "lesson", "owner"],
    "learning/market_learning.csv": ["recorded_at", "sector", "lesson"],
    "learning/message_learning.csv": ["recorded_at", "angle", "lesson"],
    "learning/offer_learning.csv": ["recorded_at", "offer", "lesson"],
    "learning/sector_learning.csv": ["recorded_at", "sector", "lesson"],
    # metrics
    "metrics/hypergrowth_metrics.csv": ["metric", "value", "freshness_iso"],
}

MD_FILES: dict[str, str] = {
    "founder/ceo_daily_brief.md": "# CEO Daily Brief\n\nGenerated by `make ceo-daily-brief`.\n",
    "founder/ceo_weekly_review.md": "# CEO Weekly Review\n\nGenerated by `make ceo-weekly-review`.\n",
    "founder/operating_scorecard.md": "# Operating Scorecard\n",
    "founder/sovereign_readiness.md": "# Sovereign Readiness\n",
    "finance/revenue_forecast.md": "# Revenue Forecast\n",
    "market_attack/beachhead_sector_scorecard.md": "# Beachhead Sector Scorecard\n",
    "market_attack/offer_market_fit_report.md": "# Offer-Market-Fit Report\n",
    "graph/revenue_intelligence_graph_report.md": "# Revenue Intelligence Graph Report\n",
}


def ensure_csv(path: Path, header: list[str]) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
    return True


def ensure_md(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    for d in DIRECTORIES:
        (root / d).mkdir(parents=True, exist_ok=True)
    created_csv = 0
    created_md = 0
    for rel, header in CSV_FILES.items():
        if ensure_csv(root / rel, header):
            created_csv += 1
    for rel, content in MD_FILES.items():
        if ensure_md(root / rel, content):
            created_md += 1
    print(f"private ops root: {root}")
    print(f"directories: {len(DIRECTORIES)}")
    print(f"csv files seeded: {created_csv}")
    print(f"md files seeded: {created_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
