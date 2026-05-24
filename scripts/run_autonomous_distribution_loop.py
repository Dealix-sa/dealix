#!/usr/bin/env python3
"""Unified CLI runner for the autonomous distribution loops.

Usage:
    python scripts/run_autonomous_distribution_loop.py morning
    python scripts/run_autonomous_distribution_loop.py evening
    python scripts/run_autonomous_distribution_loop.py weekly
    python scripts/run_autonomous_distribution_loop.py monthly

Each invocation writes a bilingual markdown report to data/autonomous_loops/
and prints a short status line. No external send happens; outreach drafts
remain in the approval_center queue.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure repo root is on sys.path when run as a script.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.autonomous_distribution import (
    evening_loop,
    monthly_loop,
    morning_loop,
    weekly_loop,
)
from auto_client_acquisition.friction_log.aggregator import aggregate as friction_aggregate

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "data" / "autonomous_loops"


def _today_str() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")


def _write_md(name: str, body: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fname = f"{_today_str()}_{name}.md"
    path = OUTPUT_DIR / fname
    path.write_text(body, encoding="utf-8")
    return path


def _disclaimer() -> str:
    return (
        "\n\n---\n"
        "> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة\n"
    )


def run_morning() -> int:
    r = morning_loop(leads_inbound=0, leads_scored=0, drafts_pending=0)
    body = (
        f"# Morning Loop — {_today_str()}\n\n"
        f"**governance_decision:** `{r.governance_decision.value}`\n\n"
        f"## Founder Digest (AR)\n{r.founder_digest_ar}\n\n"
        f"## Founder Digest (EN)\n{r.founder_digest_en}\n\n"
        f"## High-priority Actions\n"
        + "\n".join(f"- {a}" for a in r.high_priority_actions)
        + _disclaimer()
    )
    path = _write_md("morning", body)
    print(f"[morning] -> {path}")
    print(f"  governance_decision={r.governance_decision.value}")
    print(f"  actions={r.high_priority_actions}")
    return 0


def run_evening() -> int:
    try:
        friction = friction_aggregate(customer_id="dealix_internal", window_days=1)
    except Exception:  # noqa: BLE001
        friction = None
    r = evening_loop(
        revenue_today_sar=0.0,
        leads_in_pipeline=0,
        friction=friction,
        overdue_proof_packs=0,
        upcoming_sprints=0,
        retainer_due=0,
    )
    body = (
        f"# Evening Loop — {_today_str()}\n\n"
        f"**governance_decision:** `{r.governance_decision.value}`\n\n"
        f"## Founder Digest (AR)\n{r.founder_digest_ar}\n\n"
        f"## Founder Digest (EN)\n{r.founder_digest_en}\n\n"
        f"## Tomorrow Top-4\n"
        + "\n".join(f"- {a}" for a in r.tomorrow_top_4)
        + _disclaimer()
    )
    path = _write_md("evening", body)
    print(f"[evening] -> {path}")
    print(f"  governance_decision={r.governance_decision.value}")
    print(f"  friction_events={r.friction_events_today} high={r.high_severity_frictions}")
    return 0


def run_weekly() -> int:
    r = weekly_loop(
        retainers_eligible=0,
        capital_assets_added=0,
        proof_packs_completed=0,
        revenue_week_sar=0.0,
        revenue_last_week_sar=0.0,
        mrr_sar=0.0,
    )
    body = (
        f"# Weekly Loop — week of {_today_str()}\n\n"
        f"**governance_decision:** `{r.governance_decision.value}`\n\n"
        f"## Next Week Focus (AR)\n{r.next_week_focus_ar}\n\n"
        f"## Next Week Focus (EN)\n{r.next_week_focus_en}\n\n"
        f"- revenue_week_sar: {r.revenue_week_sar}\n"
        f"- mrr_sar: {r.mrr_sar}\n"
        f"- one_time_week_sar: {r.one_time_week_sar}\n"
        f"- week_over_week_pct: {r.week_over_week_pct}\n"
        f"- retainers_eligible: {r.retainers_eligible}\n"
        f"- capital_assets_added: {r.capital_assets_added}\n"
        f"- proof_packs_completed: {r.proof_packs_completed}\n"
        + _disclaimer()
    )
    path = _write_md("weekly", body)
    print(f"[weekly] -> {path}")
    print(f"  governance_decision={r.governance_decision.value}")
    return 0


def run_monthly(day_count: int) -> int:
    r = monthly_loop(
        day_count_since_launch=day_count,
        cumulative_revenue_sar=0.0,
        active_retainers=0,
        capital_assets_total=0,
        doctrine_violations=0,
    )
    body = (
        f"# Monthly Loop — {_today_str()} (day {day_count} since launch)\n\n"
        f"**governance_decision:** `{r.governance_decision.value}`\n"
        f"**phase:** `{r.month_phase}` | **verdict:** `{r.milestone_verdict}`\n\n"
        f"## Rationale (AR)\n{r.rationale_ar}\n\n"
        f"## Rationale (EN)\n{r.rationale_en}\n\n"
        f"## Founder Decisions Pending\n"
        + "\n".join(f"- {d}" for d in r.decisions_for_founder)
        + _disclaimer()
    )
    path = _write_md("monthly", body)
    print(f"[monthly] -> {path}")
    print(f"  phase={r.month_phase} verdict={r.milestone_verdict}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous Distribution Loop runner.")
    parser.add_argument(
        "loop",
        choices=["morning", "evening", "weekly", "monthly", "all"],
        help="Which loop to run.",
    )
    parser.add_argument(
        "--days-since-launch",
        type=int,
        default=1,
        help="For monthly loop: days elapsed since commercial launch.",
    )
    args = parser.parse_args()

    if args.loop == "morning":
        return run_morning()
    if args.loop == "evening":
        return run_evening()
    if args.loop == "weekly":
        return run_weekly()
    if args.loop == "monthly":
        return run_monthly(args.days_since_launch)
    if args.loop == "all":
        run_morning()
        run_evening()
        run_weekly()
        run_monthly(args.days_since_launch)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
