"""Productization candidate scorer."""
from __future__ import annotations

import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Candidate:
    workflow: str
    frequency: int
    manual_time_hours: float
    automation_value: float
    priority: str
    owner: str
    score: float = 0.0


def score(c: Candidate) -> float:
    freq = min(c.frequency, 20) / 20.0
    time = min(c.manual_time_hours, 8.0) / 8.0
    value = max(0.0, min(c.automation_value, 1.0))
    priority_boost = {"A": 0.2, "B": 0.1, "C": 0.0}.get(c.priority.strip().upper(), 0.0)
    base = 0.4 * freq + 0.3 * time + 0.3 * value
    c.score = min(1.0, base + priority_boost) * 100.0
    return c.score


def candidates_from_csv(path: Path) -> list[Candidate]:
    out: list[Candidate] = []
    if not path.exists():
        return out
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                out.append(
                    Candidate(
                        workflow=row.get("workflow", ""),
                        frequency=int((row.get("frequency") or "0") or 0),
                        manual_time_hours=float((row.get("manual_time_hours") or "0") or 0),
                        automation_value=float((row.get("automation_value") or "0") or 0),
                        priority=row.get("priority", "C"),
                        owner=row.get("owner", ""),
                    )
                )
            except (ValueError, KeyError):
                continue
    return out


def rank(candidates: list[Candidate]) -> list[Candidate]:
    for c in candidates:
        score(c)
    return sorted(candidates, key=lambda c: c.score, reverse=True)


def render_review(root: Path) -> str:
    cands = candidates_from_csv(root / "productization" / "candidates.csv")
    ranked = rank(cands)
    today = dt.date.today().isoformat()
    lines = [f"# Productization Review\nGenerated on: {today}\n", f"## Candidates: {len(ranked)}"]
    for i, c in enumerate(ranked[:10], start=1):
        lines.append(f"{i}. [{c.score:.1f}] {c.workflow} ({c.priority}, owner={c.owner})")
    if not ranked:
        lines.append("- (no candidates yet — log them in productization/candidates.csv)")
    return "\n".join(lines) + "\n"
