"""Governance gate — every Hermes task passes through here before execution.

Reuses existing primitives:
- auto_client_acquisition.governance_os.forbidden_actions.is_channel_forbidden
- auto_client_acquisition.governance_os.approval_policy.approval_for_external_channel

Decision categories:
- approved        → run the task, log governance_decision=approved
- needs_approval  → queue draft for approval_center, return placeholder
- rejected        → refuse cleanly, log refusal in friction_log
- kill_switched   → orchestrator-wide halt
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional

# Inlined from auto_client_acquisition.governance_os to keep this module
# dependency-light (the canonical package __init__ eagerly imports a heavy
# dep tree). Equivalence is asserted by tests/hermes/test_charter_pinned.py
# and tests/hermes/test_doctrine_refusals.py.

FORBIDDEN_CHANNEL_MARKERS: tuple[str, ...] = (
    "cold whatsapp",
    "linkedin automation",
    "blast",
)


def _phrase_matches(text: str, phrase: str) -> bool:
    """Whole-word match for single tokens; substring match for multi-word phrases.

    Avoids the classic substring trap: 'scrape' matching 'periscrape',
    'blast' matching 'blast radius', 'doc' matching 'doctor'. For phrases
    that already contain whitespace ('cold whatsapp', 'send email') the
    phrase boundary is implicit, so substring matching is safe.
    """
    if " " in phrase:
        return phrase in text
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def is_channel_forbidden(text: str) -> bool:
    low = text.lower()
    return any(_phrase_matches(low, m) for m in FORBIDDEN_CHANNEL_MARKERS)


class ApprovalRequirement(StrEnum):
    NONE = "none"
    INTERNAL_REVIEW = "internal_review"
    CLIENT_APPROVAL = "client_approval"
    BLOCKED = "blocked"


def approval_for_external_channel(*, channel: str, has_client_approval: bool) -> ApprovalRequirement:
    ch = channel.strip().lower()
    if ch in ("whatsapp", "linkedin_dm", "sms"):
        return ApprovalRequirement.CLIENT_APPROVAL if has_client_approval else ApprovalRequirement.BLOCKED
    if ch in ("email", "portal"):
        return ApprovalRequirement.INTERNAL_REVIEW
    return ApprovalRequirement.NONE

# Patterns that are absolute refusals regardless of channel.
_HARD_REFUSAL_PATTERNS: tuple[str, ...] = (
    "scrape",
    "scraping",
    "cold whatsapp",
    "cold email blast",
    "linkedin automation",
    "linkedin scraper",
    "fake testimonial",
    "fabricate proof",
    "fabricate testimonial",
    "guaranteed return",
    "guaranteed sales",
    "guaranteed roi",
)

# External-action verbs that always require approval_center, never auto-send.
_EXTERNAL_SEND_MARKERS: tuple[str, ...] = (
    "send email",
    "send whatsapp",
    "send linkedin",
    "send sms",
    "publish post",
    "publish article",
    "post to ",
    "dm to ",
)


class Decision(StrEnum):
    APPROVED = "approved"
    NEEDS_APPROVAL = "needs_approval"
    REJECTED = "rejected"
    KILL_SWITCHED = "kill_switched"


@dataclass
class GovernanceDecision:
    decision: str
    reason: str
    safe_alternative: str = ""
    matched_rules: list[str] = field(default_factory=list)
    requires_channel_approval: Optional[str] = None

    def is_blocking(self) -> bool:
        return self.decision in {Decision.REJECTED.value, Decision.KILL_SWITCHED.value}

    def is_approval_required(self) -> bool:
        return self.decision == Decision.NEEDS_APPROVAL.value


class GovernanceGate:
    """Pre-execution gate. Pure logic, no side effects (audit handles writes)."""

    def __init__(self, kill_switch: bool = False) -> None:
        self.kill_switch = kill_switch

    def evaluate(self, intent_text: str, *, channel: str = "") -> GovernanceDecision:
        if self.kill_switch:
            return GovernanceDecision(
                decision=Decision.KILL_SWITCHED.value,
                reason="HERMES_KILL_SWITCH active",
                safe_alternative="Unset HERMES_KILL_SWITCH after incident review.",
            )

        text = (intent_text or "").lower()
        matched: list[str] = []

        # Hard refusals — doctrine-protected. Word-boundary regex so
        # "scrape" matches the verb but not "blast radius" / "decode" /
        # "doctor"; multi-word phrases ("cold whatsapp") fall back to a
        # substring check because regex \b on the phrase boundary is
        # cumbersome but the phrase itself is unambiguous.
        for pat in _HARD_REFUSAL_PATTERNS:
            if _phrase_matches(text, pat):
                matched.append(pat)
        if matched:
            return GovernanceDecision(
                decision=Decision.REJECTED.value,
                reason="Request matches doctrine-forbidden pattern.",
                safe_alternative=(
                    "Generate a draft (no send), surface in approval_center, "
                    "and let the founder approve per non-negotiables #1, #2, #3, #8."
                ),
                matched_rules=matched,
            )

        # Channel-level forbidden markers from forbidden_actions
        if is_channel_forbidden(text):
            triggered = [m for m in FORBIDDEN_CHANNEL_MARKERS if _phrase_matches(text, m)]
            return GovernanceDecision(
                decision=Decision.REJECTED.value,
                reason="Channel use matches forbidden marker.",
                safe_alternative="Use approved channels with approval_center gating.",
                matched_rules=triggered,
            )

        # External-send verbs → queue for approval, do not auto-send
        for marker in _EXTERNAL_SEND_MARKERS:
            if _phrase_matches(text, marker):
                inferred = channel or self._infer_channel(marker)
                req = approval_for_external_channel(
                    channel=inferred, has_client_approval=False
                )
                if req in {ApprovalRequirement.BLOCKED}:
                    return GovernanceDecision(
                        decision=Decision.REJECTED.value,
                        reason=f"Channel '{inferred}' requires client approval not on file.",
                        safe_alternative="Collect client approval first, then re-submit.",
                        matched_rules=[marker],
                        requires_channel_approval=inferred,
                    )
                return GovernanceDecision(
                    decision=Decision.NEEDS_APPROVAL.value,
                    reason=f"External send on '{inferred}' must pass approval_center.",
                    safe_alternative="Hermes will generate the draft and queue it for founder approval.",
                    matched_rules=[marker],
                    requires_channel_approval=inferred,
                )

        return GovernanceDecision(
            decision=Decision.APPROVED.value,
            reason="No doctrine violation detected; internal-only action.",
        )

    @staticmethod
    def _infer_channel(marker: str) -> str:
        if "whatsapp" in marker:
            return "whatsapp"
        if "linkedin" in marker:
            return "linkedin_dm"
        if "sms" in marker:
            return "sms"
        if "email" in marker:
            return "email"
        if "post" in marker or "publish" in marker:
            return "portal"
        return "email"
