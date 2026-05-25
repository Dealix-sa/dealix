"""Marketplace publish — sovereign-only, always."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.hermes.policy.rules import RuleResult
from dealix.hermes.sovereignty.levels import SovereigntyLevel


@dataclass(frozen=True)
class MarketplacePolicyRule:
    name: str = "marketplace_publish_is_sovereign_only"

    def evaluate(self, context: dict[str, Any]) -> RuleResult:
        if not context.get("affects_marketplace"):
            return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
        level = context.get("sovereignty_level")
        if level not in (SovereigntyLevel.S4_SOVEREIGN_ONLY, SovereigntyLevel.S5_NEVER_AUTONOMOUS):
            return RuleResult(
                rule_name=self.name,
                passed=False,
                reason="marketplace publish at insufficient sovereignty level",
                severity="block",
            )
        return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
