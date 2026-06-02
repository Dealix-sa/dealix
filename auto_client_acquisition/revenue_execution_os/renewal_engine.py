"""Renewal engine — climbs the offer ladder after value is delivered.

Renewals are event-driven: after first delivery, after a value report, before
month end, after a quick win, or once a proof pack exists. The engine prepares
a renewal record pointing at the next rung; it never contacts anyone.
"""

from __future__ import annotations

from uuid import uuid4

from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.models import Renewal, now_iso
from auto_client_acquisition.revenue_execution_os.offers import (
    ENTERPRISE_RUNG,
    OFFER_LADDER,
    next_offer,
)

RENEWAL_TRIGGERS: tuple[str, ...] = (
    "after_first_delivery",
    "after_value_report",
    "before_month_end",
    "after_quick_win",
    "after_proof_pack",
)


def renewal_ladder() -> tuple[str, ...]:
    """Offer keys in ascending order (main ladder only, excludes enterprise)."""
    rungs = sorted((o for o in OFFER_LADDER if o.rung < ENTERPRISE_RUNG), key=lambda o: o.rung)
    return tuple(o.key for o in rungs)


def build_renewal(customer_id: str, current_offer_key: str, *, trigger: str = "") -> Renewal:
    """Build a renewal record pointing at the next rung (pure)."""
    nxt = next_offer(current_offer_key)
    return Renewal(
        renewal_id=f"ren_{uuid4().hex[:18]}",
        customer_id=customer_id,
        current_offer_key=current_offer_key,
        next_offer_key=nxt.key if nxt else "",
        trigger=trigger,
        due_date=now_iso(),
        status="open",
        created_at=now_iso(),
    )


def generate_renewal(customer_id: str, current_offer_key: str, *, trigger: str = "") -> Renewal:
    """Build + persist a renewal record."""
    return stores.RENEWALS.add(build_renewal(customer_id, current_offer_key, trigger=trigger))


__all__ = [
    "RENEWAL_TRIGGERS",
    "build_renewal",
    "generate_renewal",
    "renewal_ladder",
]
