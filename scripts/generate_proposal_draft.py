#!/usr/bin/env python3
"""Proposal Factory (Revenue Execution OS) — proposal drafts for qualified leads.

Pricing/scope/duration come from the canonical offers catalog (os/03_OFFERS.yml).
Proposals are ``draft_pending_approval`` — no contract or payment without approval.

Usage:
    python scripts/generate_proposal_draft.py
    python scripts/generate_proposal_draft.py --approve proposal_xxx
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
from dealix.distribution import proposals  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Generate proposal drafts from canonical offers.")
    p.add_argument("--prospects", type=Path, default=None)
    p.add_argument("--approve", metavar="PROPOSAL_ID", default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if args.approve:
        rec = proposals.approve_proposal(args.approve)
        print(f"APPROVED: {args.approve} -> {rec['status'] if rec else 'NOT FOUND'}")

    summary = proposals.run_generation(args.prospects)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("PROPOSAL_FACTORY:")
        print(f"  eligible prospects : {summary['eligible']}")
        print(f"  new proposals      : {summary['new_proposals']}")
        for pid in summary["ids"]:
            print(f"    - {pid}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"PROPOSAL_FACTORY: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
