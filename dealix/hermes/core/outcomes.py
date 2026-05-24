"""Outcome Logger — every plan must end with an outcome.

A `won` outcome with `realised_value_sar > 0` requires `OutcomeKind.PAID`
support (an `invoice_paid` flag in the payload) before the orchestrator
treats it as cash. We never count promises as revenue.
"""

from __future__ import annotations

from collections.abc import Iterable

from dealix.hermes import ValueOutput
from dealix.hermes.core.schemas import Outcome, OutcomeKind


class OutcomeLog:
    def __init__(self) -> None:
        self._store: dict[str, Outcome] = {}

    def record(
        self,
        *,
        opportunity_id: str,
        kind: OutcomeKind,
        summary: str,
        recorded_by: str,
        plan_id: str | None = None,
        realised_value_sar: float = 0.0,
        realised_outputs: Iterable[ValueOutput] | None = None,
        next_action: str | None = None,
    ) -> Outcome:
        if kind is OutcomeKind.PAID and realised_value_sar <= 0:
            raise ValueError("PAID outcome must include a positive realised value")
        if kind is OutcomeKind.WON and realised_value_sar > 0:
            # Won-but-not-paid is fine; we just don't claim cash until PAID
            pass

        outcome = Outcome(
            opportunity_id=opportunity_id,
            plan_id=plan_id,
            kind=kind,
            realised_value_sar=realised_value_sar,
            realised_outputs=[
                v for v in (realised_outputs or []) if v is not ValueOutput.WASTE
            ],
            summary=summary,
            recorded_by=recorded_by,
            next_action=next_action,
        )
        self._store[outcome.outcome_id] = outcome
        return outcome

    def mark_asset_reviewed(self, outcome_id: str) -> Outcome:
        o = self._store.get(outcome_id)
        if o is None:
            raise KeyError(outcome_id)
        o = o.model_copy(update={"asset_review_done": True})
        self._store[outcome_id] = o
        return o

    def get(self, outcome_id: str) -> Outcome | None:
        return self._store.get(outcome_id)

    def all(self) -> list[Outcome]:
        return list(self._store.values())

    def cash_collected_sar(self) -> float:
        return sum(
            o.realised_value_sar
            for o in self._store.values()
            if o.kind is OutcomeKind.PAID
        )

    def pending_asset_review(self) -> list[Outcome]:
        return [
            o
            for o in self._store.values()
            if not o.asset_review_done
            and o.kind in {OutcomeKind.WON, OutcomeKind.PAID, OutcomeKind.LEARNING}
        ]


__all__ = ["OutcomeLog"]
