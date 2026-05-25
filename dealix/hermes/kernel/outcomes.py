"""Phase 5: Outcomes logged after every Execution. No Execution skips this."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.kernel.schemas import (
    Execution,
    LifecycleEvent,
    Outcome,
    OutcomeStatus,
)


@dataclass
class OutcomeStore:
    _outcomes: dict[str, Outcome] = field(default_factory=dict)
    _by_execution: dict[str, str] = field(default_factory=dict)
    _events: list[LifecycleEvent] = field(default_factory=list)

    def log(
        self,
        execution: Execution,
        *,
        status: OutcomeStatus,
        actual_result: str,
        revenue_sar: float = 0.0,
        cost_sar: float = 0.0,
        learning: str = "",
        asset_review_required: bool = False,
        attribution_links: list[str] | None = None,
        metrics: dict[str, float] | None = None,
    ) -> Outcome:
        if execution.execution_id in self._by_execution:
            raise ValueError(f"execution {execution.execution_id} already has an outcome logged")
        outcome = Outcome(
            execution_id=execution.execution_id,
            status=status,
            actual_result=actual_result,
            revenue_sar=revenue_sar,
            cost_sar=cost_sar,
            margin_sar=revenue_sar - cost_sar,
            learning=learning,
            asset_review_required=asset_review_required,
            attribution_links=attribution_links or [],
            metrics=metrics or {},
        )
        self._outcomes[outcome.outcome_id] = outcome
        self._by_execution[execution.execution_id] = outcome.outcome_id
        self._events.append(LifecycleEvent(
            event_type="outcome.logged",
            entity_id=outcome.outcome_id,
            sovereignty_level=execution.sovereignty_level,
            payload={"status": status.value, "revenue_sar": revenue_sar},
        ))
        return outcome

    def verify_revenue(self, outcome_id: str) -> Outcome:
        o = self._outcomes[outcome_id]
        updated = o.model_copy(update={"revenue_verified": True})
        self._outcomes[outcome_id] = updated
        return updated

    def link_attribution(self, outcome_id: str, link: str) -> Outcome:
        o = self._outcomes[outcome_id]
        new_links = [*o.attribution_links, link]
        updated = o.model_copy(update={"attribution_links": new_links})
        self._outcomes[outcome_id] = updated
        return updated

    def get(self, outcome_id: str) -> Outcome:
        return self._outcomes[outcome_id]

    def for_execution(self, execution_id: str) -> Outcome | None:
        oid = self._by_execution.get(execution_id)
        return self._outcomes.get(oid) if oid else None

    def list(self) -> list[Outcome]:
        return list(self._outcomes.values())

    def events(self) -> list[LifecycleEvent]:
        return list(self._events)
