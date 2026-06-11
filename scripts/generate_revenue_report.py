#!/usr/bin/env python3
"""Generate a revenue report from the deal ledger.

Output: reports/finance/revenue-report-YYYY-MM-DD.md
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.quote_engine import load_deals, load_quotes, load_invoices  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "reports" / "finance"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()

    deals = load_deals().get("deals", [])
    quotes = load_quotes().get("quotes", [])
    invoices = load_invoices().get("invoices", [])

    won = [d for d in deals if (d.get("status") or d.get("stage")) == "won"]
    lost = [d for d in deals if (d.get("status") or d.get("stage")) == "lost"]
    open_deals = [d for d in deals if (d.get("status") or d.get("stage")) not in ("won", "lost")]

    def _setup(d): return float(d.get("setup_value") or d.get("setupValue") or 0)
    def _mrr(d): return float(d.get("monthly_value") or d.get("monthlyValue") or 0)

    won_setup = sum(_setup(d) for d in won)
    won_mrr = sum(_mrr(d) for d in won)
    pipeline_mrr = sum(_mrr(d) for d in open_deals)
    pipeline_setup = sum(_setup(d) for d in open_deals)

    lines = [
        f"# Revenue report — {date}",
        "",
        "_Demo deals included; demo flag preserved in source data._",
        "",
        "## Summary",
        "",
        f"- Closed-won deals: **{len(won)}** | Setup: **{won_setup:,.0f} SAR** | MRR: **{won_mrr:,.0f} SAR**",
        f"- Open deals: **{len(open_deals)}** | Pipeline setup: **{pipeline_setup:,.0f} SAR** | Pipeline MRR: **{pipeline_mrr:,.0f} SAR**",
        f"- Lost deals: **{len(lost)}**",
        f"- Quotes registered: **{len(quotes)}** | Invoices (stubs): **{len(invoices)}**",
        "",
        "## Quote pipeline by status",
        "",
    ]
    status_counts = {}
    for q in quotes:
        status_counts[q.get("status", "?")] = status_counts.get(q.get("status", "?"), 0) + 1
    for k, v in sorted(status_counts.items()):
        lines.append(f"- {k}: **{v}**")
    if not quotes:
        lines.append("_No quotes registered yet._")

    lines.extend(
        [
            "",
            "## Note",
            "",
            "Revenue figures include demo deals so they reflect operating reality. Filter for `demo=false` in production reporting.",
        ]
    )

    out = OUT_DIR / f"revenue-report-{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
