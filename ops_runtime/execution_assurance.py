"""Execution assurance reader.

Scores how disciplined the founder's operating loops have been recently by
counting the presence of weekly review, daily close, and approval logs.
"""

from __future__ import annotations

from pathlib import Path

ASSURANCE_CHECKS = [
    ("founder/mission_control.md", 10),
    ("founder/operating_calendar.md", 10),
    ("learning/company_memory.md", 15),
    ("revenue/revenue_action_log.csv", 15),
    ("revenue/pipeline_tracker.csv", 15),
    ("trust/approval_log.csv", 15),
    ("founder/ceo_audit_trail.csv", 10),
    ("experiments/market_experiments.csv", 10),
]


def calculate_execution_assurance(private_ops_root: str) -> dict:
    root = Path(private_ops_root).resolve()
    score = 0
    missing: list[str] = []
    for relative, weight in ASSURANCE_CHECKS:
        if (root / relative).exists():
            score += weight
        else:
            missing.append(relative)
    score = min(score, 100)

    if score >= 80:
        status = "STRONG"
    elif score >= 50:
        status = "FORMING"
    else:
        status = "WEAK"

    return {
        "score": score,
        "status": status,
        "missing": missing,
    }
