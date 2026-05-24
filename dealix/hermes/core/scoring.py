"""Scoring functions — opportunity, money priority, kill/scale."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import MoneyAction, Opportunity

# Weights tuned for cash-first founder mode. They sum to ~1.0 on the
# upside and apply a small risk penalty. Adjust here in one place.
W_CASH_SPEED = 0.30
W_CLOSE_PROB = 0.25
W_STRATEGIC = 0.20
W_VALUE = 0.10
W_RISK_PENALTY = 0.15

# Value normaliser — every 10k SAR contributes ~10 score points.
VALUE_DIVISOR = 1000.0


def money_priority_score(action: MoneyAction) -> float:
    """Compute the priority score used to rank money actions.

    The score is bounded roughly to [-15, 130]. Higher = ship now.
    """
    value_component = 0.0
    if action.estimated_value_sar:
        value_component = min(action.estimated_value_sar / VALUE_DIVISOR, 100.0)

    score = (
        action.cash_speed_score * W_CASH_SPEED
        + (action.close_probability * 100.0) * W_CLOSE_PROB
        + action.strategic_value_score * W_STRATEGIC
        + value_component * W_VALUE
        - action.risk_score * W_RISK_PENALTY
    )
    return round(score, 2)


def opportunity_score(opp: Opportunity) -> float:
    """Score an opportunity using the same weights as money actions."""
    value_component = 0.0
    if opp.estimated_value_sar:
        value_component = min(opp.estimated_value_sar / VALUE_DIVISOR, 100.0)

    score = (
        opp.cash_speed_score * W_CASH_SPEED
        + (opp.close_probability * 100.0) * W_CLOSE_PROB
        + opp.strategic_value_score * W_STRATEGIC
        + value_component * W_VALUE
        - opp.risk_score * W_RISK_PENALTY
    )
    return round(score, 2)


@dataclass(frozen=True)
class KillScaleRecommendation:
    scale: list[str]
    pause_or_kill: list[str]
    reasoning: dict[str, str]


def kill_or_scale(actions: list[MoneyAction]) -> KillScaleRecommendation:
    """Decide which money actions to scale and which to pause.

    Scale rules: priority >= 60 and risk <= 40.
    Pause rules: priority < 25 or risk >= 70.
    Anything else stays as-is and is not surfaced.
    """
    scale: list[str] = []
    pause: list[str] = []
    reasoning: dict[str, str] = {}

    for a in actions:
        score = a.money_priority_score or money_priority_score(a)
        if score >= 60 and a.risk_score <= 40:
            scale.append(a.title)
            reasoning[a.title] = f"priority {score:.1f}, risk {a.risk_score} — scale"
        elif score < 25 or a.risk_score >= 70:
            pause.append(a.title)
            reasoning[a.title] = (
                f"priority {score:.1f}, risk {a.risk_score} — pause/kill"
            )

    return KillScaleRecommendation(
        scale=scale, pause_or_kill=pause, reasoning=reasoning
    )


def rank_money_actions(actions: list[MoneyAction]) -> list[MoneyAction]:
    """Return actions sorted by money priority score descending.

    Side effect: each action gets `money_priority_score` populated.
    """
    for a in actions:
        a.money_priority_score = money_priority_score(a)
    return sorted(actions, key=lambda a: a.money_priority_score, reverse=True)


def rank_opportunities(opps: list[Opportunity]) -> list[Opportunity]:
    """Return opportunities ranked by score descending."""
    for o in opps:
        o.money_priority_score = opportunity_score(o)
    return sorted(opps, key=lambda o: o.money_priority_score, reverse=True)
