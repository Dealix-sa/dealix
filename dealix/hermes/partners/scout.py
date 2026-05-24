"""Partner Scout — converts partner signals into qualified partner opportunities."""

from __future__ import annotations

from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.core.schemas import OpportunityType, Signal, SignalType


class PartnerScout:
    def qualify(self, signal: Signal, *, estimated_value_sar: float = 25_000.0):
        if signal.signal_type != SignalType.PARTNER.value:
            return None
        return get_opportunity_store().evaluate(
            signal,
            opportunity_type=OpportunityType.PARTNER,
            estimated_value_sar=estimated_value_sar,
            cash_speed=3,
            strategic=5,
            repeatability=5,
            data_moat=4,
            difficulty=3,
            risk=2,
            recommended_action="Draft partner pitch + revenue share model",
        )
