"""Monthly Value Report — what was delivered, what came of it, what's next."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class ValueReportBuilder:
    def build(
        self,
        *,
        customer_id: str,
        opportunities_count: int,
        messages_drafted: int,
        proposals_count: int,
        outcomes_count: int,
        value_summary: str,
        next_plan: str,
        recommendation: str,
        upsell: str,
    ) -> dict[str, Any]:
        return {
            "customer_id": customer_id,
            "as_of": datetime.now(timezone.utc).isoformat(),
            "what_we_delivered": {
                "opportunities": opportunities_count,
                "messages_drafted": messages_drafted,
                "proposals": proposals_count,
                "outcomes": outcomes_count,
            },
            "what_value": value_summary,
            "next_plan": next_plan,
            "recommendation": recommendation,
            "suggested_upsell": upsell,
            "draft_only": True,
            "external_send": False,
        }
