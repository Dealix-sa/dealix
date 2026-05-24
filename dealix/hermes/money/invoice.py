"""Invoice Follow-up — chases unpaid invoices once an outcome flips to WON."""

from __future__ import annotations

from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.schemas import OutcomeStatus


class InvoiceFollowup:
    def outstanding(self) -> list[dict]:
        return [
            {
                "outcome_id": o.id,
                "amount_sar": o.revenue_sar,
                "draft": "Sharing the invoice for your reference. Let me know if any details need updating.",
                "external_send": False,
            }
            for o in get_outcome_store().list(status=OutcomeStatus.WON)
            if o.revenue_sar > 0
        ]
