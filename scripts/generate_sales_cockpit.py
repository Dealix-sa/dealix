#!/usr/bin/env python3
"""Generate the founder Sales Cockpit v2 markdown surface.

Reads commercial CSVs from the private-ops tree and writes a single
markdown cockpit. Source-of-truth spec: docs/control_plane/SALES_COCKPIT_V2.md.

Complementary to (does NOT replace) dealix/commercial_ops/founder_cockpit.py —
this generator emits a markdown artifact under docs/founder/sales_cockpit.md
that the founder can scan in seconds without searching raw CSVs.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def count(rows: list[dict[str, str]], field: str, values: set[str]) -> int:
    needle = {v.lower() for v in values}
    return sum(1 for r in rows if (r.get(field) or "").strip().lower() in needle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        required=True,
        help="Path to private-ops root (e.g. /opt/dealix-ops-private).",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output markdown path (default: <private-ops>/founder/sales_cockpit.md).",
    )
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()

    accounts = read_csv(root / "growth/market_accounts.csv")
    intel = read_csv(root / "intelligence/lead_intelligence_base.csv")
    outreach = read_csv(root / "outreach/outreach_queue.csv")
    conversations = read_csv(root / "outreach/conversation_log.csv")
    proposals = read_csv(root / "sales/proposal_queue.csv")
    payments = read_csv(root / "finance/payment_capture_queue.csv")
    retention = read_csv(root / "client_success/retention_queue.csv")
    suppression = read_csv(root / "outreach/suppression_list.csv")

    pending_approval = count(outreach, "approval_status", {"pending", "needs edit"})
    approved_ready = sum(
        1
        for r in outreach
        if (r.get("approval_status") or "").strip().lower() == "approved"
        and (r.get("send_status") or "").strip().lower() in {"ready", "draft"}
    )
    positive = count(conversations, "reply_type", {"positive", "interested", "yes"})
    proposal_due = count(proposals, "status", {"planned", "draft"})
    payment_due = count(payments, "status", {"planned", "waiting", "due"})

    if pending_approval:
        top_action = "Review outreach approvals."
    elif approved_ready:
        top_action = "Create/send approved drafts."
    elif positive:
        top_action = "Prepare samples for positive replies."
    elif proposal_due:
        top_action = "Review proposal drafts."
    elif payment_due:
        top_action = "Push payment / PO follow-up."
    elif len(intel) < 500:
        top_action = "Grow lead intelligence base toward 500."
    else:
        top_action = "Run sector experiment review."

    lines = [
        "# Sales Cockpit",
        "",
        "## Date",
        date.today().isoformat(),
        "",
        "## Top CEO Action",
        top_action,
        "",
        "## Commercial Snapshot",
        f"- Market accounts: {len(accounts)}",
        f"- Lead intelligence records: {len(intel)}",
        f"- Outreach pending approval: {pending_approval}",
        f"- Approved ready/draft outreach: {approved_ready}",
        f"- Conversations logged: {len(conversations)}",
        f"- Positive replies: {positive}",
        f"- Proposal queue: {len(proposals)}",
        f"- Payment capture queue: {len(payments)}",
        f"- Retention queue: {len(retention)}",
        f"- Suppression records: {len(suppression)}",
        "",
        "## Decision",
        "Approve / Send Drafts / Prepare Sample / Approve Proposal / Push Payment / Build More Leads",
        "",
        "## CEO Rule",
        "Do the top action before adding systems.",
        "",
    ]

    out_path = Path(args.out) if args.out else (root / "founder/sales_cockpit.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"PASS: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
