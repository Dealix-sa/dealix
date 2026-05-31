"""
VerifiedRevenueLoop — the canonical pipeline that turns a campaign touch
into *verified* revenue.

Pipeline::

    Campaign -> Touch -> Lead -> Call -> Proposal
              -> Commitment -> Invoice -> Payment -> Verified Revenue
              -> Attribution -> Learning

A deal is verified iff at least one of the policy's required events has
been recorded AND none of the excluded markers are the *only* evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class RevenueEventKind(StrEnum):
    CAMPAIGN = "campaign"
    TOUCH = "touch"
    LEAD = "lead"
    CALL = "call"
    PROPOSAL = "proposal"
    COMMITMENT = "commitment"
    INVOICE = "invoice"
    PAYMENT_RECEIVED = "payment_received"
    SIGNED_AGREEMENT = "signed_agreement"
    RETAINER_ACTIVATED = "retainer_activated"
    PARTNER_PAID_CUSTOMER = "partner_paid_customer"


REVENUE_VERIFICATION_POLICY: dict[str, Any] = {
    "policy_id": "revenue_verification_policy_v1",
    "verified_revenue_requires": [
        RevenueEventKind.PAYMENT_RECEIVED.value,
        RevenueEventKind.SIGNED_AGREEMENT.value,
        RevenueEventKind.RETAINER_ACTIVATED.value,
        RevenueEventKind.PARTNER_PAID_CUSTOMER.value,
    ],
    "excluded_from_verified_revenue": [
        "likes",
        "views",
        "meetings_booked",
        "verbal_interest",
        "unqualified_pipeline",
    ],
    "minimum_required": 1,
}


@dataclass
class RevenueEvent:
    deal_id: str
    kind: RevenueEventKind
    amount_sar: float = 0.0
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DealVerificationResult:
    deal_id: str
    verified: bool
    verified_amount_sar: float
    matched_required: tuple[str, ...]
    reason: str


class VerifiedRevenueLoop:
    def __init__(self) -> None:
        self._events: list[RevenueEvent] = []

    def record(self, event: RevenueEvent) -> None:
        self._events.append(event)

    def events_for(self, deal_id: str) -> list[RevenueEvent]:
        return [e for e in self._events if e.deal_id == deal_id]

    def verify(self, deal_id: str) -> DealVerificationResult:
        evts = self.events_for(deal_id)
        required = set(REVENUE_VERIFICATION_POLICY["verified_revenue_requires"])
        matched = {e.kind.value for e in evts} & required
        if not matched:
            return DealVerificationResult(
                deal_id=deal_id,
                verified=False,
                verified_amount_sar=0.0,
                matched_required=tuple(),
                reason="No verifying event recorded.",
            )
        amount = sum(e.amount_sar for e in evts if e.kind.value in matched)
        return DealVerificationResult(
            deal_id=deal_id,
            verified=True,
            verified_amount_sar=amount,
            matched_required=tuple(sorted(matched)),
            reason="Verifying events present.",
        )
