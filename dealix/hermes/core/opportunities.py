"""Opportunity Layer — turns signals into scored, sovereignty-classified opportunities."""

from __future__ import annotations

from threading import RLock

from dealix.hermes.core.schemas import (
    Opportunity,
    OpportunityType,
    Signal,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.core.scoring import classify_sovereignty, score_opportunity


_SIGNAL_TO_OPP: dict[str, OpportunityType] = {
    SignalType.CUSTOMER.value: OpportunityType.CUSTOMER,
    SignalType.PARTNER.value: OpportunityType.PARTNER,
    SignalType.PRODUCT.value: OpportunityType.PRODUCT,
    SignalType.MARKET.value: OpportunityType.REPORT,
    SignalType.MONEY.value: OpportunityType.CUSTOMER,
    SignalType.TRAINING.value: OpportunityType.TRAINING,
    SignalType.VENTURE.value: OpportunityType.VENTURE,
    SignalType.API.value: OpportunityType.API,
    SignalType.TRUST.value: OpportunityType.GOVERNANCE,
    SignalType.RISK.value: OpportunityType.GOVERNANCE,
    SignalType.PERSONAL.value: OpportunityType.PERSONAL_WEALTH,
}


class OpportunityStore:
    def __init__(self) -> None:
        self._items: dict[str, Opportunity] = {}
        self._lock = RLock()

    def evaluate(
        self,
        signal: Signal,
        *,
        opportunity_type: OpportunityType | str | None = None,
        title: str | None = None,
        description: str = "",
        estimated_value_sar: float = 0.0,
        cash_speed: int = 3,
        strategic: int = 3,
        repeatability: int = 3,
        data_moat: int = 3,
        difficulty: int = 3,
        risk: int = 2,
        recommended_action: str = "",
    ) -> Opportunity:
        """Promote a signal into a scored opportunity, or archive (returns minimal opp)."""
        otype = (
            OpportunityType(opportunity_type)
            if opportunity_type
            else _SIGNAL_TO_OPP.get(signal.signal_type, OpportunityType.REPORT)
        )
        opp = Opportunity(
            signal_id=signal.id,
            opportunity_type=otype,
            title=title or signal.title,
            description=description or signal.content,
            estimated_value_sar=estimated_value_sar,
            cash_speed_score=cash_speed,
            strategic_score=strategic,
            repeatability_score=repeatability,
            data_moat_score=data_moat,
            difficulty_score=difficulty,
            risk_score=risk,
            recommended_action=recommended_action or "Review and prioritise",
        )
        opp = opp.model_copy(
            update={
                "score": score_opportunity(opp),
                "sovereignty_level": classify_sovereignty(opp).value,
            }
        )
        with self._lock:
            self._items[opp.id] = opp
        return opp

    def get(self, opp_id: str) -> Opportunity | None:
        with self._lock:
            return self._items.get(opp_id)

    def list(
        self,
        *,
        status: str | None = None,
        min_score: float | None = None,
        sovereignty_level: SovereigntyLevel | str | None = None,
    ) -> list[Opportunity]:
        with self._lock:
            items = list(self._items.values())
        if status:
            items = [o for o in items if o.status == status]
        if min_score is not None:
            items = [o for o in items if o.score >= min_score]
        if sovereignty_level:
            lvl = sovereignty_level.value if isinstance(sovereignty_level, SovereigntyLevel) else sovereignty_level
            items = [o for o in items if o.sovereignty_level == lvl]
        return sorted(items, key=lambda o: o.score, reverse=True)

    def update_status(self, opp_id: str, status: str) -> Opportunity | None:
        with self._lock:
            opp = self._items.get(opp_id)
            if opp is None:
                return None
            updated = opp.model_copy(update={"status": status})
            self._items[opp_id] = updated
            return updated

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_store: OpportunityStore | None = None


def get_opportunity_store() -> OpportunityStore:
    global _default_store
    if _default_store is None:
        _default_store = OpportunityStore()
    return _default_store
