"""
Opportunity scoring — weighted, deterministic, explainable.

The score blends six dimensions:
    + cash speed       (how fast it pays)
    + strategic value  (compounding, moat)
    + repeatability    (can it become a product?)
    + data moat        (does it add to our advantage?)
    - difficulty       (effort/coordination cost)
    - risk             (legal, reputational, financial)

``should_execute_now`` is the gate the Orchestrator uses to decide:
execute now vs. queue vs. archive.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import HermesOpportunity

DEFAULT_EXECUTE_THRESHOLD = 2.7


def opportunity_score(o: HermesOpportunity) -> float:
    return (
        o.cash_speed_score * 0.25
        + o.strategic_score * 0.20
        + o.repeatability_score * 0.20
        + o.data_moat_score * 0.15
        - o.difficulty_score * 0.10
        - o.risk_score * 0.10
    )


def should_execute_now(
    o: HermesOpportunity,
    threshold: float = DEFAULT_EXECUTE_THRESHOLD,
) -> bool:
    return opportunity_score(o) >= threshold


def score_breakdown(o: HermesOpportunity) -> dict[str, float]:
    """Return the per-dimension contribution to the final score."""
    return {
        "cash_speed": o.cash_speed_score * 0.25,
        "strategic": o.strategic_score * 0.20,
        "repeatability": o.repeatability_score * 0.20,
        "data_moat": o.data_moat_score * 0.15,
        "difficulty_penalty": -o.difficulty_score * 0.10,
        "risk_penalty": -o.risk_score * 0.10,
        "total": opportunity_score(o),
    }
