"""Daily cost alert gate helper — advisory until Slack/email wired (LAUNCH_GATES O4)."""
from __future__ import annotations

import os
from typing import Any


def evaluate_daily_cost_alert(*, daily_spend_usd: float | None = None) -> dict[str, Any]:
    threshold = float(os.environ.get("DEALIX_DAILY_COST_ALERT_USD", "10"))
    spend = daily_spend_usd
    if spend is None:
        return {
            "gate": "O4_daily_cost_alert",
            "status": "advisory",
            "message": "Wire /admin/costs + DEALIX_DAILY_COST_ALERT_USD to enable ping",
            "threshold_usd": threshold,
        }
    triggered = spend > threshold
    return {
        "gate": "O4_daily_cost_alert",
        "status": "triggered" if triggered else "ok",
        "daily_spend_usd": spend,
        "threshold_usd": threshold,
        "action": "notify_on_call" if triggered else None,
    }
