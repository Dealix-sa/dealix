"""
Verified revenue — the only kind that counts.

A RevenueEvent is "verified" if its `source` matches one of:

- payment_received
- signed_agreement
- retainer_active
- partner_paid_customer

Anything else is pipeline at best.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum


class RevenueStatus(StrEnum):
    INFLUENCED = "influenced"
    QUALIFIED_PIPELINE = "qualified_pipeline"
    PROPOSAL_SENT = "proposal_sent"
    COMMITTED = "committed"
    INVOICED = "invoiced"
    PAID = "paid"
    RETAINER_ACTIVE = "retainer_active"
    EXPANDED = "expanded"
    RENEWED = "renewed"


VERIFIED_REVENUE_SOURCES: frozenset[str] = frozenset(
    {
        "payment_received",
        "signed_agreement",
        "retainer_active",
        "partner_paid_customer",
    }
)


@dataclass
class RevenueEvent:
    event_id: str
    amount_sar: float
    source: str
    status: RevenueStatus
    customer_id: str
    occurred_at: float
    offer_id: str = ""
    partner_id: str = ""
    evidence_ref: str = ""

    @property
    def verified(self) -> bool:
        return is_verified(self)


def is_verified(event: RevenueEvent) -> bool:
    if event.amount_sar <= 0:
        return False
    if event.source not in VERIFIED_REVENUE_SOURCES:
        return False
    if event.status not in (
        RevenueStatus.PAID,
        RevenueStatus.RETAINER_ACTIVE,
        RevenueStatus.EXPANDED,
        RevenueStatus.RENEWED,
    ):
        return False
    if not event.evidence_ref:
        return False
    return True


def sum_verified_revenue(events: Iterable[RevenueEvent]) -> float:
    return round(sum(e.amount_sar for e in events if is_verified(e)), 2)
