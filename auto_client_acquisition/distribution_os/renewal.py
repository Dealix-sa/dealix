"""Renewal & Upsell — reuses the existing renewal scheduler + ladder upsell.

The renewal schedule itself is owned by
``auto_client_acquisition.payment_ops.renewal_scheduler`` (do not duplicate it).
This module adds the upsell-ladder view (plan section 12) and the "when does a
renewal appear" triggers, on top of that scheduler.
"""

from __future__ import annotations

from auto_client_acquisition.distribution_os import catalog

# Re-export the canonical scheduler surface so callers have one import.
from auto_client_acquisition.payment_ops.renewal_scheduler import (
    RenewalSchedule,
    RenewalStatus,
    list_by_customer,
    list_due,
    mark_confirmed,
    mark_failed,
    mark_skipped,
    schedule_renewal,
)

# When a renewal / upsell conversation should surface (plan section 12).
RENEWAL_TRIGGERS: tuple[str, ...] = (
    "after_first_workflow_delivered",
    "after_first_weekly_value_report",
    "after_proof_pack_l3_plus",
    "before_month_end",
    "after_positive_customer_reply",
)


def upsell_ladder(current_product_id: str) -> list[dict[str, object]]:
    """The remaining rungs above the customer's current product (the upsell path)."""
    out: list[dict[str, object]] = []
    cursor = current_product_id
    while True:
        nxt = catalog.next_rung(cursor)
        if nxt is None:
            break
        out.append(
            {
                "id": nxt.id,
                "name_ar": nxt.name_ar,
                "name_en": nxt.name_en,
                "price_min_sar": nxt.price_sar,
                "price_max_sar": nxt.price_max_sar or nxt.price_sar,
            }
        )
        cursor = nxt.id
    return out


def next_upsell(current_product_id: str) -> dict[str, object] | None:
    ladder = upsell_ladder(current_product_id)
    return ladder[0] if ladder else None


__all__ = [
    "RENEWAL_TRIGGERS",
    "RenewalSchedule",
    "RenewalStatus",
    "list_by_customer",
    "list_due",
    "mark_confirmed",
    "mark_failed",
    "mark_skipped",
    "next_upsell",
    "schedule_renewal",
    "upsell_ladder",
]
