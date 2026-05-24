"""
Founder brief agent — the daily sovereign one-pager.

Pulls from the Kernel stores (opportunities, decisions, outcomes, assets)
and returns the smallest set of things Sami needs to decide today.
"""

from __future__ import annotations

from pydantic import BaseModel

from dealix.hermes.core.decisions import default_store as default_decision_store
from dealix.hermes.core.opportunities import default_store as default_opportunity_store
from dealix.hermes.core.outcomes import default_store as default_outcome_store


class FounderBrief(BaseModel):
    today_fastest_cash_action: str
    highest_strategic_opportunity: str
    pending_approvals: list[str]
    risks: list[str]
    next_best_actions: list[str]


def build_brief() -> FounderBrief:
    ranked = default_opportunity_store().ranked()
    fastest = ranked[0][1].title if ranked else "Sell Revenue Hunter Pilot"
    strategic = next(
        (o.title for _, o, _ in ranked if o.strategic_score >= 4),
        "AI Trust Kit for regulated companies",
    )
    pending = [
        f"Decision: {m.decision_title}" for _, m in default_decision_store().pending_approvals()
    ]
    wins = default_outcome_store().wins()

    return FounderBrief(
        today_fastest_cash_action=fastest,
        highest_strategic_opportunity=strategic,
        pending_approvals=pending,
        risks=["No external actions should run without Sami approval."],
        next_best_actions=[
            "Capture 10 signals",
            "Score 5 opportunities",
            "Draft 3 Revenue Hunter offers",
            f"Convert {max(0, 3 - len(wins))} more outcomes to assets",
        ],
    )
