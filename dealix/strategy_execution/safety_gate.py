"""Safety gate — the single choke point that keeps the engine draft-only.

Every planned action passes through here. The gate decides whether an action may
run internally or must be routed to the human approval queue. It can never let an
external / live action execute.
"""

from __future__ import annotations

from .schemas import (
    FORBIDDEN_LIVE_ACTIONS,
    MAX_ENABLED_AUTONOMY_LEVEL,
    Action,
    AutonomyLevel,
)

# Action types that inherently touch the outside world -> always approval-gated,
# never executed by the engine.
EXTERNAL_ACTION_TYPES = frozenset(
    {
        "outreach_draft",
        "send_message",
        "publish_content",
        "invoice",
        "payment",
        "contract",
        "production_change",
        "merge",
    }
)

# Action types that are safe to execute internally (files/reports/queues only).
INTERNAL_ACTION_TYPES = frozenset(
    {
        "analyze",
        "prioritize",
        "draft_report",
        "draft_content",
        "build_queue",
        "proof_log",
        "learning_note",
        "checklist",
    }
)


def clamp_autonomy(requested: int) -> int:
    """Never allow a level above the maximum enabled level (blocks level 5)."""

    try:
        level = int(requested)
    except (TypeError, ValueError):
        level = int(AutonomyLevel.INTERNAL_EXECUTION)
    level = max(int(AutonomyLevel.OBSERVE), level)
    return min(level, int(MAX_ENABLED_AUTONOMY_LEVEL))


def is_forbidden_live(action_type: str) -> bool:
    return action_type in FORBIDDEN_LIVE_ACTIONS


def classify(action: Action, current_level: int) -> Action:
    """Decide the final status of an action. Pure; returns the mutated action."""

    current_level = clamp_autonomy(current_level)

    # Hard block: anything that maps to a live/forbidden action never runs.
    if is_forbidden_live(action.action_type):
        action.status = "blocked"
        action.requires_approval = True
        action.detail = (action.detail + " [BLOCKED: live action never auto-run]").strip()
        return action

    # External-facing work is always a draft for human approval.
    if action.action_type in EXTERNAL_ACTION_TYPES or action.requires_approval:
        action.status = "queued_for_approval"
        action.requires_approval = True
        return action

    # Internal work runs only if the engine is at or above the action's level
    # and the action is at or below the max enabled level.
    if action.autonomy_level <= current_level and action.autonomy_level <= int(
        MAX_ENABLED_AUTONOMY_LEVEL
    ):
        action.status = "executed_internal"
        action.requires_approval = False
    else:
        # Below the engine's current autonomy -> recommend only.
        action.status = "queued_for_approval"
        action.requires_approval = True
    return action


def assert_no_live_send_enabled(env: dict[str, str]) -> list[str]:
    """Return a list of violations if any live-send flag is enabled."""

    must_be_false = (
        "EXTERNAL_SEND_ENABLED",
        "EMAIL_SEND_ENABLED",
        "WHATSAPP_SEND_ENABLED",
        "WHATSAPP_ALLOW_LIVE_SEND",
        "SMS_SEND_ENABLED",
    )
    violations: list[str] = []
    for key in must_be_false:
        val = str(env.get(key, "false")).strip().lower()
        if val in {"1", "true", "yes", "on"}:
            violations.append(f"{key} must be false (found: {val})")
    mode = str(env.get("OUTBOUND_MODE", "draft_only")).strip().lower()
    if mode and mode != "draft_only":
        violations.append(f"OUTBOUND_MODE must be draft_only (found: {mode})")
    return violations
