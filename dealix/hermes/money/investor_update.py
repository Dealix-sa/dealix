"""Investor Update — drafts the periodic founder/investor brief."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.money.cashflow import CashflowBrief


class InvestorUpdate:
    def draft(self) -> dict[str, Any]:
        cash = CashflowBrief().summary()
        opps = get_opportunity_store().list()
        return {
            "as_of": datetime.now(timezone.utc).isoformat(),
            "headline": (
                f"SAR {cash.paid_sar:.0f} collected, SAR {cash.won_unpaid_sar:.0f} won-but-unpaid, "
                f"{len(opps)} opportunities open."
            ),
            "cash": cash.__dict__,
            "top_opportunities": [
                {"title": o.title, "score": o.score, "value_sar": o.estimated_value_sar}
                for o in opps[:5]
            ],
            "draft_only": True,
            "external_send": False,
        }
