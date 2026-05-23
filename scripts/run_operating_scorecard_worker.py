#!/usr/bin/env python3
"""Operating scorecard worker — read-only aggregator.

Aggregates ceo, sales, trust, and finance summaries into a single block
and (optionally) writes it to founder/operating_scorecard.md. Never sends
anything externally.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import List

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS", "/opt/dealix-ops-private")


def count_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    return max(0, len(rows) - 1)


def tally(path: Path, column: str) -> Counter:
    counter: Counter = Counter()
    if not path.exists():
        return counter
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            counter[(row.get(column) or "").strip() or "(unknown)"] += 1
    return counter


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--no-write", action="store_true")
    return parser.parse_args(argv)


def build_block(root: Path) -> List[str]:
    leads = count_rows(root / "intelligence/lead_intelligence_base.csv")
    queue = count_rows(root / "outreach/outreach_queue.csv")
    proposals = tally(root / "sales/proposal_queue.csv", "status")
    cash_entries = count_rows(root / "finance/cash_collected.csv")
    flags = tally(root / "trust/trust_flags.csv", "severity")
    pending_approvals = tally(
        root / "approvals/approval_queue.csv", "status"
    ).get("pending", 0)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        f"# Operating Scorecard — {now}",
        "",
        f"- leads                : {leads}",
        f"- outreach queue       : {queue}",
        f"- proposals (counts)   : {dict(proposals)}",
        f"- pending approvals    : {pending_approvals}",
        f"- cash entries         : {cash_entries}",
        f"- trust flags by sev   : {dict(flags)}",
        f"- source root          : {root}",
        "",
    ]
    return lines


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    block = build_block(root)
    print("\n".join(block))
    if not args.no_write:
        target = root / "founder/operating_scorecard.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            handle.write("\n".join(block) + "\n")
        print(f"appended to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
