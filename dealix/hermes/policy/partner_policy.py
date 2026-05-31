"""Partner-policy rule — partner-visible actions need partner-policy review."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.hermes.policy.rules import RuleResult


@dataclass(frozen=True)
class PartnerPolicyRule:
    name: str = "partner_action_requires_review"

    def evaluate(self, context: dict[str, Any]) -> RuleResult:
        if not context.get("affects_partner"):
            return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
        if not context.get("partner_review_id"):
            return RuleResult(
                rule_name=self.name,
                passed=False,
                reason="partner-visible action without a partner review attached",
                severity="block",
            )
        return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
