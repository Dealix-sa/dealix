"""Run a full Company Brain Day cycle.

The cycle:
  1. (Optionally) ingest a profile.
  2. Build the company brain map.
  3. Detect bottlenecks.
  4. Generate the future radar.
  5. Generate a daily decision (seed demo if none provided).
  6. Generate the weekly board memo.
  7. Generate the 30-day action plan.
  8. Write a summary report to ``reports/brain/brain_day_<date>.md``.

No external action is taken. The brain only produces reports and ledger
entries for human review.
"""
from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any

from scripts.brain.build_company_brain_map import build_company_brain_map
from scripts.brain.detect_bottlenecks import detect_bottlenecks
from scripts.brain.generate_30_day_action_plan import generate_30_day_action_plan
from scripts.brain.generate_daily_decision import default_review_date, generate_daily_decision
from scripts.brain.generate_future_radar import generate_future_radar
from scripts.brain.generate_weekly_board_memo import generate_weekly_board_memo
from scripts.brain.ingest_company_profile import ingest_company_profile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(REPO_ROOT, "reports", "brain")


def run_brain_day(
    profile: dict[str, Any] | None = None,
    decision_kwargs: dict[str, Any] | None = None,
    reports_dir: str | None = None,
) -> dict[str, Any]:
    """Run a full brain day cycle. Returns a summary dict with report paths."""
    out_dir = reports_dir or REPORTS_DIR
    os.makedirs(out_dir, exist_ok=True)

    # 1. Ingest profile (optional)
    normalised_profile: dict[str, Any] = {}
    if profile:
        normalised_profile = ingest_company_profile(profile)

    # 2. Build brain map
    brain_map = build_company_brain_map(profile=normalised_profile)

    # 3. Detect bottlenecks
    bottlenecks = detect_bottlenecks(brain_map)

    # 4. Generate future radar
    radar = generate_future_radar(profile=normalised_profile)

    # 5. Generate a daily decision
    if decision_kwargs is None:
        decision_kwargs = {
            "decision": "Run weekly decision review with founding team.",
            "why_now": "Decision backlog and stale assumptions increase execution risk.",
            "assumption": "Founders can commit 30 minutes weekly to review.",
            "confidence": "medium",
            "owner": "CEO",
            "next_action": "Schedule recurring 30-min review and share decisions log.",
            "success_metric": ">=80% of decisions reviewed by their review_date.",
            "review_date": default_review_date(14),
            "risk_if_delayed": "Stale assumptions compound; bottlenecks go unaddressed.",
        }
    decision = generate_daily_decision(**decision_kwargs)

    # 6. Weekly board memo
    memo = generate_weekly_board_memo(brain_map=brain_map, reports_dir=out_dir)

    # 7. 30-day action plan
    plan = generate_30_day_action_plan(profile=normalised_profile, reports_dir=out_dir)

    # 8. Write summary report
    today = datetime.now(UTC).date().isoformat()
    summary_path = os.path.join(out_dir, f"brain_day_{today}.md")
    summary_lines = [
        f"# Brain Day Summary — {today}",
        "",
        "> Scenarios, not predictions. No guaranteed outcomes. No automatic external action.",
        "",
        "## Decisions logged",
        f"- {decision['id']}: {decision['decision']}",
        "",
        f"## Bottlenecks detected: {len(bottlenecks)}",
        "",
    ]
    for b in bottlenecks:
        summary_lines.append(f"- [{b['confidence']}] {b['area']}: {b['description']}")
    summary_lines.append("")
    summary_text = "\n".join(summary_lines)
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write(summary_text)

    return {
        "date": today,
        "profile": normalised_profile,
        "bottleneck_count": len(bottlenecks),
        "bottlenecks": bottlenecks,
        "decision": decision,
        "radar": radar,
        "reports": {
            "summary": summary_path,
            "memo": os.path.join(out_dir, f"weekly_board_memo_{today}.md"),
            "plan": os.path.join(out_dir, f"30_day_action_plan_{today}.md"),
        },
    }


if __name__ == "__main__":
    result = run_brain_day()
    print(json.dumps(result, indent=2, default=str))
