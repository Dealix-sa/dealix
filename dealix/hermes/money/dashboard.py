"""Money Dashboard — single pane of glass for cash, pipeline, and next action."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.schemas import OpportunityType, OutcomeStatus
from dealix.hermes.core.scoring import score_money


@dataclass
class MoneyDashboardSnapshot:
    fastest_cash_action: dict[str, Any] | None
    highest_value_deal: dict[str, Any] | None
    open_proposals: int
    follow_ups_due: int
    pending_payments_sar: float
    upsell_candidates: int
    partner_revenue_sar: float
    expected_revenue_sar: float
    cash_risk: str
    best_next_action: str

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class MoneyDashboard:
    def snapshot(self) -> MoneyDashboardSnapshot:
        opps = get_opportunity_store().list()
        outs = get_outcome_store().list()

        money_opps = [
            o
            for o in opps
            if o.opportunity_type
            in {OpportunityType.CUSTOMER.value, OpportunityType.PARTNER.value}
        ]

        # Fastest cash = highest money score
        ranked = sorted(
            money_opps,
            key=lambda o: score_money(
                cash_speed=o.cash_speed_score,
                close_probability=0.4,
                deal_value_sar=o.estimated_value_sar,
                strategic=o.strategic_score,
                risk=o.risk_score,
            ),
            reverse=True,
        )
        fastest = ranked[0].model_dump(mode="json") if ranked else None
        highest = (
            sorted(money_opps, key=lambda o: o.estimated_value_sar, reverse=True)[0].model_dump(mode="json")
            if money_opps
            else None
        )

        pending_payments = sum(
            o.revenue_sar for o in outs if o.status == OutcomeStatus.WON.value
        )
        partner_revenue = sum(
            o.revenue_sar for o in outs if o.status == OutcomeStatus.PAID.value
        )
        expected_revenue = sum(o.estimated_value_sar for o in money_opps)
        cash_risk = "high" if not ranked else ("medium" if expected_revenue < 25_000 else "low")
        best = (
            f"Move on '{ranked[0].title}' (score {ranked[0].score})"
            if ranked
            else "Ingest more customer signals"
        )

        return MoneyDashboardSnapshot(
            fastest_cash_action=fastest,
            highest_value_deal=highest,
            open_proposals=sum(1 for o in opps if o.status == "open"),
            follow_ups_due=sum(
                1 for o in outs if o.status in {OutcomeStatus.SENT.value, OutcomeStatus.REPLIED.value}
            ),
            pending_payments_sar=pending_payments,
            upsell_candidates=sum(1 for o in outs if o.status == OutcomeStatus.PAID.value),
            partner_revenue_sar=partner_revenue,
            expected_revenue_sar=expected_revenue,
            cash_risk=cash_risk,
            best_next_action=best,
        )
