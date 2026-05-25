"""Situational risk score from sensitivity, magnitude, irreversibility."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SituationalRisk:
    sensitivity: int
    magnitude: int
    irreversibility: int
    risk_score: int
    escalate: bool


def _clamp(value: int) -> int:
    return max(0, min(5, value))


def score(context: dict[str, Any]) -> SituationalRisk:
    """Return SituationalRisk computed from sensitivity, magnitude, irreversibility (0-5 each)."""
    sensitivity = _clamp(int(context.get("sensitivity", 0)))
    magnitude = _clamp(int(context.get("magnitude", 0)))
    irreversibility = _clamp(int(context.get("irreversibility", 0)))
    risk_score = sensitivity + magnitude + irreversibility
    escalate = sensitivity >= 3 or risk_score >= 8
    return SituationalRisk(
        sensitivity=sensitivity,
        magnitude=magnitude,
        irreversibility=irreversibility,
        risk_score=risk_score,
        escalate=escalate,
    )


def must_escalate(context: dict[str, Any]) -> bool:
    """Return True when context sensitivity >= 3 (founder-sovereignty doctrine)."""
    return score(context).escalate
