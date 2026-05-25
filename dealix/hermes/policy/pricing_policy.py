"""Pricing-policy rule — published pricing changes need sovereign memo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.hermes.policy.rules import RuleResult
from dealix.hermes.sovereignty.levels import SovereigntyLevel, requires_memo


@dataclass(frozen=True)
class PricingPolicyRule:
    name: str = "pricing_change_requires_sovereign_memo"

    def evaluate(self, context: dict[str, Any]) -> RuleResult:
        if not context.get("affects_pricing"):
            return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
        level = context.get("sovereignty_level")
        memo_id = context.get("memo_id")
        if isinstance(level, SovereigntyLevel) and requires_memo(level) and not memo_id:
            return RuleResult(
                rule_name=self.name,
                passed=False,
                reason="pricing change at this sovereignty level requires a memo",
                severity="block",
            )
        return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
