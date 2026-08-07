"""Draft quality gate — deterministic checks every outbound-bound draft passes.

Wraps the existing governance primitives (``audit_claim_safety`` →
``audit_draft_text``, channel-language check) and adds length + excess-PII
checks. The output decision maps to a draft ``governance_status`` so no draft
can be approved while it carries a forbidden claim or forbidden-channel
language. This is a shallow guardrail — founder review remains mandatory.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.channel_policy import (
    draft_text_has_forbidden_channel_language,
)
from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety
from auto_client_acquisition.governance_os.runtime_decision import decide

# Decision → draft governance status. ``blocked`` and ``needs_edit`` can never
# be flipped to ``approved`` by the draft factory transitions.
_DECISION_TO_STATUS: dict[str, str] = {
    "allow": "pending_approval",
    "draft_only": "needs_edit",
    "block": "blocked",
}

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?9665\d{8}|05\d{8})(?!\d)")

DEFAULT_MAX_CHARS = 1200


@dataclass(frozen=True, slots=True)
class DraftQualityResult:
    """Structured outcome of a draft quality check."""

    issues: tuple[str, ...]
    decision: str  # allow | draft_only | block
    governance_status: str  # pending_approval | needs_edit | blocked
    pii_count: int
    char_count: int
    too_long: bool

    @property
    def passed(self) -> bool:
        """True only when the draft is clean enough to enter the approval queue."""
        return self.decision == "allow"


def _count_pii(text: str) -> int:
    return len(_EMAIL_RE.findall(text)) + len(_PHONE_RE.findall(text))


def check_draft(
    *,
    text: str,
    channel: str = "email",
    max_chars: int = DEFAULT_MAX_CHARS,
    pii_threshold: int = 2,
) -> DraftQualityResult:
    """Run the quality gate on a single draft body.

    A forbidden guaranteed-outcome claim forces ``block``. Any other issue
    (forbidden operational term, forbidden-channel language, over-length,
    excess PII) forces ``draft_only`` (needs edit). A clean draft is ``allow``.
    """
    issues: list[str] = []

    claim = audit_claim_safety(text)
    issues.extend(claim.issues)

    # Broader guaranteed-OUTCOME detection (the canonical NO_GUARANTEED_CLAIMS
    # regex gate) — catches "guarantee revenue/sales/results" that the keyword
    # list in audit_draft_text does not. A bare-text decide() can only return
    # "block" via this content gate, so it cleanly isolates the claim signal.
    guarantee_block = (
        str(decide(action_type="draft_content_audit", context={"text": text}).decision) == "block"
    )
    if guarantee_block and not any(i.startswith("forbidden_claim") for i in issues):
        issues.append("forbidden_claim:guaranteed_outcome")

    if draft_text_has_forbidden_channel_language(text):
        issues.append("forbidden_channel_language")

    char_count = len(text)
    too_long = char_count > max_chars
    if too_long:
        issues.append(f"too_long:{char_count}>{max_chars}")

    pii_count = _count_pii(text)
    if pii_count > pii_threshold:
        issues.append(f"excess_pii:{pii_count}")

    if claim.suggested_decision == GovernanceDecision.BLOCK or guarantee_block:
        decision = "block"
    elif issues:
        decision = "draft_only"
    else:
        decision = "allow"

    # de-dupe while preserving order
    deduped = tuple(dict.fromkeys(issues))
    return DraftQualityResult(
        issues=deduped,
        decision=decision,
        governance_status=_DECISION_TO_STATUS[decision],
        pii_count=pii_count,
        char_count=char_count,
        too_long=too_long,
    )


def quality_gate_report(texts: list[str], *, channel: str = "email") -> dict[str, object]:
    """Aggregate a batch of draft bodies into a quality-gate report."""
    results = [check_draft(text=t, channel=channel) for t in texts]
    blocked = [r for r in results if r.decision == "block"]
    needs_edit = [r for r in results if r.decision == "draft_only"]
    approved = [r for r in results if r.decision == "allow"]
    violations = sum(len(r.issues) for r in results)
    return {
        "drafts_checked": len(results),
        "violations": violations,
        "blocked_drafts": len(blocked),
        "needs_edit": len(needs_edit),
        "approved_for_review": len(approved),
        "recommended_edits": [list(r.issues) for r in needs_edit if r.issues],
    }


__all__ = [
    "DEFAULT_MAX_CHARS",
    "DraftQualityResult",
    "check_draft",
    "quality_gate_report",
]
