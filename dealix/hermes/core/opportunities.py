"""Opportunity Graph — converts signals into scored opportunities.

Scoring blends estimated value, close probability, fit, urgency, and risk
into an `expected_value_sar`. Risk *reduces* expected value; high risk +
low fit pushes the opportunity toward the kill pile.
"""

from __future__ import annotations

from collections.abc import Iterable

from dealix.hermes import ValueOutput
from dealix.hermes.core.schemas import (
    Opportunity,
    OpportunityKind,
    Signal,
)


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def score_expected_value(
    *,
    estimated_value_sar: float,
    close_probability: float,
    fit_score: float,
    urgency_score: float,
    risk_score: float,
) -> float:
    """Risk-adjusted expected value used for ranking and kill/scale calls."""
    fit = _clip01(fit_score)
    urgency = _clip01(urgency_score)
    risk = _clip01(risk_score)
    prob = _clip01(close_probability)
    quality = fit * 0.6 + urgency * 0.4
    risk_penalty = 1.0 - 0.7 * risk
    return max(0.0, estimated_value_sar) * prob * quality * risk_penalty


class OpportunityGraph:
    """In-memory opportunity store + ranker."""

    def __init__(self) -> None:
        self._store: dict[str, Opportunity] = {}

    def register(
        self,
        *,
        source_signals: Iterable[Signal],
        kind: OpportunityKind,
        title: str,
        buyer_segment: str,
        estimated_value_sar: float,
        close_probability: float,
        fit_score: float,
        urgency_score: float,
        risk_score: float,
        proposed_value_outputs: list[ValueOutput],
        notes: str = "",
    ) -> Opportunity:
        signals = list(source_signals)
        if not signals:
            raise ValueError("at least one source signal is required")

        expected = score_expected_value(
            estimated_value_sar=estimated_value_sar,
            close_probability=close_probability,
            fit_score=fit_score,
            urgency_score=urgency_score,
            risk_score=risk_score,
        )

        opp = Opportunity(
            source_signal_ids=[s.signal_id for s in signals],
            kind=kind,
            title=title,
            buyer_segment=buyer_segment,
            estimated_value_sar=estimated_value_sar,
            close_probability=close_probability,
            fit_score=fit_score,
            urgency_score=urgency_score,
            risk_score=risk_score,
            expected_value_sar=expected,
            proposed_value_outputs=proposed_value_outputs,
            notes=notes,
        )
        self._store[opp.opportunity_id] = opp
        return opp

    def top(self, n: int = 10) -> list[Opportunity]:
        return sorted(
            self._store.values(),
            key=lambda o: o.expected_value_sar,
            reverse=True,
        )[:n]

    def by_kind(self, kind: OpportunityKind) -> list[Opportunity]:
        return [o for o in self._store.values() if o.kind is kind]

    def get(self, opportunity_id: str) -> Opportunity | None:
        return self._store.get(opportunity_id)

    def all(self) -> list[Opportunity]:
        return list(self._store.values())

    def kill_pile(self, threshold_sar: float = 100.0) -> list[Opportunity]:
        """Opportunities whose expected value is below `threshold_sar` AND
        whose risk dominates fit — these are honestly waste.
        """
        return [
            o
            for o in self._store.values()
            if o.expected_value_sar < threshold_sar and o.risk_score > o.fit_score
        ]


__all__ = ["OpportunityGraph", "score_expected_value"]
