"""Data-policy rule — agents must respect their data boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.hermes.data.classification import DataClass
from dealix.hermes.data.boundaries import DataBoundary
from dealix.hermes.policy.rules import RuleResult


@dataclass(frozen=True)
class DataBoundaryRule:
    name: str = "agent_respects_data_boundary"

    def evaluate(self, context: dict[str, Any]) -> RuleResult:
        boundary: DataBoundary | None = context.get("data_boundary")
        requested: DataClass | None = context.get("requested_class")
        if boundary is None or requested is None:
            return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
        if not boundary.can_read(requested):
            return RuleResult(
                rule_name=self.name,
                passed=False,
                reason=f"agent {boundary.agent_id} cannot read {requested}",
                severity="block",
            )
        return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
