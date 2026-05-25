"""Semantic vetting — does the tool's behavior match its description?"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SemanticVetting:
    passed: bool
    confidence: float
    reasons: tuple[str, ...]


def vet_tool_semantics(
    *,
    declared_purpose: str,
    parameters_schema: dict[str, Any],
    observed_side_effects: list[str] | None = None,
) -> SemanticVetting:
    reasons: list[str] = []
    observed = observed_side_effects or []

    risky_purposes = ("read", "list", "summarize")
    risky_side_effects = ("write", "send", "delete", "publish")

    if any(p in declared_purpose.lower() for p in risky_purposes):
        for effect in observed:
            if any(eff in effect.lower() for eff in risky_side_effects):
                reasons.append(
                    f"declared '{declared_purpose}' but observed '{effect}'"
                )

    parameter_count = len(parameters_schema.get("properties", {}))
    confidence = 1.0
    if parameter_count > 25:
        reasons.append(f"unusually large parameter surface ({parameter_count})")
        confidence -= 0.3

    if not reasons:
        return SemanticVetting(passed=True, confidence=confidence, reasons=())
    return SemanticVetting(passed=False, confidence=max(0.0, confidence), reasons=tuple(reasons))
