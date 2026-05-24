"""Decision Layer — turns an opportunity into a bounded, justified choice."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock

from dealix.hermes.core.schemas import (
    Decision,
    Opportunity,
    RiskLevel,
    SovereigntyLevel,
)


class DecisionStore:
    def __init__(self) -> None:
        self._items: dict[str, Decision] = {}
        self._lock = RLock()

    def propose(
        self,
        opportunity: Opportunity,
        *,
        decision_type: str = "execute",
        context: str = "",
        options: list[str] | None = None,
        recommendation: str = "",
        risk_level: RiskLevel | str = RiskLevel.LOW,
    ) -> Decision:
        sov = SovereigntyLevel(opportunity.sovereignty_level)
        requires_approval = sov in {
            SovereigntyLevel.S2_SAMI_APPROVAL,
            SovereigntyLevel.S4_SOVEREIGN_ONLY,
            SovereigntyLevel.S5_NEVER_AUTONOMOUS,
        }
        dec = Decision(
            opportunity_id=opportunity.id,
            decision_type=decision_type,
            context=context or f"Opportunity score {opportunity.score}",
            options=options or [recommendation or "Proceed", "Defer", "Kill"],
            recommendation=recommendation or "Proceed",
            risk_level=RiskLevel(risk_level),
            sovereignty_level=sov,
            requires_approval=requires_approval,
        )
        with self._lock:
            self._items[dec.id] = dec
        return dec

    def get(self, decision_id: str) -> Decision | None:
        with self._lock:
            return self._items.get(decision_id)

    def approve(self, decision_id: str, approver: str = "Sami") -> Decision | None:
        with self._lock:
            dec = self._items.get(decision_id)
            if dec is None:
                return None
            updated = dec.model_copy(
                update={
                    "approved_by": approver,
                    "approved_at": datetime.now(timezone.utc),
                    "requires_approval": False,
                }
            )
            self._items[decision_id] = updated
            return updated

    def reject(self, decision_id: str, reason: str) -> Decision | None:
        with self._lock:
            dec = self._items.get(decision_id)
            if dec is None:
                return None
            updated = dec.model_copy(
                update={
                    "decision_type": "kill",
                    "rejection_reason": reason,
                    "requires_approval": False,
                }
            )
            self._items[decision_id] = updated
            return updated

    def list(self, *, pending_only: bool = False) -> list[Decision]:
        with self._lock:
            items = list(self._items.values())
        if pending_only:
            items = [d for d in items if d.requires_approval]
        return sorted(items, key=lambda d: d.created_at, reverse=True)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_store: DecisionStore | None = None


def get_decision_store() -> DecisionStore:
    global _default_store
    if _default_store is None:
        _default_store = DecisionStore()
    return _default_store
