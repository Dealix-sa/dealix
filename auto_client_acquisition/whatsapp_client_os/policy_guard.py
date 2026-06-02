"""WhatsApp Client OS — policy guard.

Single gate every outbound WhatsApp card/message passes through before the
brain emits it. Reuses the canonical ``governance_os`` checks (forbidden
channel language, guaranteed-outcome claims, scraping/cold-outreach) and adds
WhatsApp-specific posture: pricing commitments are never auto-promised in
chat (they route to a human), and secret material is never echoed.

No live send ever originates here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from auto_client_acquisition.governance_os import GovernanceDecision, policy_check_draft
from auto_client_acquisition.whatsapp_client_os.permission_os import looks_like_secret

# Affirmative final-price / commitment language that must go to a human
# rather than be promised by the bot. Neutral price *ranges in a proposal
# card* are fine; these are bot-authored commitments.
_PRICING_COMMIT = (
    re.compile(r"السعر\s+النهائي|أؤكد\s+لك\s+السعر|نلتزم\s+بسعر|خصم\s+خاص\s+لك", re.IGNORECASE),
    re.compile(
        r"final\s+price|i\s+confirm\s+the\s+price|we\s+commit\s+to\s+a\s+price", re.IGNORECASE
    ),
)


@dataclass(frozen=True, slots=True)
class GuardResult:
    allowed: bool
    governance_decision: str
    reasons: tuple[str, ...]


def has_pricing_commitment(text: str) -> bool:
    if not text:
        return False
    return any(p.search(text) for p in _PRICING_COMMIT)


def guard_outbound(text: str) -> GuardResult:
    """Gate text the bot intends to send to a client.

    BLOCK on forbidden channel/claim language or secret leakage.
    REQUIRE_APPROVAL (route to human) on pricing commitments.
    ALLOW otherwise.
    """
    reasons: list[str] = []

    check = policy_check_draft(text)
    if not check.allowed:
        reasons.extend(check.issues)

    if looks_like_secret(text):
        reasons.append("secret_material_in_text")

    if reasons:
        return GuardResult(False, GovernanceDecision.BLOCK.value, tuple(dict.fromkeys(reasons)))

    if has_pricing_commitment(text):
        return GuardResult(
            False,
            GovernanceDecision.REQUIRE_APPROVAL.value,
            ("pricing_commitment_requires_human",),
        )

    return GuardResult(True, GovernanceDecision.ALLOW.value, ())


__all__ = ["GuardResult", "guard_outbound", "has_pricing_commitment"]
