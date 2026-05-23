"""
System scorecard.

A scorecard is a 0..100 score for a named operating system, with the
contributing signals and the verifier that produced them. The composite
company-health score uses these.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SystemScorecard:
    name: str
    score: int  # 0..100
    signals: dict[str, float]
    verifier: str

    @property
    def band(self) -> str:
        if self.score >= 80:
            return "HEALTHY"
        if self.score >= 60:
            return "WATCH"
        return "ALERT"


def score_system(
    name: str,
    *,
    signals: dict[str, float],
    weights: dict[str, float] | None = None,
    verifier: str = "scripts/verify_company_os.py",
) -> SystemScorecard:
    """Score a system from named signals in [0, 1].

    If weights are omitted, each signal is weighted equally.
    """
    if not signals:
        return SystemScorecard(name=name, score=0, signals={}, verifier=verifier)
    weights = weights or {k: 1.0 for k in signals}
    total_weight = sum(weights.get(k, 0.0) for k in signals)
    if total_weight <= 0:
        return SystemScorecard(name=name, score=0, signals=signals, verifier=verifier)
    weighted = sum(
        max(0.0, min(1.0, float(v))) * weights.get(k, 0.0)
        for k, v in signals.items()
    )
    score = int(round((weighted / total_weight) * 100))
    return SystemScorecard(
        name=name,
        score=max(0, min(100, score)),
        signals=signals,
        verifier=verifier,
    )
