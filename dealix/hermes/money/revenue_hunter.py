"""Revenue Hunter — turns customer signals into qualified money opportunities."""

from __future__ import annotations

from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.core.schemas import OpportunityType, Signal, SignalType


class RevenueHunter:
    def qualify(self, signal: Signal, *, estimated_value_sar: float = 5_000.0):
        if signal.signal_type not in {
            SignalType.CUSTOMER.value,
            SignalType.MONEY.value,
            SignalType.PARTNER.value,
        }:
            return None
        return get_opportunity_store().evaluate(
            signal,
            opportunity_type=OpportunityType.CUSTOMER,
            estimated_value_sar=estimated_value_sar,
            cash_speed=4,
            strategic=4,
            repeatability=4,
            data_moat=3,
            difficulty=2,
            risk=2,
            recommended_action="Send qualifying questions + price range",
        )
