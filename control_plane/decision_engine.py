"""DecisionEngine: classify decisions as BUILD / FIX / KILL / DEFER / APPROVE.

Decision = impact + urgency + risk reduction + founder leverage - complexity.
A Trust OS violation always returns REJECT or ESCALATE regardless of scores.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DecisionType(str, Enum):
    BUILD = "BUILD"
    FIX = "FIX"
    KILL = "KILL"
    DEFER = "DEFER"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    ESCALATE = "ESCALATE"


@dataclass
class DecisionInput:
    title: str
    revenue_impact: int  # 0..10
    urgency: int  # 0..10
    risk_reduction: int  # 0..10
    founder_leverage: int  # 0..10
    complexity: int  # 0..10
    trust_violation: bool = False


@dataclass
class DecisionResult:
    decision: DecisionType
    rationale: str
    score: int


class DecisionEngine:
    """Rule-driven classifier for CEO-level decisions."""

    def classify(self, item: DecisionInput) -> DecisionResult:
        score = (
            item.revenue_impact
            + item.urgency
            + item.risk_reduction
            + item.founder_leverage
            - item.complexity
        )

        if item.trust_violation:
            return DecisionResult(
                decision=DecisionType.REJECT,
                rationale="Trust OS violation: trust overrides all other systems.",
                score=score,
            )

        if item.risk_reduction >= 8:
            return DecisionResult(
                decision=DecisionType.FIX,
                rationale="High risk reduction; fix now.",
                score=score,
            )

        if item.revenue_impact >= 8 and item.urgency >= 7:
            return DecisionResult(
                decision=DecisionType.BUILD,
                rationale="High revenue impact and urgent; build or fix now.",
                score=score,
            )

        if item.founder_leverage >= 8 and item.complexity <= 5:
            return DecisionResult(
                decision=DecisionType.BUILD,
                rationale="High founder leverage at acceptable complexity.",
                score=score,
            )

        if item.complexity >= 8 and item.revenue_impact <= 5:
            return DecisionResult(
                decision=DecisionType.DEFER,
                rationale="High complexity without proportional revenue impact.",
                score=score,
            )

        if item.revenue_impact <= 2 and item.founder_leverage <= 2:
            return DecisionResult(
                decision=DecisionType.KILL,
                rationale="No revenue or leverage justification.",
                score=score,
            )

        if score >= 18:
            return DecisionResult(
                decision=DecisionType.APPROVE,
                rationale="Aggregate score warrants approval.",
                score=score,
            )

        return DecisionResult(
            decision=DecisionType.DEFER,
            rationale="Insufficient signal to act now.",
            score=score,
        )

    @staticmethod
    def explain(result: DecisionResult, title: Optional[str] = None) -> str:
        prefix = f"[{title}] " if title else ""
        return f"{prefix}{result.decision.value} (score={result.score}) — {result.rationale}"
