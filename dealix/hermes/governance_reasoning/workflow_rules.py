"""Per-workflow rule overrides."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_WORKFLOW_RULES: dict[str, dict[str, Any]] = {}


@dataclass(frozen=True)
class WorkflowRuleResult:
    allowed: bool
    reason: str = ""


def set_workflow_rule(workflow_id: str, rules: dict[str, Any]) -> None:
    """Register or replace the per-workflow rule set."""
    _WORKFLOW_RULES[workflow_id] = dict(rules)


def evaluate(workflow_id: str, action: str, context: dict[str, Any]) -> WorkflowRuleResult:
    """Apply workflow-scoped rules; permissive default when no rule registered."""
    rules = _WORKFLOW_RULES.get(workflow_id, {})
    allowed_actions = rules.get("allowed_actions")
    if allowed_actions is not None and action not in allowed_actions:
        return WorkflowRuleResult(allowed=False, reason=f"workflow {workflow_id}: action {action} not whitelisted")

    max_records = rules.get("max_records")
    if max_records is not None and int(context.get("record_count", 0)) > int(max_records):
        return WorkflowRuleResult(
            allowed=False,
            reason=f"workflow {workflow_id}: record_count exceeds {max_records}",
        )
    return WorkflowRuleResult(allowed=True)


def clear() -> None:
    """Clear the in-memory workflow rule registry (test helper)."""
    _WORKFLOW_RULES.clear()
