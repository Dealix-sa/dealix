"""Scale / Kill Engine — weekly review that decides what to scale, pause, or kill."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.schemas import Opportunity, OutcomeStatus


Verdict = Literal["scale", "pause", "kill", "hold"]


@dataclass
class ScaleVerdict:
    opportunity_id: str
    title: str
    verdict: Verdict
    reason: str
    outcomes_total: int
    revenue_sar: float
    score: float


def review(opp: Opportunity, *, paying_threshold: int = 2, dead_threshold: int = 50) -> ScaleVerdict:
    """Return a scale/pause/kill verdict for an opportunity based on its outcomes."""
    out_store = get_outcome_store()
    # We don't have a direct opp→outcome index; this is a best-effort summary.
    all_outcomes = out_store.list()
    revenue = sum(o.revenue_sar for o in all_outcomes if o.revenue_sar > 0)
    paying = sum(1 for o in all_outcomes if o.status == OutcomeStatus.PAID.value)
    ignored = sum(1 for o in all_outcomes if o.status == OutcomeStatus.IGNORED.value)

    if paying >= paying_threshold:
        v: Verdict = "scale"
        reason = f"Has {paying} paying outcomes — scale rule met."
    elif ignored >= dead_threshold:
        v = "kill"
        reason = f"Ignored {ignored} times — kill rule met."
    elif opp.score < 1.0:
        v = "pause"
        reason = "Low opportunity score — pause and re-evaluate."
    else:
        v = "hold"
        reason = "Not enough signal yet — keep observing."

    return ScaleVerdict(
        opportunity_id=opp.id,
        title=opp.title,
        verdict=v,
        reason=reason,
        outcomes_total=len(all_outcomes),
        revenue_sar=revenue,
        score=opp.score,
    )
