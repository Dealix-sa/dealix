"""Approval-first safety gate for Dealix strategy execution.

This module is intentionally deterministic and stdlib-only. It does not send,
publish, merge, charge, or change production. It classifies proposed actions so
runners can fail closed and write approval queues instead of executing risky work.
"""

from __future__ import annotations

from dataclasses import dataclass, field

BLOCKED_KEYWORDS = (
    "cold whatsapp",
    "whatsapp blast",
    "mass linkedin",
    "auto post",
    "auto-send",
    "autosend",
    "guaranteed revenue",
    "guarantee revenue",
    "guaranteed sales",
    "government access",
    "bypass rate limit",
    "scrape linkedin",
    "hardcode secret",
    "expose ollama",
    "public vllm",
)

EXTERNAL_ACTION_KEYWORDS = (
    "send email",
    "send whatsapp",
    "publish",
    "post to linkedin",
    "post to x",
    "merge pr",
    "charge",
    "invoice",
    "payment",
    "production deploy",
    "change production",
)

SAFE_INTERNAL_ACTIONS = {
    "read_context",
    "score_targets",
    "draft_outreach",
    "draft_content",
    "generate_report",
    "write_action_queue",
    "write_approval_queue",
    "write_proof_log",
    "write_learning_notes",
    "prepare_issue_draft",
    "prepare_pr_draft",
}


@dataclass(frozen=True)
class SafetyDecision:
    """Safety classification for one action."""

    action: str
    allowed: bool
    approval_required: bool
    reasons: list[str] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        return not self.allowed and not self.approval_required


def _contains_any(text: str, phrases: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in phrases if phrase in lowered]


def evaluate_action_safety(action: str, *, autonomy_level: int = 3) -> SafetyDecision:
    """Classify whether an action can run internally or must wait for approval.

    Level 0-1: observe/analyze only.
    Level 2-3: draft/internal artifacts only.
    Level 4: repo execution only when a caller explicitly implements it.
    Level 5: external execution remains blocked in this package.
    """

    normalized = action.strip().lower()
    reasons: list[str] = []

    blocked_hits = _contains_any(normalized, BLOCKED_KEYWORDS)
    if blocked_hits:
        return SafetyDecision(
            action=action,
            allowed=False,
            approval_required=False,
            reasons=[f"blocked_keyword:{hit}" for hit in blocked_hits],
        )

    external_hits = _contains_any(normalized, EXTERNAL_ACTION_KEYWORDS)
    if external_hits:
        return SafetyDecision(
            action=action,
            allowed=False,
            approval_required=True,
            reasons=[f"external_action_requires_approval:{hit}" for hit in external_hits],
        )

    if normalized in SAFE_INTERNAL_ACTIONS:
        if autonomy_level >= 2:
            return SafetyDecision(action=action, allowed=True, approval_required=False, reasons=["safe_internal"])
        return SafetyDecision(action=action, allowed=False, approval_required=True, reasons=["autonomy_level_too_low"])

    if autonomy_level >= 3:
        return SafetyDecision(action=action, allowed=True, approval_required=False, reasons=["unclassified_internal_default"])

    return SafetyDecision(action=action, allowed=False, approval_required=True, reasons=["needs_founder_review"])
