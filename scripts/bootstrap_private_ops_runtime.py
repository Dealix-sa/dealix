#!/usr/bin/env python3
"""Bootstrap the Dealix private-ops runtime tree.

Creates the directory layout + empty CSVs (with headers) that the
Founder Console internal API reads. Idempotent: re-running is safe and
will not overwrite existing data.

Usage::

    python scripts/bootstrap_private_ops_runtime.py \\
        --private-ops /opt/dealix-ops-private

or:

    make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

# (relative_path, [headers])
CSV_FILES: list[tuple[str, list[str]]] = [
    ("intelligence/lead_intelligence_base.csv",
     ["id", "company", "sector", "stage", "score", "evidence_ref", "owner", "updated_at"]),
    ("outreach/outreach_queue.csv",
     ["id", "lead_id", "channel", "status", "draft_ref", "approval_id", "created_at"]),
    ("outreach/conversation_log.csv",
     ["id", "lead_id", "direction", "channel", "summary", "ts"]),
    ("outreach/suppression_list.csv",
     ["company", "reason", "added_at"]),
    ("approvals/approval_queue.csv",
     ["id", "action", "target", "draft_ref", "policy_class", "status", "created_at"]),
    ("trust/approval_decisions.csv",
     ["id", "approval_id", "decision", "reason", "decided_by", "decided_at", "policy_class"]),
    ("trust/trust_flags.csv",
     ["id", "category", "severity", "status", "target", "opened_at"]),
    ("trust/incidents.csv",
     ["id", "kind", "target", "reason", "opened_at", "opened_by", "status"]),
    ("sales/proposal_queue.csv",
     ["id", "customer", "offer", "status", "amount_sar", "updated_at"]),
    ("finance/payment_capture_queue.csv",
     ["id", "invoice_id", "amount_sar", "status", "due_at"]),
    ("finance/cash_collected.csv",
     ["id", "invoice_id", "amount_sar", "collected_at"]),
    ("finance/ai_unit_economics.csv",
     ["period", "agent", "cost_sar", "revenue_attributed_sar"]),
    ("runtime/worker_state.csv",
     ["worker", "last_run", "status", "failures_24h", "next_run", "notes"]),
    ("distribution/channel_scorecard.csv",
     ["channel", "replies", "proposals", "cash_sar"]),
    ("distribution/sector_scorecard.csv",
     ["sector", "replies", "proposals", "cash_sar"]),
    ("evals/eval_status.csv",
     ["suite", "status", "last_run", "fail_count"]),
    ("product/productization_candidates.csv",
     ["id", "theme", "customer_count", "status", "owner"]),
    ("security/security_status.csv",
     ["item", "status", "checked_at"]),
]

MD_FILES: list[tuple[str, str]] = [
    ("founder/operating_scorecard.md", "# Operating Scorecard\n\n_Not generated yet. Run `make operating-scorecard`._\n"),
    ("founder/sovereign_readiness.md", "# Sovereign Readiness\n\n_Not generated yet. Run `make sovereign-readiness`._\n"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
        help="Private ops root directory (default: $DEALIX_PRIVATE_OPS or /opt/dealix-ops-private).",
    )
    args = parser.parse_args()

    root = Path(args.private_ops)
    try:
        root.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"[FAIL] cannot create {root}: permission denied", file=sys.stderr)
        return 2

    created = 0
    skipped = 0

    for rel, headers in CSV_FILES:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            skipped += 1
            continue
        with path.open("w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerow(headers)
        created += 1

    for rel, content in MD_FILES:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            skipped += 1
            continue
        path.write_text(content, encoding="utf-8")
        created += 1

    print(f"[OK] bootstrap complete at {root}")
    print(f"     created={created}  skipped(existing)={skipped}")
    print("     next: export DEALIX_PRIVATE_OPS=" + str(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
