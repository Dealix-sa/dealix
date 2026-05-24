#!/usr/bin/env python3
"""
Bootstrap the Dealix private-ops runtime scaffold.

Default location: /opt/dealix (honors the existing convention).
Override via $PRIVATE_OPS env var or --private-ops flag.

Idempotent: never overwrites existing files. Creates only the new
subdirectories that don't exist yet, each seeded with a header-only
CSV + a placeholder README.md.

Reads: nothing from the repo (this is a scaffold script).
Writes: $PRIVATE_OPS/<subdir>/* outside the repo.

Honors the 11 non-negotiables:
  - no external send
  - no live charge
  - no scraping
  - read-only / placeholder seeds only
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# (subdir, csv_filename, csv_headers, placeholder_md_title)
SCAFFOLD: list[tuple[str, str, list[str], str]] = [
    ("founder", "decision_log.csv",
     ["timestamp", "decision_id", "category", "decision_en", "rationale_en", "owner", "review_date"],
     "Founder Decision Log"),
    ("founder", "strategic_assumptions.csv",
     ["assumption_id", "statement_en", "owner", "test_method", "review_date", "status"],
     "Strategic Assumptions"),
    ("founder", "delegation_queue.csv",
     ["task_id", "task_en", "from_role", "to_role", "due_date", "status"],
     "Delegation Queue"),
    ("founder", "founder_time_audit.csv",
     ["date", "activity", "category", "minutes", "leverage_score"],
     "Founder Time Audit"),

    ("outreach", "outreach_queue.csv",
     ["draft_id", "contact_id", "channel", "subject", "draft_en", "draft_ar", "status", "approval_required"],
     "Outreach Queue (drafts only — no auto-send)"),
    ("outreach", "conversation_log.csv",
     ["message_id", "contact_id", "direction", "channel", "body", "timestamp", "source"],
     "Conversation Log"),
    ("outreach", "followup_queue.csv",
     ["followup_id", "contact_id", "due_date", "next_action_en", "owner", "status"],
     "Follow-up Queue"),
    ("outreach", "reply_routing_queue.csv",
     ["reply_id", "contact_id", "intent", "suggested_route", "approval_required", "status"],
     "Reply Routing Queue"),
    ("outreach", "suppression_list.csv",
     ["contact_id", "reason", "added_at", "source"],
     "Suppression List"),

    ("approvals", "approval_queue.csv",
     ["request_id", "action_class", "risk_level", "requires_evidence", "status", "decision", "decided_at", "decided_by"],
     "Approval Queue"),

    ("trust", "approval_decisions.csv",
     ["decision_id", "action_class", "approved", "evidence_refs", "decided_at", "decided_by"],
     "Approval Decisions Ledger"),
    ("trust", "trust_flags.csv",
     ["flag_id", "category", "severity", "summary_en", "detected_at", "status"],
     "Trust Flags"),
    ("trust", "incidents.csv",
     ["incident_id", "category", "severity", "summary_en", "detected_at", "resolved_at", "owner"],
     "Incidents"),

    ("finance", "payment_capture_queue.csv",
     ["invoice_id", "customer_handle", "amount_sar", "status", "created_at", "captured_at"],
     "Payment Capture Queue (test mode only — NO live charge)"),
    ("finance", "cash_collected.csv",
     ["receipt_id", "customer_handle", "amount_sar", "received_at", "evidence_ref"],
     "Cash Collected (payment evidence only)"),
    ("finance", "capital_allocation.csv",
     ["category", "subcategory", "monthly_sar", "roi_note", "owner", "review_date"],
     "Capital Allocation"),

    ("market_attack", "beachhead_sector_scorecard.csv",
     ["sector", "fit_score", "evidence_count", "active_conversations", "paid_pilots", "review_date"],
     "Beachhead Sector Scorecard"),
    ("market_attack", "strategic_accounts.csv",
     ["account_handle", "sector", "score", "stage", "owner", "next_action_en", "next_action_date"],
     "Strategic Accounts"),
    ("market_attack", "offer_market_fit_tests.csv",
     ["test_id", "offer_id", "sector", "hypothesis_en", "result_en", "evidence_ref"],
     "Offer-Market Fit Tests"),

    ("graph", "accounts.csv",
     ["account_id", "handle", "sector", "size_band", "source", "first_seen", "last_signal"],
     "Accounts"),
    ("graph", "contacts.csv",
     ["contact_id", "account_id", "role", "consent_status", "source", "first_seen"],
     "Contacts"),
    ("graph", "signals.csv",
     ["signal_id", "account_id", "type", "source", "captured_at", "evidence_ref"],
     "Signals"),
    ("graph", "messages.csv",
     ["message_id", "contact_id", "direction", "channel", "body_hash", "timestamp", "approval_id"],
     "Messages"),
    ("graph", "learnings.csv",
     ["learning_id", "category", "summary_en", "evidence_ref", "captured_at"],
     "Learnings"),

    ("customer_success", "client_health.csv",
     ["customer_handle", "delivery_score", "engagement_score", "expansion_score", "risk_flags", "as_of"],
     "Client Health"),
    ("customer_success", "expansion_opportunities.csv",
     ["opportunity_id", "customer_handle", "next_rung", "evidence_refs", "blocker", "owner"],
     "Expansion Opportunities"),
    ("customer_success", "referral_queue.csv",
     ["referral_id", "from_customer", "to_account", "status", "approval_required"],
     "Referral Queue"),

    ("runtime", "worker_state.csv",
     ["worker_id", "state", "last_heartbeat", "last_error", "owner"],
     "Worker State"),

    ("metrics", "hypergrowth_metrics.csv",
     ["metric_id", "name", "value", "unit", "source", "captured_at", "is_estimate"],
     "Hypergrowth Metrics (every numeric value must carry source OR is_estimate=true)"),
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _placeholder_md(title: str, csv_path: Path) -> str:
    return (
        f"# {title}\n\n"
        f"- Created: {_now_iso()}\n"
        f"- Backing CSV: `{csv_path.name}`\n"
        f"- Owner role: Founder (override via `OWNER` column).\n"
        f"- This file is part of the **private** Dealix ops runtime.\n"
        f"- It MUST NOT be committed to the repo.\n"
        f"- Every numeric value referenced from this CSV must carry a\n"
        f"  `source` field OR an `is_estimate=true` flag (claim_policy).\n"
    )


def bootstrap(private_ops: Path, *, dry_run: bool = False) -> dict[str, int]:
    """Create the scaffold under private_ops. Idempotent; never overwrites."""
    stats = {"created_dirs": 0, "created_csvs": 0, "created_mds": 0, "unchanged": 0}
    if not private_ops.exists():
        if dry_run:
            stats["created_dirs"] += 1
        else:
            private_ops.mkdir(parents=True, exist_ok=True)
            stats["created_dirs"] += 1

    seen_dirs: set[Path] = set()
    for subdir, csv_name, headers, md_title in SCAFFOLD:
        target_dir = private_ops / subdir
        if target_dir not in seen_dirs:
            if not target_dir.exists():
                if not dry_run:
                    target_dir.mkdir(parents=True, exist_ok=True)
                stats["created_dirs"] += 1
            seen_dirs.add(target_dir)

        csv_path = target_dir / csv_name
        if not csv_path.exists():
            if not dry_run:
                csv_path.write_text(",".join(headers) + "\n", encoding="utf-8")
            stats["created_csvs"] += 1
        else:
            stats["unchanged"] += 1

        md_path = target_dir / "README.md"
        if not md_path.exists():
            if not dry_run:
                md_path.write_text(_placeholder_md(md_title, csv_path), encoding="utf-8")
            stats["created_mds"] += 1
    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Bootstrap Dealix private-ops runtime scaffold.")
    p.add_argument(
        "--private-ops",
        default=os.environ.get("PRIVATE_OPS", os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix")),
        help="Private ops root (default: $PRIVATE_OPS or /opt/dealix).",
    )
    p.add_argument("--dry-run", action="store_true", help="Plan only; do not write files.")
    args = p.parse_args()

    private_ops = Path(args.private_ops).expanduser().resolve()
    try:
        stats = bootstrap(private_ops, dry_run=args.dry_run)
    except PermissionError as exc:
        print(f"PRIVATE_OPS_BOOTSTRAP=fail reason=permission_denied path={private_ops} err={exc}")
        print(
            f"  Hint: set PRIVATE_OPS to a writable path,"
            f" e.g. PRIVATE_OPS=$HOME/dealix-ops make bootstrap-runtime"
        )
        return 2
    except OSError as exc:
        print(f"PRIVATE_OPS_BOOTSTRAP=fail reason=os_error path={private_ops} err={exc}")
        return 2

    print(f"PRIVATE_OPS_BOOTSTRAP=ok path={private_ops}")
    print(f"  created_dirs={stats['created_dirs']}")
    print(f"  created_csvs={stats['created_csvs']}")
    print(f"  created_mds={stats['created_mds']}")
    print(f"  unchanged={stats['unchanged']}")
    if args.dry_run:
        print("  mode=dry_run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
