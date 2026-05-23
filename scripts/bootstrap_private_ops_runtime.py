#!/usr/bin/env python3
"""
Bootstrap the Dealix private ops runtime.

Creates the canonical folder tree and seed CSV files outside the repo
(default: /opt/dealix-ops-private, overridable via env or CLI).
This directory holds operational state (approvals, suppression list,
trust flags, conversation logs, finance, etc) — none of which belongs in
git.

Usage:
    python scripts/bootstrap_private_ops_runtime.py
    python scripts/bootstrap_private_ops_runtime.py --target /opt/dealix-ops-private
    PRIVATE_OPS=/opt/dealix-ops-private python scripts/bootstrap_private_ops_runtime.py
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Canonical files — (relative_path, header_columns)
FILES: list[tuple[str, list[str]]] = [
    ("intelligence/lead_intelligence_base.csv",
     ["id", "sector", "company", "url", "country", "size", "trigger_event", "score", "added_at"]),
    ("outreach/outreach_queue.csv",
     ["id", "channel", "draft", "approval_state", "owner", "due", "created_at"]),
    ("outreach/conversation_log.csv",
     ["id", "lead_id", "channel", "stage", "summary", "ts"]),
    ("outreach/suppression_list.csv",
     ["id", "match_type", "match_value", "reason", "added_by", "added_at"]),
    ("outreach/linkedin_queue.csv",
     ["id", "target", "message_draft", "approval_state", "owner", "created_at"]),
    ("outreach/contact_form_queue.csv",
     ["id", "target_url", "message_draft", "approval_state", "owner", "created_at"]),
    ("outreach/followup_queue.csv",
     ["id", "lead_id", "draft", "due_at", "approval_state"]),
    ("outreach/reply_routing_queue.csv",
     ["id", "lead_id", "intent", "suggested_route", "approval_state"]),
    ("outreach/nurture_queue.csv",
     ["id", "lead_id", "stage", "next_touch_due", "approval_state"]),
    ("approvals/approval_queue.csv",
     ["id", "type", "risk", "summary", "payload_ref", "status", "created_at"]),
    ("trust/approval_decisions.csv",
     ["id", "ts", "actor", "action", "target", "risk", "payload_json"]),
    ("trust/trust_flags.csv",
     ["id", "severity", "description", "source", "created_at"]),
    ("trust/incidents.csv",
     ["id", "status", "severity", "summary", "owner", "opened_at", "closed_at"]),
    ("sales/proposal_queue.csv",
     ["id", "client", "offer", "sprint", "value_sar", "status", "created_at"]),
    ("sales/sample_queue.csv",
     ["id", "prospect", "sample_type", "status", "approval_state", "created_at"]),
    ("finance/payment_capture_queue.csv",
     ["id", "client", "invoice_no", "amount_sar", "status", "due_date"]),
    ("finance/cash_collected.csv",
     ["id", "client", "amount_sar", "collected_at", "method"]),
    ("finance/ai_unit_economics.csv",
     ["ts", "ai_cost_usd", "deals_supported", "cost_per_deal_usd"]),
    ("runtime/worker_state.csv",
     ["id", "name", "status", "last_run", "failure_count", "owner"]),
    ("distribution/channel_scorecard.csv",
     ["channel", "draft_volume_7d", "reply_rate", "qualified_rate", "owner"]),
    ("distribution/sector_scorecard.csv",
     ["sector", "accounts", "engaged", "qualified", "won", "owner"]),
    ("distribution/experiment_log.csv",
     ["id", "hypothesis", "channel", "started_at", "ended_at", "result", "status", "owner"]),
    ("evals/eval_status.csv",
     ["ts", "suite", "pass", "fail", "blocking", "notes"]),
    ("product/productization_candidates.csv",
     ["id", "offer", "rung", "readiness", "owner", "next_step"]),
    ("product/offer_ladder.csv",
     ["rung", "name", "positioning", "price_band_sar", "trust_gate"]),
    ("product/product_distribution.csv",
     ["rung", "offer", "channel", "status", "owner"]),
    ("security/security_status.csv",
     ["ts", "secrets_scan", "dependency_scan", "pdpl_review", "incident_open"]),
    ("brand/brand_assets_registry.csv",
     ["id", "asset_type", "path", "approved_by", "ts"]),
    ("marketing/content_calendar.csv",
     ["day", "topic", "channel", "owner", "approval_state"]),
    ("marketing/campaigns.csv",
     ["id", "name", "sector", "owner", "status", "created_at"]),
    ("marketing/content_ideas.csv",
     ["id", "topic", "source", "sector", "owner", "created_at"]),
    ("growth/target_segments.csv",
     ["segment", "icp_fit", "saudi_relevance", "ticket_band_sar", "priority"]),
    ("growth/sector_targets.csv",
     ["sector", "priority", "accounts", "score", "owner"]),
    ("growth/account_scores.csv",
     ["account", "sector", "score", "rank", "next_action"]),
    ("growth/distribution_machines.csv",
     ["machine", "owner", "status", "kpi", "trust_gate"]),
    ("customer_success/client_health.csv",
     ["client", "health", "next_action", "due", "owner"]),
    ("customer_success/referral_queue.csv",
     ["id", "client", "referral_target", "status", "owner"]),
    ("proof/proof_library.csv",
     ["id", "sector", "title", "summary_md_ref", "approval_state", "owner"]),
    ("proof/proof_approval_queue.csv",
     ["id", "proof_id", "submitted_by", "status", "ts"]),
]

MARKDOWN_FILES: list[tuple[str, str]] = [
    ("founder/operating_scorecard.md",
     "# Operating Scorecard\n\nFour pillars (Revenue / Trust / Delivery / Growth).\nRefresh nightly. Source: Founder Console scorecard worker.\n"),
    ("founder/sovereign_readiness.md",
     "# Sovereign Readiness\n\nSaudi data residency, PDPL, NCA alignment, Arabic quality.\nReviewed monthly.\n"),
]


def _resolve_target(cli_target: str | None) -> Path:
    target = cli_target or os.getenv("PRIVATE_OPS") or os.getenv("DEALIX_PRIVATE_OPS_DIR") or "/opt/dealix-ops-private"
    return Path(target).expanduser().resolve()


def bootstrap(target: Path, force: bool = False) -> dict[str, list[str]]:
    """Create folders + seed CSVs. Returns a summary dict."""
    created_files: list[str] = []
    skipped_files: list[str] = []
    created_dirs: list[str] = []

    for rel, header in FILES:
        full = target / rel
        if not full.parent.exists():
            full.parent.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(full.parent))
        if full.exists() and not force:
            skipped_files.append(str(full))
            continue
        with full.open("w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerow(header)
        created_files.append(str(full))

    for rel, body in MARKDOWN_FILES:
        full = target / rel
        if not full.parent.exists():
            full.parent.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(full.parent))
        if full.exists() and not force:
            skipped_files.append(str(full))
            continue
        full.write_text(body, encoding="utf-8")
        created_files.append(str(full))

    # README so anyone discovering the folder knows what it is.
    readme = target / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Dealix Private Ops Runtime\n\n"
            "This directory holds **operational state** for Dealix (approvals,\n"
            "trust flags, conversation logs, finance, etc). It is **outside the\n"
            "repository** by design. Never commit anything from this directory.\n\n"
            f"Bootstrapped at: {datetime.now(timezone.utc).isoformat()}\n",
            encoding="utf-8",
        )
        created_files.append(str(readme))

    return {"created_files": created_files, "skipped_files": skipped_files, "created_dirs": created_dirs}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Bootstrap Dealix private ops runtime")
    ap.add_argument("--target", help="Target directory (default: /opt/dealix-ops-private or $PRIVATE_OPS)")
    ap.add_argument("--force", action="store_true", help="Overwrite existing seed files")
    args = ap.parse_args(argv)

    target = _resolve_target(args.target)
    try:
        target.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"ERROR: cannot create {target} — choose a writable path via --target or PRIVATE_OPS=", file=sys.stderr)
        return 2

    summary = bootstrap(target, force=args.force)
    print(f"[ok] private ops runtime at: {target}")
    print(f"  created files: {len(summary['created_files'])}")
    print(f"  skipped (exist): {len(summary['skipped_files'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
