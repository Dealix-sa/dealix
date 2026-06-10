"""Minimal CEO business score calculator.

Reads simple CSV / markdown evidence from a private-ops directory and emits a
dict of metrics + a 0-100 score. Designed to be safe when files are missing
(returns zeros) so the control tower can still produce a posture signal.

Expected layout under <private_ops>/:
    pipeline/leads.csv              one row per lead (contacted, replied columns)
    revenue/revenue_action_log.csv  one row per revenue action (type column)
    delivery/delivery_log.csv       one row per delivery (status column)
    finance/cash_log.csv            one row per cash event (amount column)
    business_audit/ceo_business_score.md (written by this module)
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict


def _read_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def _count_truthy(rows: list[dict], column: str) -> int:
    return sum(1 for r in rows if str(r.get(column, "")).strip().lower() in {"1", "true", "yes", "y"})


def _count_value(rows: list[dict], column: str, value: str) -> int:
    target = value.strip().lower()
    return sum(1 for r in rows if str(r.get(column, "")).strip().lower() == target)


def _sum_float(rows: list[dict], column: str) -> float:
    total = 0.0
    for r in rows:
        raw = str(r.get(column, "")).strip()
        if not raw:
            continue
        try:
            total += float(raw)
        except ValueError:
            continue
    return total


def calculate_business_score(private_ops: str) -> Dict:
    root = Path(private_ops).resolve()

    leads = _read_csv_rows(root / "pipeline" / "leads.csv")
    revenue_actions = _read_csv_rows(root / "revenue" / "revenue_action_log.csv")
    deliveries = _read_csv_rows(root / "delivery" / "delivery_log.csv")
    cash_events = _read_csv_rows(root / "finance" / "cash_log.csv")

    metrics = {
        "lead_count": len(leads),
        "contacted": _count_truthy(leads, "contacted"),
        "replied": _count_truthy(leads, "replied"),
        "sample_sent": _count_value(revenue_actions, "type", "sample"),
        "proposal_sent": _count_value(revenue_actions, "type", "proposal"),
        "payment_pursued": _count_value(revenue_actions, "type", "payment"),
        "paid": _count_value(deliveries, "status", "paid")
                + _count_value(deliveries, "status", "delivered"),
        "delivered": _count_value(deliveries, "status", "delivered"),
        "qa_pass": _count_value(deliveries, "qa", "pass"),
        "feedback_received": _count_truthy(deliveries, "feedback"),
        "cash_collected": _sum_float(cash_events, "amount"),
    }

    weights = {
        "lead_count":      (25, 15),   # (target, points)
        "contacted":       (25, 15),
        "replied":         (3, 10),
        "sample_sent":     (3, 10),
        "proposal_sent":   (1, 15),
        "payment_pursued": (1, 10),
        "delivered":       (1, 10),
        "qa_pass":         (1, 10),
        "feedback_received": (1, 5),
    }
    total = 0
    for key, (target, points) in weights.items():
        actual = metrics.get(key, 0)
        if target <= 0:
            continue
        total += int(round(points * min(actual / target, 1.0)))
    total = max(0, min(100, total))

    score = {
        "total_score": total,
        "metrics": metrics,
        "private_ops": str(root),
    }

    _write_score_markdown(root, score)
    return score


def _write_score_markdown(root: Path, score: dict) -> None:
    out_dir = root / "business_audit"
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics = score["metrics"]
    lines = [
        "# CEO Business Score",
        "",
        f"## Total Score: {score['total_score']} / 100",
        "",
        "## Metrics",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in metrics.items():
        if isinstance(value, float):
            display = f"{value:,.2f}"
        else:
            display = str(value)
        lines.append(f"| {key} | {display} |")
    (out_dir / "ceo_business_score.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
