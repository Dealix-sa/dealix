"""Business audit / CEO business score generator."""
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_score(root: Path) -> tuple[int, str]:
    """Return (score, top_action). Score is 0-100."""
    pipeline = _read_csv(root / "pipeline" / "pipeline_tracker.csv")
    cash = _read_csv(root / "revenue" / "cash_collected.csv")
    proposals = _read_csv(root / "sales" / "proposal_tracker.csv")
    evidence = _read_csv(root / "evidence" / "execution_evidence_ledger.csv")

    score = 0
    if any((c.get("status") or "").strip().lower() == "confirmed" for c in cash):
        score += 30
    if any((p.get("status") or "").strip() in {"Sent", "Negotiating", "Verbal yes"} for p in proposals):
        score += 20
    if len(pipeline) >= 25:
        score += 20
    if len(evidence) >= 5:
        score += 15
    if any((p.get("priority") or "").strip() == "A" for p in pipeline):
        score += 15

    if score < 30:
        top_action = "Get 25 leads into the pipeline tracker."
    elif score < 60:
        top_action = "Move a sample to a proposal this week."
    elif score < 85:
        top_action = "Close the open proposal or move to the next bet."
    else:
        top_action = "Repeat the offer: find 2 more clients like the last one."

    return score, top_action


def render(root: Path) -> str:
    score, top_action = compute_score(root)
    today = dt.date.today().isoformat()
    return (
        f"# CEO Business Score\nGenerated on: {today}\n\n"
        f"## Score: {score}/100\n\n"
        f"## Top action\n{top_action}\n"
    )
