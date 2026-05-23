#!/usr/bin/env python3
"""Bootstrap the Dealix private ops runtime directory.

Creates the directory tree and CSV/Markdown headers used by the Founder
Console and Control Plane. Does **not** populate any real customer data;
the file is safe to run repeatedly (idempotent).

Default path: $DEALIX_PRIVATE_OPS or /opt/dealix-ops-private. Override
with --private-ops <path>.
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path


CSV_HEADERS: dict[str, list[str]] = {
    "intelligence/lead_intelligence_base.csv": [
        "lead_id",
        "company",
        "sector",
        "country",
        "size_band",
        "score",
        "source",
        "added_at",
        "notes",
    ],
    "outreach/outreach_queue.csv": [
        "outreach_id",
        "lead_id",
        "channel",
        "status",
        "draft",
        "approved_by",
        "approved_at",
        "queued_at",
    ],
    "outreach/conversation_log.csv": [
        "conversation_id",
        "lead_id",
        "channel",
        "direction",
        "classification",
        "summary",
        "occurred_at",
    ],
    "outreach/suppression_list.csv": [
        "contact",
        "reason",
        "added_at",
    ],
    "approvals/approval_queue.csv": [
        "id",
        "type",
        "class",
        "summary",
        "payload",
        "status",
        "created_at",
    ],
    "trust/approval_decisions.csv": [
        "id",
        "decision",
        "decided_at",
        "reason",
        "approved_by",
        "evidence",
        "class",
    ],
    "trust/trust_flags.csv": [
        "flag_id",
        "type",
        "severity",
        "detail",
        "status",
        "raised_at",
    ],
    "trust/agent_toggles.csv": [
        "agent_id",
        "decision",
        "decided_at",
        "reason",
    ],
    "sales/proposal_queue.csv": [
        "proposal_id",
        "lead_id",
        "stage",
        "status",
        "value",
        "probability",
        "due_at",
    ],
    "finance/payment_capture_queue.csv": [
        "payment_id",
        "customer",
        "amount",
        "status",
        "due_at",
        "notes",
    ],
    "finance/cash_collected.csv": [
        "payment_id",
        "customer",
        "amount",
        "mrr",
        "collected_at",
    ],
    "runtime/worker_state.csv": [
        "worker",
        "last_run",
        "status",
        "failures_24h",
        "next_run",
        "notes",
    ],
    "distribution/channel_scorecard.csv": [
        "channel",
        "leads",
        "approved",
        "won",
        "roi",
        "as_of",
    ],
    "distribution/sector_scorecard.csv": [
        "sector",
        "signal",
        "as_of",
    ],
    "delivery/delivery_queue.csv": [
        "id",
        "customer",
        "stage",
        "status",
        "owner",
        "due_at",
    ],
    "retention/retention_queue.csv": [
        "customer",
        "health",
        "next_action",
        "owner",
        "renewal_at",
    ],
    "proof/proof_library.csv": [
        "id",
        "title",
        "customer",
        "anonymized",
        "status",
        "approved_at",
    ],
    "evals/eval_status.csv": [
        "suite",
        "agent",
        "status",
        "score",
        "ran_at",
    ],
    "product/productization_candidates.csv": [
        "name",
        "repeats",
        "owner",
        "status",
        "first_seen_at",
    ],
    "security/security_status.csv": [
        "check",
        "status",
        "detail",
        "checked_at",
    ],
}

MD_FILES: dict[str, str] = {
    "founder/operating_scorecard.md": (
        "# Operating Scorecard\n\nPlaceholder. "
        "Generate with: python scripts/generate_operating_scorecard.py\n"
    ),
}


def ensure_csv(path: Path, headers: list[str]) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
    return True


def ensure_text(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def bootstrap(root: Path) -> dict[str, int]:
    created_csv = 0
    created_md = 0
    for rel, headers in CSV_HEADERS.items():
        if ensure_csv(root / rel, headers):
            created_csv += 1
    for rel, content in MD_FILES.items():
        if ensure_text(root / rel, content):
            created_md += 1
    return {"csv_created": created_csv, "md_created": created_md}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
        help="Target private ops root (default: $DEALIX_PRIVATE_OPS or /opt/dealix-ops-private)",
    )
    args = parser.parse_args()
    root = Path(args.private_ops)
    root.mkdir(parents=True, exist_ok=True)
    stats = bootstrap(root)
    print(f"[bootstrap_private_ops_runtime] root={root}")
    print(f"[bootstrap_private_ops_runtime] csv_created={stats['csv_created']}")
    print(f"[bootstrap_private_ops_runtime] md_created={stats['md_created']}")
    print(f"[bootstrap_private_ops_runtime] total_files_expected={len(CSV_HEADERS) + len(MD_FILES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
