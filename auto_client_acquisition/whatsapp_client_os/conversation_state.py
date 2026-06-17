"""Conversation state machine for the WhatsApp Client OS.

Decisions about *what happens next* live here — not in an LLM. The LLM may
draft copy; this module decides the next stage from (current stage, intent).

Global overrides (evaluated first, from any stage):
- ``blocked_unsafe`` → stage unchanged (the engine returns a refusal card).
- ``human_handoff``  → ``human_handoff``.
- ``support``        → ``support``.
"""

from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.whatsapp_client_os.schemas import (
    ClientIntent,
    SessionStage,
    WhatsAppSession,
)

# Per-stage transition table: stage → {intent → next_stage}
_TRANSITIONS: dict[SessionStage, dict[ClientIntent, SessionStage]] = {
    "new": {
        "welcome": "menu",
        "unknown": "menu",
    },
    "menu": {
        "diagnose": "assessment_in_progress",
        "assessment_start": "assessment_in_progress",
        "not_sure": "assessment_in_progress",
        "campaign_followup": "recommendation",
        "connect_tools": "permission_request",
        "review_report": "recommendation",
        "request_proposal": "proposal",
        "book_call": "proposal",
        "send_file_link": "awaiting_secure_input",
    },
    "assessment_in_progress": {
        "assessment_answer": "assessment_in_progress",  # stays until complete
        "assessment_start": "assessment_in_progress",
    },
    "assessment_complete": {
        "request_proposal": "proposal",
        "book_call": "proposal",
        "connect_tools": "permission_request",
        "diagnose": "recommendation",
        "unknown": "recommendation",
    },
    "recommendation": {
        "request_proposal": "proposal",
        "book_call": "proposal",
        "connect_tools": "permission_request",
        "send_file_link": "awaiting_secure_input",
        "assessment_start": "assessment_in_progress",
    },
    "permission_request": {
        "permission_grant": "awaiting_secure_input",
        "permission_deny": "recommendation",
        "send_file_link": "awaiting_secure_input",
    },
    "awaiting_secure_input": {
        "approve": "draft_review",
        "review_report": "draft_review",
        "unknown": "awaiting_secure_input",
    },
    "draft_review": {
        "approve": "proposal",
        "reject": "recommendation",
        "edit": "draft_review",
        "simplify": "draft_review",
    },
    "proposal": {
        "approve": "payment_handoff",
        "request_proposal": "proposal",
        "reject": "recommendation",
        "book_call": "proposal",
    },
    "payment_handoff": {
        "approve": "onboarding",
        "reject": "recommendation",
    },
    "onboarding": {
        "connect_tools": "permission_request",
        "send_file_link": "awaiting_secure_input",
        "review_report": "draft_review",
    },
    "support": {
        "human_handoff": "human_handoff",
        "review_report": "recommendation",
        "unknown": "support",
    },
    "human_handoff": {},  # terminal until a human resumes
    "closed": {},
}


def transition(
    stage: SessionStage,
    intent: ClientIntent,
    *,
    assessment_complete: bool = False,
) -> SessionStage:
    """Compute the next stage. Global overrides take precedence."""
    # Global overrides
    if intent == "blocked_unsafe":
        return stage  # no progress on a blocked attempt
    if intent == "human_handoff":
        return "human_handoff"
    if intent == "support":
        return "support"

    # Assessment completion gate
    if stage == "assessment_in_progress" and assessment_complete:
        return "assessment_complete"

    # Starting the readiness scan is valid from any non-terminal stage
    # (deep-links, re-scans, «ما أعرف» before the menu is shown).
    if intent in {"assessment_start", "diagnose"} and not is_terminal(stage):
        return "assessment_in_progress"

    table = _TRANSITIONS.get(stage, {})
    if intent in table:
        return table[intent]

    # Sensible defaults: from new → menu; otherwise stay put.
    if stage == "new":
        return "menu"
    return stage


def advance(
    session: WhatsAppSession,
    intent: ClientIntent,
    *,
    assessment_complete: bool = False,
) -> WhatsAppSession:
    """Return an updated session copy after applying a transition."""
    next_stage = transition(session.stage, intent, assessment_complete=assessment_complete)
    return session.model_copy(
        update={
            "stage": next_stage,
            "last_intent": intent,
            "message_count": session.message_count + 1,
            "handoff_requested": session.handoff_requested or next_stage == "human_handoff",
            "updated_at": datetime.now(UTC),
        }
    )


def is_terminal(stage: SessionStage) -> bool:
    return stage in {"human_handoff", "closed"}


def allowed_intents(stage: SessionStage) -> list[ClientIntent]:
    """Intents that produce a real transition from a stage (for UI hinting)."""
    base = list(_TRANSITIONS.get(stage, {}).keys())
    for always in ("support", "human_handoff"):
        if always not in base:
            base.append(always)  # type: ignore[arg-type]
    return base


__all__ = ["advance", "allowed_intents", "is_terminal", "transition"]
