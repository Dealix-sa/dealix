"""
Customer Value Report — the artifact that justifies the retainer.

It must cover: activities, outputs, outcomes, revenue influenced, risks
reduced, assets created, recommended next actions, and upsell.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class ValueReport:
    report_id: str
    customer_id: str
    period_start: datetime
    period_end: datetime
    activities: tuple[str, ...]
    outputs: tuple[str, ...]
    outcomes: tuple[str, ...]
    revenue_influenced_sar: float
    risks_reduced: tuple[str, ...]
    assets_created: tuple[str, ...]
    recommended_next_actions: tuple[str, ...]
    upsell_opportunity: str
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "customer_id": self.customer_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "activities": list(self.activities),
            "outputs": list(self.outputs),
            "outcomes": list(self.outcomes),
            "revenue_influenced_sar": self.revenue_influenced_sar,
            "risks_reduced": list(self.risks_reduced),
            "assets_created": list(self.assets_created),
            "recommended_next_actions": list(self.recommended_next_actions),
            "upsell_opportunity": self.upsell_opportunity,
            "generated_at": self.generated_at.isoformat(),
        }


class ValueReportGenerator:
    def generate(
        self,
        *,
        report_id: str,
        customer_id: str,
        period_start: datetime,
        period_end: datetime,
        activities: tuple[str, ...],
        outputs: tuple[str, ...],
        outcomes: tuple[str, ...],
        revenue_influenced_sar: float,
        risks_reduced: tuple[str, ...] = (),
        assets_created: tuple[str, ...] = (),
        recommended_next_actions: tuple[str, ...] = (),
        upsell_opportunity: str = "",
    ) -> ValueReport:
        if not outcomes:
            raise ValueError("Customer value report requires at least one Outcome.")
        return ValueReport(
            report_id=report_id,
            customer_id=customer_id,
            period_start=period_start,
            period_end=period_end,
            activities=activities,
            outputs=outputs,
            outcomes=outcomes,
            revenue_influenced_sar=revenue_influenced_sar,
            risks_reduced=risks_reduced,
            assets_created=assets_created,
            recommended_next_actions=recommended_next_actions,
            upsell_opportunity=upsell_opportunity,
        )
