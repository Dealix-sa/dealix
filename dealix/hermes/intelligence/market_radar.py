"""MarketRadar — collects market signals and emits Hermes Signal objects.

Section 119: a market signal must lead to one of {campaign, report, offer,
risk_warning, lead_list, partner_target}. The radar enforces that by
tagging the emitted Signal with ``intent``.
"""

from __future__ import annotations

from enum import Enum

from dealix.hermes.core.schemas import Signal


class MarketSignalKind(str, Enum):
    TREND = "trend"
    REGULATION = "regulation"
    TENDER = "tender"
    COMPETITOR = "competitor"
    HIRING = "hiring"
    FUNDING = "funding"


_ALLOWED_INTENTS = {"campaign", "report", "offer", "risk_warning", "lead_list", "partner_target"}


class MarketRadar:
    def emit(
        self,
        *,
        kind: MarketSignalKind,
        summary: str,
        intent: str,
        sector: str | None = None,
        risk_hint: str = "low",
    ) -> Signal:
        if intent not in _ALLOWED_INTENTS:
            raise ValueError(f"intent must be one of {_ALLOWED_INTENTS}, got {intent!r}.")
        sig = Signal.make(
            source="market_radar",
            domain="market",
            summary=summary,
            risk_hint=risk_hint,
            payload={"kind": kind.value, "intent": intent, "sector": sector or "general"},
            tags=[kind.value, intent, sector or "general"],
        )
        return sig


__all__ = ["MarketRadar", "MarketSignalKind"]
