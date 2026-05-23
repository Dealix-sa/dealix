#!/usr/bin/env python3
"""CEO summary worker — read-only.

Reads private-ops CSVs and prints a single founder brief to stdout. With
--write-scorecard, appends the brief to founder/operating_scorecard.md.
Never sends anything externally.

Usage:
    python scripts/run_ceo_summary_worker.py --root /opt/dealix-ops-private
    python scripts/run_ceo_summary_worker.py --root /opt/dealix-ops-private --write-scorecard
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS", "/opt/dealix-ops-private")


def count_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    return max(0, len(rows) - 1)


def count_matching(path: Path, column: str, values: Iterable[str]) -> int:
    if not path.exists():
        return 0
    wanted = set(values)
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if (row.get(column) or "").strip() in wanted:
                count += 1
    return count


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--write-scorecard", action="store_true")
    return parser.parse_args(argv)


def build_summary(root: Path) -> List[str]:
    leads = count_rows(root / "intelligence/lead_intelligence_base.csv")
    outreach_queue = count_rows(root / "outreach/outreach_queue.csv")
    pending_approvals = count_matching(
        root / "approvals/approval_queue.csv", "status", ["pending"]
    )
    proposals = count_rows(root / "sales/proposal_queue.csv")
    cash_entries = count_rows(root / "finance/cash_collected.csv")
    open_incidents = count_matching(
        root / "trust/incidents.csv", "status", ["open"]
    )
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return [
        f"# CEO Summary — {now}",
        "",
        f"- leads in pipeline      : {leads}",
        f"- outreach queue size    : {outreach_queue}",
        f"- pending approvals      : {pending_approvals}",
        f"- proposals in flight    : {proposals}",
        f"- cash-collected entries : {cash_entries}",
        f"- open incidents         : {open_incidents}",
        f"- source root            : {root}",
        "",
    ]


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    summary = build_summary(root)
    print("\n".join(summary))
    if args.write_scorecard:
        target = root / "founder/operating_scorecard.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            handle.write("\n".join(summary) + "\n")
        print(f"appended to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
