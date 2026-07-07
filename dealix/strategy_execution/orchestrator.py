"""Orchestrator for Dealix internal strategy execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .action_queue import build_action_queue, build_approval_queue, write_json
from .execution_planner import plan_daily_execution
from .growth_engine import build_content_queue
from .learning_loop import build_learning_notes
from .proof_logger import build_proof_log
from .strategy_registry import write_strategy_snapshot


def run_daily_strategy_execution(
    *, output_root: Path, autonomy_level: int = 3, limit: int = 50
) -> dict[str, Any]:
    plan = plan_daily_execution(autonomy_level=autonomy_level, limit=limit)
    run_date = plan["date"]

    action_queue = build_action_queue(plan)
    approval_queue = build_approval_queue(plan)
    content_queue = build_content_queue(plan)
    proof_log = build_proof_log(plan, action_queue, approval_queue)
    learning_notes = build_learning_notes(plan, proof_log)

    write_json(output_root / "actions" / f"{run_date}_actions.json", action_queue)
    write_json(output_root / "approvals" / f"{run_date}_approvals.json", approval_queue)
    write_json(output_root / "proof" / f"{run_date}_proof_log.json", proof_log)
    write_json(output_root / "learning" / f"{run_date}_learning.json", learning_notes)
    write_json(output_root / "content" / f"{run_date}_content_queue.json", content_queue)
    write_strategy_snapshot(output_root / "daily" / f"{run_date}_strategy_registry.md")

    report = render_daily_report(plan, action_queue, approval_queue, content_queue, proof_log)
    report_path = output_root / "daily" / f"{run_date}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    return {
        "date": run_date,
        "report_path": str(report_path),
        "actions": len(action_queue),
        "approvals": len(approval_queue),
        "content_items": len(content_queue),
        "proof_log": proof_log,
    }


def render_daily_report(
    plan: dict[str, Any],
    action_queue: list[dict[str, Any]],
    approval_queue: list[dict[str, Any]],
    content_queue: list[dict[str, Any]],
    proof_log: dict[str, Any],
) -> str:
    lines = [
        f"# Dealix Autonomous Growth Daily Report — {plan['date']}",
        "",
        "## Executive summary",
        "",
        f"- Mode: {plan.get('mode')}",
        f"- Autonomy level: {plan.get('autonomy_level')}",
        f"- Strategies planned: {len(plan.get('planned', []))}",
        f"- Internal actions ready: {len(action_queue)}",
        f"- Founder approval items: {len(approval_queue)}",
        f"- Content ideas queued: {len(content_queue)}",
        "",
        "## Top strategies",
        "",
    ]
    for block in plan.get("planned", []):
        strategy = block.get("strategy", {})
        lines.append(f"- **{strategy.get('name')}** — {strategy.get('goal')}")

    lines.extend(["", "## Internal action queue", ""])
    for item in action_queue[:20]:
        lines.append(f"- {item['strategy']}: {item['action']} ({item['status']})")

    lines.extend(["", "## Approval queue", ""])
    if not approval_queue:
        lines.append("- No approval-blocked items in this run.")
    else:
        for item in approval_queue[:20]:
            lines.append(f"- {item['strategy']}: {item['action']} — {item['status']}")

    lines.extend(["", "## Content queue", ""])
    for item in content_queue[:20]:
        lines.append(f"- {item['type']}: {item['title']} ({item['status']})")

    lines.extend(
        [
            "",
            "## Proof log summary",
            "",
            f"- Strategies: {proof_log.get('strategies_count')}",
            f"- Internal actions: {proof_log.get('internal_actions_count')}",
            f"- Approval items: {proof_log.get('approval_items_count')}",
            f"- Blocked items: {proof_log.get('blocked_count')}",
            "",
            "## Safety posture",
            "",
            "- External execution remains disabled.",
            "- Founder approval is required for any external or high-risk action.",
            "- This report is an internal artifact only.",
        ]
    )
    return "\n".join(lines) + "\n"
