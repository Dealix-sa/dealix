"""Heuristics for cash-speed and risk scoring of an opportunity.

These functions encode the founder's rules of thumb. They run before
the generic `scoring.money_priority_score` so each opportunity arrives
at the ranker with sensible component scores.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import Opportunity, Signal, SignalSource

# Sources that historically convert fastest.
FAST_SOURCES: frozenset[SignalSource] = frozenset(
    {
        SignalSource.INBOUND_LEAD,
        SignalSource.PARTNER_REFERRAL,
        SignalSource.SUPPORT_CHANNEL,
    }
)

SLOW_SOURCES: frozenset[SignalSource] = frozenset(
    {SignalSource.SECTOR_RADAR, SignalSource.MARKET_NEWS}
)


def cash_speed_score_for(signal: Signal, value_sar: float | None) -> int:
    """Return cash-speed score in [0, 100]."""
    base = 40
    if signal.source in FAST_SOURCES:
        base += 35
    elif signal.source in SLOW_SOURCES:
        base -= 15

    # High-value deals close slower in this market — penalise lightly.
    if value_sar is not None:
        if value_sar < 2_000:
            base += 15
        elif value_sar < 10_000:
            base += 5
        elif value_sar > 50_000:
            base -= 15

    return max(0, min(100, base))


def close_probability_for(signal: Signal, sector: str | None) -> float:
    """Return close probability in [0, 1]."""
    base = 0.25
    if signal.source == SignalSource.INBOUND_LEAD:
        base += 0.30
    elif signal.source == SignalSource.PARTNER_REFERRAL:
        base += 0.25
    elif signal.source == SignalSource.SUPPORT_CHANNEL:
        base += 0.15

    if sector and sector.lower() in {"agencies", "consultants", "training_centers"}:
        base += 0.10
    return max(0.0, min(1.0, base))


def risk_score_for(signal: Signal, value_sar: float | None) -> int:
    """Return risk score in [0, 100]. Higher = more risky."""
    base = 20
    if signal.source == SignalSource.OUTBOUND_RESEARCH:
        base += 10
    if signal.source == SignalSource.INTERNAL_OBSERVATION:
        base += 5
    if value_sar is not None and value_sar > 25_000:
        base += 20
    return max(0, min(100, base))


def strategic_value_score_for(signal: Signal, recommended_offer: str | None) -> int:
    """Return strategic value score in [0, 100]."""
    base = 30
    if recommended_offer and "white_label" in recommended_offer.lower():
        base += 30
    if recommended_offer and "enterprise" in recommended_offer.lower():
        base += 25
    if signal.source == SignalSource.PARTNER_REFERRAL:
        base += 15
    return max(0, min(100, base))


def hydrate(opp: Opportunity, signal: Signal) -> Opportunity:
    """Populate component scores on an opportunity in place."""
    opp.cash_speed_score = cash_speed_score_for(signal, opp.estimated_value_sar)
    opp.close_probability = close_probability_for(signal, opp.sector)
    opp.risk_score = risk_score_for(signal, opp.estimated_value_sar)
    opp.strategic_value_score = strategic_value_score_for(signal, opp.recommended_offer)
    return opp
