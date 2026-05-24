"""Cash Scout — finds the fastest path to revenue across all opportunities."""

from __future__ import annotations

from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.core.schemas import Opportunity
from dealix.hermes.core.scoring import score_money


class CashScout:
    def fastest_paths(self, *, top: int = 5) -> list[dict]:
        opps = get_opportunity_store().list(status="open")
        ranked: list[tuple[Opportunity, float]] = sorted(
            (
                (
                    o,
                    score_money(
                        cash_speed=o.cash_speed_score,
                        close_probability=0.5,
                        deal_value_sar=o.estimated_value_sar,
                        strategic=o.strategic_score,
                        risk=o.risk_score,
                    ),
                )
                for o in opps
            ),
            key=lambda pair: pair[1],
            reverse=True,
        )
        return [
            {
                "opportunity_id": o.id,
                "title": o.title,
                "money_score": s,
                "estimated_value_sar": o.estimated_value_sar,
                "next_step": o.recommended_action,
            }
            for o, s in ranked[:top]
        ]
