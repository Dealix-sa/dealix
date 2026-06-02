"""Quality + Compliance Gate for outreach drafts.

This gate does NOT reinvent governance. It *composes* the existing,
test-locked cores and adds deliverability/compliance checks on top:

  - ``governance_os.policy_check_draft``  -> forbidden channels/terms/claims
  - ``governance_os.audit_claim_safety``  -> suggested GovernanceDecision
  - ``revenue_os.anti_waste.validate_pipeline_step`` -> blocked sources
    (scraping / cold_whatsapp / purchased_list / linkedin_automation) and
    sub-L4 public-proof attempts

Added deliverability/compliance rules (CAN-SPAM / sender-reputation hygiene):
  - unsubscribe must be present
  - personalization must be >= P1 (never send sector-only blasts)
  - subject must not be misleading (no fake Re:/Fwd:, not empty, not shouting)
  - recipient must not be on the suppression list

A failing gate yields ``governance_decision == "BLOCK"`` and the draft is
never eligible for the approval queue or any send path.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from auto_client_acquisition.governance_os import (
    audit_claim_safety,
    policy_check_draft,
)
from auto_client_acquisition.market_production_os.schemas import (
    PersonalizationLevel,
    RiskLevel,
)
from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step

# Fake-thread prefixes used by spammers to fake an existing conversation.
_FAKE_THREAD_RE = re.compile(r"^\s*(re|fwd|fw)\s*:", re.IGNORECASE)
# Obvious spam-bait tokens that wreck deliverability.
_SPAM_BAIT = (
    "free money",
    "act now",
    "100% free",
    "risk-free guarantee",
    "$$$",
    "click here now",
)


@dataclass(frozen=True, slots=True)
class GateResult:
    passed: bool
    reasons: tuple[str, ...]
    governance_decision: str
    risk_level: str


def _misleading_subject(subject: str) -> list[str]:
    issues: list[str] = []
    s = subject.strip()
    if not s:
        issues.append("empty_subject")
        return issues
    if _FAKE_THREAD_RE.match(s):
        issues.append("fake_thread_prefix")
    # Shouting check applies only to ASCII-heavy subjects; Arabic letters have
    # no case, so ``all()`` over an empty ASCII set must not flag them.
    ascii_letters = [c for c in s if c.isalpha() and c.isascii()]
    if len(ascii_letters) >= 8 and all(c.isupper() for c in ascii_letters):
        issues.append("shouting_subject")
    low = s.lower()
    for bait in _SPAM_BAIT:
        if bait in low:
            issues.append(f"spam_bait:{bait}")
    return issues


def _decision_value(decision: object) -> str:
    return str(getattr(decision, "value", decision))


def check_draft(
    *,
    subject: str,
    body: str,
    personalization_level: int,
    evidence_level: int,
    unsubscribe_included: bool,
    recipient_email: str = "",
    lead_source: str = "founder_supplied",
    suppression: Iterable[str] = (),
    public_marketing: bool = False,
) -> GateResult:
    """Run the full gate. Returns a :class:`GateResult`."""
    reasons: list[str] = []

    # 1) Governance: forbidden channels / terms / guaranteed claims.
    policy = policy_check_draft(f"{subject}\n{body}")
    if not policy.allowed:
        reasons.extend(policy.issues)

    # 2) Claim safety -> suggested governance decision (for the field).
    claim = audit_claim_safety(f"{subject}\n{body}")

    # 3) Anti-waste: blocked sources + public-proof-below-L4.
    waste = validate_pipeline_step(
        has_decision_passport=True,
        lead_source=lead_source,
        action_external=True,
        upsell_attempt=False,
        proof_event_count=1,
        evidence_level_for_public=int(evidence_level),
        public_marketing_attempt=public_marketing,
    )
    reasons.extend(v.code for v in waste)

    # 4) Deliverability / compliance hygiene.
    if not unsubscribe_included:
        reasons.append("missing_unsubscribe")
    if int(personalization_level) < int(PersonalizationLevel.P1):
        reasons.append("personalization_below_p1")
    reasons.extend(_misleading_subject(subject))
    suppressed = {e.strip().lower() for e in suppression if e}
    if recipient_email and recipient_email.strip().lower() in suppressed:
        reasons.append("suppressed_recipient")
    if int(evidence_level) < 0:
        reasons.append("missing_evidence_level")

    reasons = list(dict.fromkeys(reasons))
    passed = not reasons

    if not passed:
        governance_decision = "BLOCK"
        risk = RiskLevel.HIGH.value
    else:
        # Passed the automated gate; a human still approves before any send.
        governance_decision = (
            "ALLOW_WITH_REVIEW"
            if _decision_value(claim.suggested_decision) in {"ALLOW", "DRAFT_ONLY"}
            else "BLOCK"
        )
        risk = (
            RiskLevel.LOW.value
            if int(personalization_level) >= int(PersonalizationLevel.P2)
            and int(evidence_level) >= 2
            else RiskLevel.MEDIUM.value
        )

    return GateResult(
        passed=passed,
        reasons=tuple(reasons),
        governance_decision=governance_decision,
        risk_level=risk,
    )


__all__ = ["GateResult", "check_draft"]
