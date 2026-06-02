"""Sending Ramp OS — caps on *human-approved* sends per day.

This module never sends. It computes how many already-approved drafts may
be released today, and refuses (returns 0) unless every send condition is
met together. The ramp protects domain reputation; volume never overrides
it.
"""

from __future__ import annotations

from dataclasses import dataclass

# week -> (soft_floor, hard_cap). Only the cap is enforced; the floor is a
# planning guide for the founder.
RAMP: dict[int, tuple[int, int]] = {
    0: (0, 20),
    1: (25, 50),
    2: (50, 100),
    3: (100, 150),
    4: (150, 250),
}


@dataclass(frozen=True, slots=True)
class RampDecision:
    allowed_sends: int
    cap: int
    blocked: bool
    reasons: tuple[str, ...]


def max_sends_for_week(week: int) -> int:
    """Hard cap for a given warm-up week (week >= 4 uses the 4+ band)."""
    if week < 0:
        return 0
    key = min(week, 4)
    return RAMP[key][1]


def allowed_sends_today(
    *,
    week: int,
    approved_count: int,
    has_approval: bool,
    domain_health_ok: bool,
    suppression_ok: bool,
    personalization_ok: bool,
    risk_ok: bool = True,
) -> RampDecision:
    """All conditions must hold; otherwise 0 sends are permitted.

    Conditions mirror the doctrine: approval + unsubscribe/suppression
    hygiene + domain health + personalization >= P1 + acceptable risk.
    """
    reasons: list[str] = []
    if not has_approval:
        reasons.append("no_founder_approval")
    if not domain_health_ok:
        reasons.append("domain_health_not_ok")
    if not suppression_ok:
        reasons.append("suppression_check_failed")
    if not personalization_ok:
        reasons.append("personalization_below_p1")
    if not risk_ok:
        reasons.append("risk_too_high")
    if approved_count <= 0:
        reasons.append("no_approved_drafts")

    cap = max_sends_for_week(week)
    if reasons:
        return RampDecision(0, cap, blocked=True, reasons=tuple(reasons))
    return RampDecision(min(approved_count, cap), cap, blocked=False, reasons=())


__all__ = ["RAMP", "RampDecision", "allowed_sends_today", "max_sends_for_week"]
