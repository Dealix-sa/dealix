"""Rule base class and primitive results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol


@dataclass(frozen=True)
class RuleResult:
    rule_name: str
    passed: bool
    reason: str
    severity: str = "info"  # info | warn | block


class Rule(Protocol):
    name: str

    def evaluate(self, context: dict[str, Any]) -> RuleResult: ...


@dataclass(frozen=True)
class LambdaRule:
    """Convenience wrapper for inline rules in tests."""

    name: str
    predicate: Callable[[dict[str, Any]], bool]
    fail_reason: str = "rule_failed"
    severity: str = "block"

    def evaluate(self, context: dict[str, Any]) -> RuleResult:
        passed = bool(self.predicate(context))
        return RuleResult(
            rule_name=self.name,
            passed=passed,
            reason="" if passed else self.fail_reason,
            severity="info" if passed else self.severity,
        )
