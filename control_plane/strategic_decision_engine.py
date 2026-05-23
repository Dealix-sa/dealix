"""Strategic decision engine.

Helps the founder choose the weekly bet by combining last week's metrics
with the open experiments backlog.
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


def recommend_weekly_bet(root: Path) -> str:
    metrics = _read_csv(root / "metrics_history" / "weekly_metrics.csv")
    experiments = _read_csv(root / "experiments" / "market_experiments.csv")

    last = metrics[-1] if metrics else None
    leads = int((last or {}).get("leads", 0) or 0) if last else 0
    proposals = int((last or {}).get("proposals", 0) or 0) if last else 0
    paid = float((last or {}).get("cash_collected_sar", 0) or 0) if last else 0.0

    if paid == 0 and proposals == 0:
        bet = "Get to 1 paid (or written-approved) deal this week."
    elif proposals < 2:
        bet = "Move 2 qualified opportunities to proposal stage this week."
    elif leads < 25:
        bet = "Restock the top of pipeline: add 25 qualified leads."
    else:
        bet = "Convert a top-of-pipeline lead to a sample-to-proposal path."

    open_experiments = [
        e for e in experiments if (e.get("decision") or "").strip().lower() in {"", "pending"}
    ]
    if open_experiments:
        bet += f" Open experiments: {len(open_experiments)}; close at least one."

    today = dt.date.today().isoformat()
    return f"# Weekly Bet Recommendation\nGenerated on: {today}\n\n{bet}\n"
