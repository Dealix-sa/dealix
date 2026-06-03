#!/usr/bin/env python3
"""Payment Handoff (Revenue Execution OS) — draft instruction, never a live link.

Creates ``draft_pending_approval`` handoffs for APPROVED proposals so the founder
can issue a Moyasar link / manual invoice himself. The OS never creates, sends,
or charges a payment link.

Usage:
    python scripts/generate_payment_handoff.py
    python scripts/generate_payment_handoff.py --approve pay_xxx
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution import payments  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Generate payment-handoff drafts (no live link).")
    p.add_argument("--approve", metavar="HANDOFF_ID", default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if args.approve:
        rec = payments.approve_handoff(args.approve)
        print(f"APPROVED: {args.approve} -> {rec['status'] if rec else 'NOT FOUND'}")

    summary = payments.run_generation()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("PAYMENT_HANDOFF:")
        print(f"  approved proposals : {summary['approved_proposals']}")
        print(f"  new handoffs       : {summary['new_handoffs']}")
        print(f"  policy             : {summary['policy']}")
        for hid in summary["ids"]:
            print(f"    - {hid}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"PAYMENT_HANDOFF: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
