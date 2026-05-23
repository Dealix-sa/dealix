#!/usr/bin/env python3
"""Generate the CEO Verification Brief from private-ops CSV evidence.

Reads counts from `$PRIVATE_OPS/{intelligence,outreach,sales,finance}`,
derives the current status, top failure, and a single next action, and
writes `$PRIVATE_OPS/founder/ceo_verification_brief.md`.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

POSITIVE_REPLY_TYPES = {"positive", "interested", "yes"}


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def derive_status(counts: dict[str, int]) -> tuple[str, str, str]:
    leads = counts["leads"]
    approved = counts["approved_outreach"]
    sent = counts["sent"]
    positive = counts["positive_replies"]
    proposals = counts["proposals"]
    payments = counts["payments"]

    if leads < 100:
        return (
            "C2 Runtime Ready / C3 Revenue Not Ready",
            "Lead intelligence below 100.",
            "Build 100 lead records in the top sector.",
        )
    if approved < 25:
        return (
            "C3 Revenue Partial",
            "Not enough approved outreach.",
            "Approve 25 high-fit outreach messages.",
        )
    if sent < 10:
        return (
            "C3 Outreach Ready",
            "Approved outreach exists but not enough sent/draft evidence.",
            "Create/send approved drafts.",
        )
    if positive > 0 and proposals == 0:
        return (
            "C3 Conversion Partial",
            "Positive replies exist but no proposal/sample path.",
            "Create samples and proposal queue.",
        )
    if proposals > 0 and payments == 0:
        return (
            "C3 Proposal Partial",
            "Proposals exist but no payment capture queue.",
            "Create payment follow-up queue.",
        )
    return (
        "C4 Operational",
        "None critical.",
        "Scale best-performing sector carefully.",
    )


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, type=Path)
    args = parser.parse_args()

    root = args.private_ops
    intel = _read_csv(root / "intelligence/lead_intelligence_base.csv")
    outreach = _read_csv(root / "outreach/outreach_queue.csv")
    conv = _read_csv(root / "outreach/conversation_log.csv")
    proposals = _read_csv(root / "sales/proposal_queue.csv")
    payments = _read_csv(root / "finance/payment_capture_queue.csv")

    approved = [
        r for r in outreach if (r.get("approval_status") or "").strip().lower() == "approved"
    ]
    sent = [r for r in outreach if (r.get("send_status") or "").strip().lower() == "sent"]
    positive = [
        r for r in conv if (r.get("reply_type") or "").strip().lower() in POSITIVE_REPLY_TYPES
    ]

    counts = {
        "leads": len(intel),
        "approved_outreach": len(approved),
        "sent": len(sent),
        "conversations": len(conv),
        "positive_replies": len(positive),
        "proposals": len(proposals),
        "payments": len(payments),
    }

    status, top_failure, next_action = derive_status(counts)

    body = f"""# CEO Verification Brief

## Date
{datetime.now(UTC).isoformat().replace("+00:00", "Z")}

## Status
{status}

## Top Failure / Constraint
{top_failure}

## Next Action
{next_action}

## Evidence Snapshot
- Lead intelligence: {counts['leads']}
- Approved outreach: {counts['approved_outreach']}
- Sent outreach: {counts['sent']}
- Conversations: {counts['conversations']}
- Positive replies: {counts['positive_replies']}
- Proposals: {counts['proposals']}
- Payment capture records: {counts['payments']}

## CEO Rule
Fix the top constraint before adding new systems.
"""

    out = root / "founder/ceo_verification_brief.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"PASS: wrote {out}")
    print(f"STATUS={status}")
    print(f"COUNTS={counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
