"""Policy engine — runs rules and aggregates verdicts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from dealix.hermes.policy.rules import Rule, RuleResult


class PolicyVerdict(StrEnum):
    allow = "allow"
    escalate = "escalate"
    deny = "deny"


@dataclass(frozen=True)
class PolicyEvaluation:
    verdict: PolicyVerdict
    results: tuple[RuleResult, ...]

    @property
    def blocking_reasons(self) -> list[str]:
        return [r.reason for r in self.results if not r.passed and r.severity == "block"]

    @property
    def warnings(self) -> list[str]:
        return [r.reason for r in self.results if not r.passed and r.severity == "warn"]


@dataclass
class PolicyEngine:
    _rules: list[Rule] = field(default_factory=list)

    def register(self, rule: Rule) -> None:
        self._rules.append(rule)

    def evaluate(self, context: dict[str, Any]) -> PolicyEvaluation:
        results = tuple(rule.evaluate(context) for rule in self._rules)
        if any(not r.passed and r.severity == "block" for r in results):
            verdict = PolicyVerdict.deny
        elif any(not r.passed and r.severity == "warn" for r in results):
            verdict = PolicyVerdict.escalate
        else:
            verdict = PolicyVerdict.allow
        return PolicyEvaluation(verdict=verdict, results=results)
