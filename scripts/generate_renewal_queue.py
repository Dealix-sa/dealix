#!/usr/bin/env python3
"""Renewal & Upsell Queue (Revenue Execution OS) — the second sale.

Builds renewal/upsell records for delivered (won) clients using the canonical
offers ladder. Enforces "no upsell before proof" (skips clients below L1).

Usage:
    python scripts/generate_renewal_queue.py
    python scripts/generate_renewal_queue.py --today 2026-06-02
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution import renewals  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Generate the renewal/upsell queue.")
    p.add_argument("--prospects", type=Path, default=None)
    p.add_argument("--today", type=date.fromisoformat, default=None, help="YYYY-MM-DD")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    summary = renewals.run_generation(args.prospects, today=args.today)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("RENEWAL_QUEUE:")
        print(f"  won clients        : {summary['won_clients']}")
        print(f"  new renewals       : {summary['new_renewals']}")
        print(f"  skipped (no proof) : {summary['skipped_no_proof']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"RENEWAL_QUEUE: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
