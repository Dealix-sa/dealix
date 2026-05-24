"""Outcome Layer — every execution MUST resolve to a recorded outcome."""

from __future__ import annotations

from threading import RLock

from dealix.hermes.core.schemas import Execution, Outcome, OutcomeStatus


class OutcomeStore:
    def __init__(self) -> None:
        self._items: dict[str, Outcome] = {}
        self._by_execution: dict[str, str] = {}
        self._lock = RLock()

    def record(
        self,
        execution: Execution,
        *,
        status: OutcomeStatus | str,
        actual_result: str = "",
        revenue_sar: float = 0.0,
        time_saved_minutes: int = 0,
        risk_reduced: bool = False,
        learning: str = "",
        asset_review_required: bool = True,
    ) -> Outcome:
        out = Outcome(
            execution_id=execution.id,
            status=OutcomeStatus(status),
            actual_result=actual_result,
            revenue_sar=revenue_sar,
            time_saved_minutes=time_saved_minutes,
            risk_reduced=risk_reduced,
            learning=learning,
            asset_review_required=asset_review_required,
        )
        with self._lock:
            self._items[out.id] = out
            self._by_execution[execution.id] = out.id
        return out

    def get(self, outcome_id: str) -> Outcome | None:
        with self._lock:
            return self._items.get(outcome_id)

    def for_execution(self, execution_id: str) -> Outcome | None:
        with self._lock:
            oid = self._by_execution.get(execution_id)
            return self._items.get(oid) if oid else None

    def list(self, *, status: OutcomeStatus | str | None = None) -> list[Outcome]:
        with self._lock:
            items = list(self._items.values())
        if status:
            sval = OutcomeStatus(status).value
            items = [o for o in items if o.status == sval]
        return sorted(items, key=lambda o: o.created_at, reverse=True)

    def attach_asset(self, outcome_id: str, asset_id: str) -> Outcome | None:
        with self._lock:
            out = self._items.get(outcome_id)
            if out is None:
                return None
            updated = out.model_copy(
                update={"asset_id": asset_id, "asset_review_required": False}
            )
            self._items[outcome_id] = updated
            return updated

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            self._by_execution.clear()


_default_store: OutcomeStore | None = None


def get_outcome_store() -> OutcomeStore:
    global _default_store
    if _default_store is None:
        _default_store = OutcomeStore()
    return _default_store
