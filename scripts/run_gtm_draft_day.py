#!/usr/bin/env python3
"""Run a GTM draft day: research -> 250 drafts -> gate -> approval queue -> report.

Produces drafts only. Sends nothing (``MAX_AUTO_SENDS == 0``). With
``--dry-run`` it prints a summary and writes nothing to disk.

Usage:
  python3 scripts/run_gtm_draft_day.py --dry-run
  python3 scripts/run_gtm_draft_day.py --prospects path/to/prospects.jsonl --out reports/gtm
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.market_production_os import (  # noqa: E402
    DAILY_DRAFT_TARGET,
    MAX_AUTO_SENDS,
    Prospect,
    daily_gtm_report,
    produce_drafts,
    rank_for_approval,
    summarize_batch,
)

_DEFAULT_PROSPECTS = (
    REPO_ROOT
    / "auto_client_acquisition"
    / "market_production_os"
    / "seeds"
    / "prospects.sample.jsonl"
)
_DEFAULT_OFFERS = [
    "Free AI Ops Diagnostic",
    "7-Day Revenue Intelligence Sprint",
    "Data-to-Revenue Pack",
]


def _load_prospects(path: Path) -> list[Prospect]:
    prospects: list[Prospect] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        prospects.append(
            Prospect(
                prospect_id=str(row.get("prospect_id", "")),
                company=str(row.get("company", "")),
                sector=str(row.get("sector", "")),
                recipient_role=str(row.get("recipient_role", "")),
                source=str(row.get("source", "founder_supplied")),
                region=str(row.get("region", "Saudi Arabia")),
                score=int(row.get("score", 0)),
                state=str(row.get("state", "qualified")),
            )
        )
    return prospects


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a governed GTM draft day.")
    parser.add_argument("--prospects", type=Path, default=_DEFAULT_PROSPECTS)
    parser.add_argument("--target", type=int, default=DAILY_DRAFT_TARGET)
    parser.add_argument("--top-n", type=int, default=50)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "reports" / "gtm")
    parser.add_argument("--dry-run", action="store_true", help="print only; write nothing")
    args = parser.parse_args(argv)

    if not args.prospects.exists():
        print(f"prospects file not found: {args.prospects}", file=sys.stderr)
        return 2

    prospects = _load_prospects(args.prospects)
    drafts = produce_drafts(prospects, offers=_DEFAULT_OFFERS, target=args.target)
    summary = summarize_batch(drafts)
    queue = rank_for_approval(drafts, top_n=args.top_n)

    # Hard invariant: the factory never auto-sends.
    if summary["auto_sent"] != 0 or MAX_AUTO_SENDS != 0:
        print("DOCTRINE VIOLATION: auto-send detected", file=sys.stderr)
        return 1

    metrics = {
        "drafts_generated": summary["generated"],
        "drafts_quality_passed": summary["quality_passed"],
        "drafts_approved": 0,  # founder fills after review
        "emails_sent": 0,
        "auto_sent": summary["auto_sent"],
    }
    report = daily_gtm_report(metrics)

    print(f"prospects: {len(prospects)}")
    print(json.dumps(summary, ensure_ascii=False))
    print(f"approval queue (top {args.top_n}): {len(queue)} drafts")
    print(f"auto-send invariant: {'PASS' if summary['auto_sent'] == 0 else 'FAIL'}")

    if args.dry_run:
        print("[dry-run] nothing written")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "DAILY_GTM_REPORT.md").write_text(report, encoding="utf-8")
    (args.out / "APPROVAL_QUEUE.jsonl").write_text(
        "\n".join(json.dumps(d.to_dict(), ensure_ascii=False) for d in queue) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out / 'DAILY_GTM_REPORT.md'}")
    print(f"wrote {args.out / 'APPROVAL_QUEUE.jsonl'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
