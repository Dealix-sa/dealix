"""Execution planner — picks today's highest-value strategies and turns each
strategy's steps into concrete, classified Actions."""

from __future__ import annotations

from .schemas import Action, Strategy

# Keywords in a step that imply an external/approval-gated action.
_APPROVAL_HINTS = (
    "send",
    "outreach",
    "message",
    "publish",
    "post ",
    "invoice",
    "payment",
    "charge",
    "contract",
    "email",
    "whatsapp",
    "linkedin",
    "deploy",
    "merge",
)

# Keywords that map a step to an action_type understood by the safety gate.
_TYPE_HINTS = (
    ("draft", "draft_report"),
    ("write", "draft_content"),
    ("content", "draft_content"),
    ("outreach", "outreach_draft"),
    ("message", "outreach_draft"),
    ("queue", "build_queue"),
    ("prioriti", "prioritize"),
    ("analy", "analyze"),
    ("checklist", "checklist"),
    ("proof", "proof_log"),
    ("invoice", "invoice"),
    ("payment", "payment"),
    ("publish", "publish_content"),
)


def _classify_step_type(step: str) -> str:
    low = step.lower()
    for needle, action_type in _TYPE_HINTS:
        if needle in low:
            return action_type
    return "analyze"


def _step_requires_approval(step: str, strategy: Strategy) -> bool:
    low = step.lower()
    if any(hint in low for hint in _APPROVAL_HINTS):
        return True
    for needs in strategy.approval_required_for:
        if needs and needs.lower() in low:
            return True
    return False


def select_strategies(strategies: list[Strategy], limit: int) -> list[Strategy]:
    """Return the top strategies by priority (already sorted by the registry)."""

    if limit <= 0:
        return list(strategies)
    return list(strategies)[:limit]


def plan_actions(strategy: Strategy) -> list[Action]:
    """Expand a strategy's steps into Actions (unclassified status)."""

    actions: list[Action] = []
    for step in strategy.steps:
        action_type = _classify_step_type(step)
        requires_approval = _step_requires_approval(step, strategy)
        # External-ish steps carry a higher nominal level; internal steps sit at
        # level 3 (internal execution).
        level = 3 if not requires_approval else 5
        actions.append(
            Action(
                strategy=strategy.name,
                title=step,
                action_type=action_type,
                autonomy_level=level,
                requires_approval=requires_approval,
                detail=strategy.goal,
            )
        )
    return actions
