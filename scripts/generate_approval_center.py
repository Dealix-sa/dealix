#!/usr/bin/env python3
"""Generate the founder Approval Center v2 markdown surface.

Reads outreach / proposal / payment queues from the private-ops tree and
writes a single markdown approval center. Cross-references the existing
hard-coded NEVER_AUTO_EXECUTE set in dealix.classifications so that rows
matching a never-auto action type are flagged for explicit human approval.

This generator does NOT redefine approval policy. The source-of-truth
policy surface remains:
  - dealix/trust/approval.py (ApprovalCenter, ApprovalStatus)
  - dealix/classifications/__init__.py (NEVER_AUTO_EXECUTE, classify)
  - auto_client_acquisition/approval_center/ (renderer, store)

Source-of-truth spec: docs/runtime/REVENUE_FACTORY_RUNTIME_V2.md
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

try:
    from dealix.classifications import NEVER_AUTO_EXECUTE
except Exception:  # pragma: no cover — keep generator runnable in CI without full package install
    NEVER_AUTO_EXECUTE = frozenset()


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def flag(row: dict[str, str], field: str) -> str:
    value = (row.get(field) or "").strip().lower()
    if value in NEVER_AUTO_EXECUTE:
        return " **[NEVER_AUTO_EXECUTE]**"
    return ""


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
        help="Output markdown path (default: <private-ops>/founder/approval_center.md).",
    )
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()

    outreach = read_csv(root / "outreach/outreach_queue.csv")
    proposals = read_csv(root / "sales/proposal_queue.csv")
    payments = read_csv(root / "finance/payment_capture_queue.csv")

    pending_outreach = [
        r
        for r in outreach
        if (r.get("approval_status") or "").strip().lower() in {"pending", "needs edit"}
    ]
    pending_proposals = [
        r
        for r in proposals
        if (r.get("status") or "").strip().lower() in {"draft", "planned", "pending approval"}
    ]
    pending_payments = [
        r
        for r in payments
        if (r.get("status") or "").strip().lower() in {"planned", "waiting", "due"}
    ]

    lines: list[str] = [
        "# Approval Center",
        "",
        "## Date",
        date.today().isoformat(),
        "",
        "## Policy reference",
        "- `dealix/trust/approval.py` — approval surface and statuses.",
        "- `dealix/classifications/__init__.py` — `NEVER_AUTO_EXECUTE` set and (A,R,S) classifications.",
        "- `auto_client_acquisition/approval_center/` — renderer and store.",
        "",
        "## Outreach Pending Approval",
    ]
    if not pending_outreach:
        lines.append("(no outreach pending approval)")
        lines.append("")
    for i, r in enumerate(pending_outreach[:50], start=1):
        lines.extend([
            f"### {i}. {r.get('company', '')}{flag(r, 'channel')}",
            f"- Channel: {r.get('channel', '')}",
            f"- Message: {r.get('message', '')}",
            "- Action: Approve / Reject / Needs Edit",
            "",
        ])

    lines.append("## Proposals Pending Approval")
    if not pending_proposals:
        lines.append("(no proposals pending approval)")
        lines.append("")
    for i, r in enumerate(pending_proposals[:20], start=1):
        lines.extend([
            f"### {i}. {r.get('company', '')}{flag(r, 'proposal_type')}",
            f"- Type: {r.get('proposal_type', '')}",
            f"- Amount: {r.get('amount_sar', '')}",
            f"- Next: {r.get('next_action', '')}",
            "",
        ])

    lines.append("## Payment Follow-Ups")
    if not pending_payments:
        lines.append("(no payment follow-ups due)")
        lines.append("")
    for i, r in enumerate(pending_payments[:20], start=1):
        lines.extend([
            f"### {i}. {r.get('company', '')}",
            f"- Value: {r.get('proposal_value', '')}",
            f"- Stage: {r.get('followup_stage', '')}",
            f"- Next: {r.get('next_action', '')}",
            "",
        ])

    lines.extend([
        "## CEO Approval Rule",
        "External sending, proposal sending, pricing exceptions, proof, and A2/A3 actions require explicit approval.",
        "",
    ])

    out_path = Path(args.out) if args.out else (root / "founder/approval_center.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"PASS: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
