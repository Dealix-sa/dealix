"""Execution assurance report generator.

Checks whether the founder is following the daily/weekly loops by inspecting
freshness of expected outputs and counts of evidence entries.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path
import time


EXPECTED = [
    ("founder/mission_control.md", 2),
    ("founder/ceo_action_queue.md", 2),
    ("founder/control_tower_brief.md", 2),
    ("business_audit/ceo_business_score.md", 8),
    ("evidence/execution_assurance_report.md", 8),
]


def render(root: Path) -> str:
    today = dt.date.today().isoformat()
    lines = [f"# Execution Assurance Report\nGenerated on: {today}\n", "## Loop compliance\n"]
    now = time.time()
    issues = 0
    for rel, max_days in EXPECTED:
        path = root / rel
        if not path.exists():
            lines.append(f"- {rel}: MISSING (run the relevant make target)")
            issues += 1
            continue
        age_days = (now - path.stat().st_mtime) / 86_400.0
        if age_days > max_days:
            lines.append(f"- {rel}: STALE ({age_days:.1f}d > {max_days}d)")
            issues += 1
        else:
            lines.append(f"- {rel}: OK ({age_days:.1f}d)")
    lines.append("")
    lines.append(f"## Issues: {issues}")
    if issues == 0:
        lines.append("PASS: execution loops in compliance.")
    else:
        lines.append("Action: refresh the surfaces above before the next decision.")
    return "\n".join(lines) + "\n"
