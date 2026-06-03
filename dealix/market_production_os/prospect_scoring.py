"""Weighted prospect scoring + qualification.

Weights (max 100): sector_fit 20 · expected_leads 20 · decision_maker_clear 15
· pain_clear 15 · payment_capacity 15 · personalization 10 · low_risk 5.
"""

from __future__ import annotations

from dealix.market_production_os.models import ProspectScore
from dealix.market_production_os.personalization import level_rank

_PAYMENT = {"high": 15, "medium": 10, "low": 5, "unknown": 0}
_RISK = {"low": 5, "medium": 2, "high": 0}
# personalization points by level rank (P0..P4)
_PERSONALIZATION = (0, 4, 6, 8, 10)

DEFAULT_THRESHOLD = 60


def score_prospect(prospect: dict) -> ProspectScore:
    sector = prospect.get("sector", "other")
    sector_fit = 20 if sector and sector != "other" else 8
    expected = 20 if prospect.get("has_expected_leads") else 0
    dm = 15 if prospect.get("decision_maker_clear") else 0
    pain = 15 if prospect.get("pain_clear") else 0
    pay = _PAYMENT.get(prospect.get("payment_capacity", "unknown"), 0)
    rank = min(level_rank(prospect.get("personalization_level", "P0")), 4)
    pers = _PERSONALIZATION[rank]
    risk = _RISK.get(prospect.get("risk_level", "medium"), 2)
    return ProspectScore(
        sector_fit=sector_fit,
        expected_leads=expected,
        decision_maker_clear=dm,
        pain_clear=pain,
        payment_capacity=pay,
        personalization=pers,
        low_risk=risk,
    )


def qualify(prospect: dict, *, threshold: int = DEFAULT_THRESHOLD) -> bool:
    if prospect.get("status") == "do_not_contact":
        return False
    return score_prospect(prospect).total >= threshold


def recommended_status(prospect: dict, *, threshold: int = DEFAULT_THRESHOLD) -> str:
    if prospect.get("status") == "do_not_contact":
        return "do_not_contact"
    return "qualified" if qualify(prospect, threshold=threshold) else "nurture"
