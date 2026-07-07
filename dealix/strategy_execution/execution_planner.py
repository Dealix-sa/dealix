"""Daily execution planner for Dealix strategy execution."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Any

from .safety_gate import evaluate_action_safety
from .strategy_registry import load_strategy_registry


def plan_daily_execution(*, autonomy_level: int = 3, limit: int = 50) -> dict[str, Any]:
    """Build a deterministic internal-only daily plan."""

    strategies = load_strategy_registry()
    selected = strategies[: max(1, min(limit, len(strategies)))]
    planned: list[dict[str, Any]] = []
    approvals: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []

    for strategy in selected:
        safe_actions: list[dict[str, Any]] = []
        for action in strategy.allowed_actions:
            decision = evaluate_action_safety(action, autonomy_level=autonomy_level)
            item = {"strategy": strategy.name, "action": action, "decision": asdict(decision)}
            if decision.allowed:
                safe_actions.append(item)
            elif decision.approval_required:
                approvals.append(item)
            else:
                blocked.append(item)

        planned.append(
            {
                "strategy": strategy.to_dict(),
                "safe_actions": safe_actions,
                "expected_outputs": strategy.outputs,
                "kpis": strategy.kpis,
                "proof_required": strategy.proof_required,
            }
        )

    return {
        "date": date.today().isoformat(),
        "autonomy_level": autonomy_level,
        "mode": "draft-only",
        "planned": planned,
        "approvals_required": approvals,
        "blocked": blocked,
        "external_execution_enabled": False,
    }
