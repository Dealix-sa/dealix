"""Finance V2 runtime — produces a finance command report and pricing review."""
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sum(rows: list[dict], col: str) -> float:
    total = 0.0
    for r in rows:
        try:
            total += float((r.get(col) or "0").replace(",", ""))
        except ValueError:
            continue
    return total


def render_finance_command_report(root: Path) -> str:
    cash = _read(root / "revenue" / "cash_collected.csv")
    expenses = _read(root / "finance" / "expenses.csv")
    unit = _read(root / "finance" / "unit_economics.csv")

    total_cash = _sum(cash, "amount_sar")
    total_expenses = _sum(expenses, "amount_sar")
    total_gm = _sum(unit, "gross_margin_sar")
    today = dt.date.today().isoformat()
    return (
        f"# Finance Command Report\nGenerated on: {today}\n\n"
        f"## Totals\n"
        f"- Cash collected (lifetime, confirmed): {total_cash:,.0f} SAR\n"
        f"- Expenses (lifetime): {total_expenses:,.0f} SAR\n"
        f"- Gross margin tracked: {total_gm:,.0f} SAR\n\n"
        f"## Engagements with unit economics: {len(unit)}\n"
    )


def render_pricing_review(root: Path) -> str:
    unit = _read(root / "finance" / "unit_economics.csv")
    proposals = _read(root / "sales" / "proposal_tracker.csv")
    discounts = _read(root / "finance" / "discount_log.csv")
    today = dt.date.today().isoformat()
    lines = [
        f"# Pricing Review\nGenerated on: {today}\n",
        f"## Engagements: {len(unit)}",
        f"## Active proposals: {sum(1 for p in proposals if (p.get('status') or '').strip() in ('Sent','Negotiating','Verbal yes'))}",
        f"## Discount events: {len(discounts)}",
        "",
        "## Recommendations",
    ]
    if len(discounts) > 3:
        lines.append("- Discount frequency > 3 — review list pricing")
    if len(unit) >= 3:
        lines.append("- 3+ engagements logged — recompute effective hourly per rung")
    if not lines[-1].startswith("##") and not lines[-1].startswith("-"):
        lines.append("- (no automated recommendations this cycle)")
    return "\n".join(lines) + "\n"
