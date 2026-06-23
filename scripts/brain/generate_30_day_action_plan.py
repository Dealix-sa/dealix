"""Generate a rolling 30-day action plan — scenario-based, non-deterministic.

For each focus area, the plan lists base/upside/downside actions with a
confidence level. The plan is written to ``reports/brain/30_day_action_plan_<date>.md``
and returned as a string.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(REPO_ROOT, "reports", "brain")

CONFIDENCE_LEVELS = ("low", "medium", "high")


def _action_entry(action: str, confidence: str, day_range: str) -> dict[str, str]:
    if confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"confidence must be one of {CONFIDENCE_LEVELS}, got {confidence}")
    return {"action": action, "confidence": confidence, "when": day_range}


def generate_30_day_action_plan(
    focus_areas: list[str] | None = None,
    profile: dict[str, Any] | None = None,
    reports_dir: str | None = None,
) -> str:
    """Generate and persist a 30-day scenario action plan. Returns the plan text."""
    if focus_areas is None:
        focus_areas = (profile or {}).get("focus_areas") or ["growth", "product", "operations"]

    today = datetime.now(timezone.utc).date()
    lines: list[str] = []
    lines.append(f"# 30-Day Action Plan — {today.isoformat()}")
    lines.append("")
    lines.append(
        "> Every action is a scenario with a confidence level. "
        "No guaranteed outcomes. No deterministic ROI. Adjust based on evidence."
    )
    lines.append("")

    # Split the 30 days into three windows.
    windows = [
        ("Days 1–10", "medium"),
        ("Days 11–20", "medium"),
        ("Days 21–30", "low"),
    ]

    for area in focus_areas:
        lines.append(f"## {area}")
        lines.append("")
        for label, default_conf in windows:
            lines.append(f"### {label}")
            lines.append(f"- **base** [{default_conf}]: Continue current {area} cadence; review at end of window.")
            lines.append(f"- **upside** [low]: If assumptions hold, accelerate {area} by adding one experiment.")
            lines.append(f"- **downside** [medium]: If assumptions break, pause new {area} bets and protect runway.")
            lines.append("")
        lines.append("")

    # Key dates
    lines.append("## Key review dates")
    lines.append("")
    for offset in (10, 20, 30):
        d = (today + timedelta(days=offset)).isoformat()
        lines.append(f"- Day {offset} review: {d}")
    lines.append("")

    plan = "\n".join(lines)

    out_dir = reports_dir or REPORTS_DIR
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"30_day_action_plan_{today.isoformat()}.md")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(plan)

    return plan


if __name__ == "__main__":
    print(generate_30_day_action_plan())