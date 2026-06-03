"""Control tower brief generator.

Pulls inputs from the private ops tree and produces a single markdown brief.
"""
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sum_decimal(rows: list[dict], column: str) -> float:
    total = 0.0
    for row in rows:
        try:
            total += float((row.get(column) or "0").replace(",", ""))
        except ValueError:
            continue
    return total


def render(root: Path) -> str:
    pipeline = _read_csv(root / "pipeline" / "pipeline_tracker.csv")
    cash = _read_csv(root / "revenue" / "cash_collected.csv")
    proposals = _read_csv(root / "sales" / "proposal_tracker.csv")
    weighted = _read_csv(root / "revenue" / "pipeline_value.csv")
    mrr = _read_csv(root / "revenue" / "mrr_tracker.csv")
    approvals = _read_csv(root / "trust" / "approval_log.csv")

    open_approvals = [a for a in approvals if (a.get("decision") or "").strip().lower() == "pending"]
    open_proposals = [p for p in proposals if (p.get("status") or "").strip() in {"Sent", "Negotiating", "Verbal yes"}]

    money_section = (
        f"- Cash collected (all-time, confirmed): {_sum_decimal(cash, 'amount_sar'):,.0f} SAR\n"
        f"- Weighted pipeline value: {_sum_decimal(weighted, 'weighted_value'):,.0f} SAR\n"
        f"- MRR (active): {_sum_decimal(mrr, 'monthly_amount_sar'):,.0f} SAR/mo\n"
        f"- Open proposals: {len(open_proposals)}\n"
    )

    risks_section = (
        f"- Pending approvals: {len(open_approvals)}\n"
        f"- Pipeline opportunities: {len(pipeline)}\n"
    )

    top_action = "Refresh the action queue: `make ceo-action-queue`"
    for p in pipeline:
        if (p.get("priority") or "").strip() == "A":
            top_action = f"Move A-priority deal forward: {p.get('company','?')} -> {p.get('next_action','?')}"
            break

    today = dt.date.today().isoformat()
    return (
        f"# Control Tower Brief\nGenerated on: {today}\n\n"
        f"## Money\n{money_section}\n"
        f"## Risks\n{risks_section}\n"
        f"## Top action\n{top_action}\n\n"
        "## One bet\n(see weekly close output)\n\n"
        "## Constraints\n(none recorded)\n"
    )
