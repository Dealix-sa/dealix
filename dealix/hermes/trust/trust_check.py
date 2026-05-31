"""
Trust Check — the master gate every agent action goes through.

Checks:
  - no overclaim
  - no false partnership claim
  - no sensitive data leakage
  - pricing approval
  - external commitment approval
  - data scope
  - evidence attached when required
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.policy.engine import PolicyEngine, PolicyEvaluation, PolicyVerdict


_OVERCLAIM_PHRASES = (
    "guaranteed", "100% accuracy", "always works", "infallible",
    "official partner", "trusted by everyone",
)

_PARTNERSHIP_PHRASES = (
    "we are partners with", "in partnership with", "official reseller of",
)


@dataclass(frozen=True)
class TrustCheckResult:
    passed: bool
    reasons: tuple[str, ...]
    policy_evaluation: PolicyEvaluation | None = None

    @property
    def blocking_reasons(self) -> list[str]:
        if self.policy_evaluation:
            return [*self.reasons, *self.policy_evaluation.blocking_reasons]
        return list(self.reasons)


@dataclass
class TrustCheck:
    engine: PolicyEngine = field(default_factory=PolicyEngine)
    approved_partners: set[str] = field(default_factory=set)

    def check(
        self,
        *,
        agent_id: str,
        proposed_text: str = "",
        context: dict[str, Any] | None = None,
    ) -> TrustCheckResult:
        reasons: list[str] = []
        text_lower = proposed_text.lower()

        for phrase in _OVERCLAIM_PHRASES:
            if phrase in text_lower:
                reasons.append(f"overclaim phrase detected: '{phrase}'")
                break

        for phrase in _PARTNERSHIP_PHRASES:
            if phrase in text_lower:
                claimed_partner = (context or {}).get("claimed_partner")
                if not claimed_partner or claimed_partner not in self.approved_partners:
                    reasons.append("partnership claim without approved partner record")
                    break

        ctx = context or {}
        if ctx.get("contains_pii") and ctx.get("audience") == "external":
            reasons.append("sensitive data leakage: PII in external content")

        if ctx.get("affects_pricing") and not ctx.get("pricing_approval_id"):
            reasons.append("pricing change without approval")

        if ctx.get("external_commitment") and not ctx.get("approval_id"):
            reasons.append("external commitment without approval")

        if ctx.get("evidence_required") and not ctx.get("evidence_pack_id"):
            reasons.append("evidence required but no pack attached")

        evaluation = self.engine.evaluate({**ctx, "agent_id": agent_id, "text": proposed_text})

        if evaluation.verdict == PolicyVerdict.deny:
            reasons.extend(evaluation.blocking_reasons)

        return TrustCheckResult(
            passed=not reasons,
            reasons=tuple(reasons),
            policy_evaluation=evaluation,
        )
