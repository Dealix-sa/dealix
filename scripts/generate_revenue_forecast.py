"""Bottom-up revenue forecast from the private_ops graph.

Reads:
    graph/accounts.csv      (id, name, stage, expected_value_sar, close_probability, close_date)
    graph/offers.csv        (id, name, list_price_sar)
    finance/cash_collected.csv (date, amount_sar)
Outputs a markdown forecast: weighted pipeline by month + cash-in trend.
"""
from __future__ import annotations

import sys
import datetime as _dt
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _private_ops_runtime import (  # noqa: E402
    ledger_path,
    parse_args,
    read_csv,
    today_iso,
    write_or_print,
)


def _f(s: str | None) -> float:
    try:
        return float((s or "0").replace(",", "").replace("SAR", "").strip())
    except (TypeError, ValueError):
        return 0.0


def _month_key(s: str | None) -> str:
    if not s:
        return "unknown"
    try:
        return _dt.date.fromisoformat(s).strftime("%Y-%m")
    except ValueError:
        return "unknown"


def main() -> int:
    args = parse_args("generate_revenue_forecast")
    po = args.private_ops

    accounts_p = ledger_path(po, "graph", "accounts.csv")
    cash_p = ledger_path(po, "finance", "cash_collected.csv")

    _, accounts = read_csv(accounts_p)
    _, cash = read_csv(cash_p)

    if args.strict and not accounts:
        print(f"[strict] no rows in {accounts_p}", file=sys.stderr)
        return 1

    weighted: dict[str, float] = defaultdict(float)
    for r in accounts:
        value = _f(r.get("expected_value_sar"))
        prob = _f(r.get("close_probability")) / 100.0 if _f(r.get("close_probability")) > 1 \
            else _f(r.get("close_probability"))
        month = _month_key(r.get("close_date"))
        weighted[month] += value * max(0.0, min(1.0, prob))

    lines = [f"# Revenue Forecast — {today_iso()}\n",
             "Source: private_ops/graph/accounts.csv + finance/cash_collected.csv (read-only).\n",
             "Bottom-up weighted pipeline (expected_value_sar × close_probability):\n",
             "## Weighted pipeline by close month\n"]
    if not weighted:
        lines.append("- (no pipeline rows)\n")
    else:
        lines.append("| Month | Weighted (SAR) |")
        lines.append("|---|---:|")
        for month in sorted(weighted):
            lines.append(f"| {month} | {weighted[month]:,.0f} |")
        total = sum(weighted.values())
        lines.append(f"| **Total** | **{total:,.0f}** |")

    lines.append("\n## Cash collected by month\n")
    by_month: dict[str, float] = defaultdict(float)
    for r in cash:
        by_month[_month_key(r.get("date"))] += _f(r.get("amount_sar"))
    if not by_month:
        lines.append("- (no cash entries yet)\n")
    else:
        lines.append("| Month | Cash in (SAR) |")
        lines.append("|---|---:|")
        for month in sorted(by_month):
            lines.append(f"| {month} | {by_month[month]:,.0f} |")

    write_or_print("\n".join(lines), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
