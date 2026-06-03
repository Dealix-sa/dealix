"""Priority router for the executive control plane.

Scores candidate actions by money proximity, reversibility cost, time decay,
and founder-bottleneck weight. Returns the ordered queue.
"""
from __future__ import annotations

import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Candidate:
    source: str
    description: str
    money_proximity: float
    reversibility_cost: float
    time_decay: float
    founder_bottleneck: bool
    raw_score: float = 0.0


WEIGHTS = {
    "money_proximity": 0.45,
    "reversibility_cost": 0.20,
    "time_decay": 0.20,
    "founder_bottleneck": 0.15,
}


def score(candidate: Candidate) -> float:
    raw = (
        WEIGHTS["money_proximity"] * candidate.money_proximity
        + WEIGHTS["reversibility_cost"] * candidate.reversibility_cost
        + WEIGHTS["time_decay"] * candidate.time_decay
        + WEIGHTS["founder_bottleneck"] * (1.0 if candidate.founder_bottleneck else 0.0)
    )
    candidate.raw_score = raw
    return raw


def candidates_from_pipeline(path: Path) -> list[Candidate]:
    out: list[Candidate] = []
    if not path.exists():
        return out
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            stage = (row.get("stage") or "").strip()
            priority = (row.get("priority") or "C").strip()
            money_proximity = {
                "New": 0.2,
                "Qualified": 0.4,
                "Sample sent": 0.6,
                "Proposal sent": 0.8,
                "Verbal yes": 0.95,
                "Closed-won": 0.0,
                "Closed-lost": 0.0,
            }.get(stage, 0.3)
            priority_boost = {"A": 0.2, "B": 0.1, "C": 0.0}.get(priority, 0.0)
            money_proximity = min(1.0, money_proximity + priority_boost)
            time_decay = _decay(row.get("last_touch", ""))
            out.append(
                Candidate(
                    source=path.name,
                    description=f"{row.get('company','?')} - {row.get('next_action','?')}",
                    money_proximity=money_proximity,
                    reversibility_cost=0.4,
                    time_decay=time_decay,
                    founder_bottleneck=True,
                )
            )
    return out


def _decay(last_touch: str) -> float:
    try:
        when = dt.date.fromisoformat(last_touch)
    except (ValueError, TypeError):
        return 0.5
    days = (dt.date.today() - when).days
    return min(1.0, max(0.0, days / 14.0))


def rank(candidates: list[Candidate]) -> list[Candidate]:
    for c in candidates:
        score(c)
    return sorted(candidates, key=lambda c: c.raw_score, reverse=True)
