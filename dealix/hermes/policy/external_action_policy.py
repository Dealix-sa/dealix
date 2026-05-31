"""External-action policy — no external send happens without approval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.hermes.policy.rules import RuleResult


@dataclass(frozen=True)
class ExternalActionRule:
    name: str = "external_action_requires_approval"

    def evaluate(self, context: dict[str, Any]) -> RuleResult:
        external = bool(context.get("external"))
        approval_id = context.get("approval_id")
        if external and not approval_id:
            return RuleResult(
                rule_name=self.name,
                passed=False,
                reason="external action attempted without an approval_id",
                severity="block",
            )
        return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
