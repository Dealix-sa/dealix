"""Customer health scoring (section 121)."""

from __future__ import annotations

from dataclasses import dataclass


def _clip(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass(frozen=True)
class CustomerHealth:
    score: float
    components: dict[str, float]
    renewal_risk: str    # low|medium|high
    upsell_potential: str


class CustomerHealthScorer:
    def compute(
        self,
        *,
        usage: float,
        outcomes: float,
        communication: float,
        value: float,
    ) -> CustomerHealth:
        u = _clip(usage)
        o = _clip(outcomes)
        c = _clip(communication)
        v = _clip(value)
        score = 0.25 * u + 0.35 * o + 0.15 * c + 0.25 * v
        renewal_risk = "high" if score < 0.4 else "medium" if score < 0.65 else "low"
        upsell_potential = "high" if score > 0.75 and v > 0.7 else "medium" if score > 0.55 else "low"
        return CustomerHealth(
            score=score,
            components={"usage": u, "outcomes": o, "communication": c, "value": v},
            renewal_risk=renewal_risk,
            upsell_potential=upsell_potential,
        )


__all__ = ["CustomerHealth", "CustomerHealthScorer"]
