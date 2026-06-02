"""Payment handoff — prepares (never sends) a payment-link handoff.

A payment link is an external commitment. This module never sends one; it
assembles a handoff and records which preconditions are met. The doctrine:
no payment link without proposal approved + price/scope/terms confirmed +
founder approval. Moyasar live mode stays founder-flipped only.
"""

from __future__ import annotations

from uuid import uuid4

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.models import (
    PaymentHandoff,
    PaymentHandoffStatus,
    Proposal,
    ProposalStatus,
    now_iso,
)
from auto_client_acquisition.revenue_execution_os.offers import offer_by_key, price_label

PRECONDITION_KEYS: tuple[str, ...] = (
    "proposal_approved",
    "price_confirmed",
    "scope_confirmed",
    "terms_confirmed",
    "founder_approved",
)


def build_payment_handoff(
    proposal: Proposal,
    *,
    price_confirmed: bool = False,
    scope_confirmed: bool = False,
    terms_confirmed: bool = False,
    founder_approved: bool = False,
) -> PaymentHandoff:
    """Assemble a payment handoff for an approved proposal (pure, no send)."""
    preconditions = {
        "proposal_approved": proposal.status == ProposalStatus.APPROVED,
        "price_confirmed": bool(price_confirmed),
        "scope_confirmed": bool(scope_confirmed),
        "terms_confirmed": bool(terms_confirmed),
        "founder_approved": bool(founder_approved),
    }
    blocking = [k for k in PRECONDITION_KEYS if not preconditions[k]]
    status = PaymentHandoffStatus.APPROVED if not blocking else PaymentHandoffStatus.DRAFT
    amount_label = ""
    try:
        amount_label = price_label(offer_by_key(proposal.offer_key), "ar")
    except KeyError:
        amount_label = proposal.price_label
    return PaymentHandoff(
        handoff_id=f"pay_{uuid4().hex[:18]}",
        prospect_id=proposal.prospect_id,
        proposal_id=proposal.proposal_id,
        offer_key=proposal.offer_key,
        amount_label=amount_label,
        status=status,
        preconditions=preconditions,
        blocking_reasons=blocking,
        # Sending a payment link is always a human action.
        governance_decision=str(GovernanceDecision.REQUIRE_APPROVAL),
        created_at=now_iso(),
    )


def handoff_is_ready(handoff: PaymentHandoff) -> bool:
    """True only when every precondition for sending the link is met."""
    return not handoff.blocking_reasons


def generate_payment_handoff(
    proposal: Proposal,
    *,
    price_confirmed: bool = False,
    scope_confirmed: bool = False,
    terms_confirmed: bool = False,
    founder_approved: bool = False,
) -> PaymentHandoff:
    """Build + persist a payment handoff."""
    handoff = build_payment_handoff(
        proposal,
        price_confirmed=price_confirmed,
        scope_confirmed=scope_confirmed,
        terms_confirmed=terms_confirmed,
        founder_approved=founder_approved,
    )
    return stores.PAYMENT_HANDOFFS.add(handoff)


__all__ = [
    "PRECONDITION_KEYS",
    "build_payment_handoff",
    "generate_payment_handoff",
    "handoff_is_ready",
]
