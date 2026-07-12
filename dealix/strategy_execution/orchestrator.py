"""Orchestrator — runs one draft-only day of the Strategy Execution OS.

Pipeline:
    load strategies -> select top N -> plan actions -> safety gate classify
    -> split queues -> proof log -> learning notes -> content queue -> write files

No network, no secrets, no external side effects. Outputs are internal reports.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from . import (
    action_queue,
    execution_planner,
    growth_engine,
    learning_loop,
    proof_logger,
    safety_gate,
    strategy_registry,
)
from .schemas import MAX_ENABLED_AUTONOMY_LEVEL, Action, ApprovalItem, ProofEvent

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports" / "autonomous_growth"


@dataclass
class RunResult:
    run_date: date
    autonomy_level: int
    strategies: list[str]
    actions: list[Action]
    approvals: list[ApprovalItem]
    proof: list[ProofEvent]
    learning: list[str]
    content: str
    outputs: dict[str, str] = field(default_factory=dict)

    @property
    def executed_count(self) -> int:
        return sum(1 for a in self.actions if a.status == "executed_internal")

    @property
    def approval_count(self) -> int:
        return len(self.approvals)

    @property
    def blocked_count(self) -> int:
        return sum(1 for a in self.actions if a.status == "blocked")


def run_day(
    autonomy_level: int = int(MAX_ENABLED_AUTONOMY_LEVEL) - 1,
    limit: int = 50,
    mode: str = "draft-only",
    run_date: date | None = None,
    write: bool = True,
) -> RunResult:
    """Execute one draft-only day. Returns a RunResult."""

    run_date = run_date or date.today()
    level = safety_gate.clamp_autonomy(autonomy_level)

    # Hard safety: this engine only ever runs draft-only.
    if mode != "draft-only":
        raise ValueError("Strategy Execution OS only supports mode='draft-only'.")

    strategies = strategy_registry.load_strategies()
    selected = execution_planner.select_strategies(strategies, limit=limit)

    all_actions: list[Action] = []
    for strat in selected:
        for action in execution_planner.plan_actions(strat):
            all_actions.append(safety_gate.classify(action, current_level=level))

    _, approvals = action_queue.split_queues(all_actions)
    proof = proof_logger.build_proof_log(all_actions)
    learning = learning_loop.build_learning_notes(selected, all_actions)
    content = growth_engine.build_content_queue(run_date)

    result = RunResult(
        run_date=run_date,
        autonomy_level=level,
        strategies=[s.name for s in selected],
        actions=all_actions,
        approvals=approvals,
        proof=proof,
        learning=learning,
        content=content,
    )

    if write:
        result.outputs = _write_outputs(result)
    return result


def _write_outputs(result: RunResult) -> dict[str, str]:
    d = result.run_date.isoformat()
    daily = REPORTS_DIR / "daily"
    actions_dir = REPORTS_DIR / "actions"
    approvals_dir = REPORTS_DIR / "approvals"
    proof_dir = REPORTS_DIR / "proof"
    content_dir = REPORTS_DIR / "content"
    learning_dir = REPORTS_DIR / "learning"
    for folder in (daily, actions_dir, approvals_dir, proof_dir, content_dir, learning_dir):
        folder.mkdir(parents=True, exist_ok=True)

    actions_path = actions_dir / f"{d}_actions.json"
    approvals_path = approvals_dir / f"{d}_approvals.json"
    proof_path = proof_dir / f"{d}_proof_log.json"
    content_path = content_dir / f"{d}_content_queue.md"
    learning_path = learning_dir / f"{d}_learning.md"
    daily_path = daily / f"{d}.md"

    actions_path.write_text(
        json.dumps(
            {
                "date": d,
                "autonomy_level": result.autonomy_level,
                "mode": "draft-only",
                "actions": [a.to_dict() for a in result.actions],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    approvals_path.write_text(
        json.dumps(
            {
                "date": d,
                "note": "Founder must review each item before any external send.",
                "approvals": [a.to_dict() for a in result.approvals],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    proof_path.write_text(
        json.dumps(
            {"date": d, "proof": [p.to_dict() for p in result.proof]},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    content_path.write_text(result.content, encoding="utf-8")
    learning_path.write_text(
        f"# Learning notes — {d}\n\n" + "\n".join(f"- {n}" for n in result.learning) + "\n",
        encoding="utf-8",
    )
    daily_path.write_text(_render_daily_md(result), encoding="utf-8")

    def rel(p: Path) -> str:
        return str(p.relative_to(ROOT))

    return {
        "daily": rel(daily_path),
        "actions": rel(actions_path),
        "approvals": rel(approvals_path),
        "proof": rel(proof_path),
        "content": rel(content_path),
        "learning": rel(learning_path),
    }


def _render_daily_md(result: RunResult) -> str:
    d = result.run_date.isoformat()
    lines = [
        f"# Dealix Autonomous Growth — Daily Report {d}",
        "",
        "**Mode:** draft-only · **Autonomy level:** "
        f"{result.autonomy_level} (max enabled: {int(MAX_ENABLED_AUTONOMY_LEVEL)}; "
        "level 5 external execution is BLOCKED)",
        "",
        "## Summary",
        f"- Strategies run: {len(result.strategies)}",
        f"- Internal actions executed: {result.executed_count}",
        f"- Drafts awaiting founder approval: {result.approval_count}",
        f"- Live actions blocked: {result.blocked_count}",
        "",
        "## Strategies (by priority)",
    ]
    lines += [f"- {name}" for name in result.strategies]
    lines += ["", "## Approval queue (founder action required)"]
    if result.approvals:
        for item in result.approvals[:50]:
            lines.append(f"- [{item.strategy}] {item.title} — _{item.reason}_")
    else:
        lines.append("- (none)")
    lines += ["", "## Learning notes"]
    lines += [f"- {n}" for n in result.learning]
    lines += [
        "",
        "## Safety",
        "- No external message was sent. No content was published. No payment was taken.",
        "- Every customer-facing item is a draft in the approval queue.",
        "",
        "## Generated artifacts",
    ]
    for key, path in result.outputs.items():
        lines.append(f"- {key}: `{path}`")
    return "\n".join(lines) + "\n"


def summary_dict(result: RunResult) -> dict[str, Any]:
    return {
        "date": result.run_date.isoformat(),
        "autonomy_level": result.autonomy_level,
        "mode": "draft-only",
        "strategies": len(result.strategies),
        "executed_internal": result.executed_count,
        "approvals": result.approval_count,
        "blocked": result.blocked_count,
        "outputs": result.outputs,
    }


def env_snapshot() -> dict[str, str]:
    """Read only the outbound-flag names we care about (never prints values of
    unrelated secrets)."""

    defaults = {
        "EXTERNAL_SEND_ENABLED": "false",
        "EMAIL_SEND_ENABLED": "false",
        "WHATSAPP_SEND_ENABLED": "false",
        "WHATSAPP_ALLOW_LIVE_SEND": "false",
        "SMS_SEND_ENABLED": "false",
        "OUTBOUND_MODE": "draft_only",
    }
    return {k: os.environ.get(k, default) for k, default in defaults.items()}
