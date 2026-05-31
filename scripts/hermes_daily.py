#!/usr/bin/env python3
"""Hermes Daily Loop — single command, single brief.

Composes a founder-friendly daily brief by dispatching three Hermes
intents in order and writing the audit refs to the run log:

  1. PM:       "produce today's status + next 1-3 actions"
  2. DELIVERY: "summarize active sprints + day-N artefacts due today"
  3. SALES:    "list warm-list contacts ready for draft outreach"

Each dispatch produces a `governance_decision` and a `prompt_envelope`
that downstream LLM clients can feed to the active provider. The script
never sends external messages — outputs are drafts only, queued via
approval_center where applicable.

Hard rules (mirrored from dealix_founder_daily_brief.py):
  - Article 4: NEVER auto-sends; ALWAYS prints / writes to gitignored file.
  - Article 8: numeric outputs carry `is_estimate=True`.
  - Article 11: composes existing modules — no new business logic.

Usage:
    python3 scripts/hermes_daily.py
    python3 scripts/hermes_daily.py --out data/founder_briefs/hermes_today.md
    python3 scripts/hermes_daily.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.hermes import HermesOrchestrator, HermesTask  # noqa: E402
from dealix.hermes.agents import route_to_agent_executor  # noqa: E402
from dealix.hermes.router import TaskClass  # noqa: E402


_DAILY_INTENTS: list[tuple[str, TaskClass, str]] = [
    (
        "pm_status",
        TaskClass.PM,
        "Produce today's status (phase + commit delta + top-3 friction) "
        "and the next 1-3 actions per the 90-day plan.",
    ),
    (
        "delivery_summary",
        TaskClass.DELIVERY,
        "Summarize active sprints; list day-N artefacts due today and the "
        "ledger entries each requires.",
    ),
    (
        "sales_drafts",
        TaskClass.SALES,
        "List warm-list contacts ready for draft outreach today, ordered by "
        "qualification score. Drafts only — queued for approval.",
    ),
]


def run_daily() -> dict:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    runs: dict[str, dict] = {}
    for label, hint, intent in _DAILY_INTENTS:
        task = HermesTask(
            intent=intent,
            customer_id="dealix_internal",
            hint=hint,
        )
        result = orch.dispatch(task)
        runs[label] = result.to_dict()
    return {
        "date_utc": datetime.now(UTC).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(UTC).isoformat(),
        "runs": runs,
    }


def render_markdown(brief: dict) -> str:
    lines: list[str] = [
        f"# Hermes Daily Brief — {brief['date_utc']}",
        "",
        f"_Generated at {brief['generated_at']}._",
        "",
        "> Drafts only. No external send happened. Approval-required items "
        "live in approval_center.",
        "",
        "---",
    ]
    for label, run in brief["runs"].items():
        gd = run["governance_decision"]
        route = run.get("route") or {}
        output = run.get("output") or {}
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"- **run_id:** `{run['run_id']}`")
        lines.append(f"- **decision:** `{gd['decision']}`")
        if route:
            lines.append(
                f"- **routed:** `{route['sub_agent']}` "
                f"(gear `{route['gear']}`, provider `{route['provider']}`, "
                f"model `{route['model_id']}`)"
            )
        if gd.get("safe_alternative"):
            lines.append(f"- **safe_alt:** {gd['safe_alternative']}")
        if output.get("deliverable"):
            lines.append(f"- **deliverable:** {output['deliverable']}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Estimated value is not Verified value / "
                 "القيمة التقديرية ليست قيمة مُتحقَّقة")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="hermes_daily")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional output path for the markdown brief.",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Emit the full brief as JSON instead of markdown.",
    )
    args = p.parse_args(argv)

    brief = run_daily()

    if args.json:
        text = json.dumps(brief, ensure_ascii=False, indent=2)
    else:
        text = render_markdown(brief)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
