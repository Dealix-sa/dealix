"""Phase 2: turn Signals into scored Opportunities."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.kernel.schemas import (
    LifecycleEvent,
    Opportunity,
    OpportunityType,
    RecommendedAction,
    Signal,
    SovereigntyLevel,
)
from dealix.hermes.kernel.scoring import recommend, score_opportunity


@dataclass
class OpportunityStore:
    _opps: dict[str, Opportunity] = field(default_factory=dict)
    _events: list[LifecycleEvent] = field(default_factory=list)

    def create_from_signal(
        self,
        signal: Signal,
        *,
        opportunity_type: OpportunityType,
        title: str,
        estimated_value_sar: float = 0.0,
        scores: dict[str, int] | None = None,
        sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL,
        assigned_engine: str | None = None,
    ) -> Opportunity:
        scores = scores or {}
        opp = Opportunity(
            signal_id=signal.signal_id,
            opportunity_type=opportunity_type,
            title=title,
            estimated_value_sar=estimated_value_sar,
            cash_speed_score=scores.get("cash_speed_score", 0),
            strategic_score=scores.get("strategic_score", 0),
            repeatability_score=scores.get("repeatability_score", 0),
            data_moat_score=scores.get("data_moat_score", 0),
            difficulty_score=scores.get("difficulty_score", 0),
            risk_score=scores.get("risk_score", 0),
            sovereignty_level=sovereignty_level,
            assigned_engine=assigned_engine,
            owner=signal.owner,
        )
        scored = self.score(opp)
        self._opps[scored.opportunity_id] = scored
        self._events.append(LifecycleEvent(
            event_type="opportunity.created",
            entity_id=scored.opportunity_id,
            workspace_id=signal.workspace_id,
            sovereignty_level=sovereignty_level,
            payload={"composite_score": scored.composite_score},
        ))
        return scored

    def score(self, opp: Opportunity) -> Opportunity:
        composite = score_opportunity(opp)
        action = recommend(opp.model_copy(update={"composite_score": composite}))
        scored = opp.model_copy(update={
            "composite_score": composite,
            "recommended_action": action,
        })
        self._opps[scored.opportunity_id] = scored
        self._events.append(LifecycleEvent(
            event_type="opportunity.scored",
            entity_id=scored.opportunity_id,
            payload={"composite_score": composite, "recommended_action": action.value},
        ))
        return scored

    def assign_engine(self, opportunity_id: str, engine: str) -> Opportunity:
        opp = self._opps[opportunity_id]
        updated = opp.model_copy(update={"assigned_engine": engine})
        self._opps[opportunity_id] = updated
        return updated

    def get(self, opportunity_id: str) -> Opportunity:
        return self._opps[opportunity_id]

    def list(self) -> list[Opportunity]:
        return list(self._opps.values())

    def events(self) -> list[LifecycleEvent]:
        return list(self._events)
