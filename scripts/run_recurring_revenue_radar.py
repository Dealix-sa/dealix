#!/usr/bin/env python3
"""Daily Recurring Revenue Radar — surface one-off → retainer expansion.

Loads the book of business, ranks expansion opportunities (within doctrine:
no revenue before paid, proof before upsell, approval-first), writes a bilingual
founder brief, and records the run to the radar ledger.

Account source (first that exists wins):
  1. ``--accounts <path>``
  2. ``data/recurring_revenue/accounts_seed.json``  (your real book — gitignored)
  3. ``data/demo/recurring_revenue_accounts_seed.json``  (synthetic demo)

Outputs:
  * ``data/founder_briefs/recurring_revenue_radar_<YYYY-MM-DD>.md``  (brief)
  * appends a compact snapshot to ``data/recurring_revenue/radar_log.json``

No external sends. Prints ``DEALIX_RECURRING_REVENUE_RADAR=OK`` on success.
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.revenue_ops_autopilot.recurring_revenue_radar import (  # noqa: E402
    AccountSnapshot,
    RecurringRevenueRadar,
    RecurringRevenueRadarLedger,
    load_accounts_from_file,
    render_radar_markdown,
)

_REAL_SEED = ROOT / "data" / "recurring_revenue" / "accounts_seed.json"
_DEMO_SEED = ROOT / "data" / "demo" / "recurring_revenue_accounts_seed.json"
_BRIEFS_DIR = ROOT / "data" / "founder_briefs"


def _resolve_accounts(explicit: str | None) -> tuple[list[AccountSnapshot], str]:
    for candidate in (Path(explicit) if explicit else None, _REAL_SEED, _DEMO_SEED):
        if candidate and candidate.is_file():
            return load_accounts_from_file(candidate), str(candidate.relative_to(ROOT))
    return [], "(none)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Daily Recurring Revenue Radar")
    parser.add_argument("--accounts", default=None, help="Path to a portfolio JSON seed file.")
    parser.add_argument("--top-n", type=int, default=10, help="Opportunities to show in the brief.")
    parser.add_argument("--no-write", action="store_true", help="Do not write brief or ledger.")
    parser.add_argument("--json", action="store_true", help="Print the full summary as JSON.")
    args = parser.parse_args(argv)

    accounts, source = _resolve_accounts(args.accounts)
    summary = RecurringRevenueRadar().evaluate(accounts)
    md = render_radar_markdown(summary, top_n=args.top_n)

    brief_path = None
    if not args.no_write:
        day = datetime.now(UTC).strftime("%Y-%m-%d")
        _BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
        brief_path = _BRIEFS_DIR / f"recurring_revenue_radar_{day}.md"
        brief_path.write_text(md, encoding="utf-8")
        RecurringRevenueRadarLedger().append_run(summary)

    if args.json:
        print(summary.model_dump_json(indent=2))
    else:
        print(md)

    print("─" * 60)
    print(f"source: {source}")
    print(
        f"accounts={summary.accounts_total} "
        f"opportunities={summary.opportunities_count} "
        f"realised_mrr={summary.realized_mrr_sar:,.0f} SAR "
        f"pipeline_mrr={summary.pipeline_incremental_mrr_sar:,.0f} SAR "
        f"pipeline_arr={summary.pipeline_incremental_arr_sar:,.0f} SAR"
    )
    if brief_path:
        print(f"brief: {brief_path.relative_to(ROOT)}")
    print("DEALIX_RECURRING_REVENUE_RADAR=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
