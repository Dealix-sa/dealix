"""
Offer readiness gate — before an offer is allowed to ship publicly, it
must clear delivery, legal, security, and trust-signal checks.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OfferReadinessGate:
    offer_id: str
    ready: bool
    failing_checks: list[str]
    notes: list[str]


_REQUIRED_CHECKS = (
    "delivery_playbook_present",
    "pricing_documented",
    "approval_flow_documented",
    "data_handling_documented",
    "claim_verifier_pass",
    "trust_signals_min_3",
    "owner_assigned",
)


def check_offer_readiness(
    offer_id: str, checks: dict[str, bool], *, notes: list[str] | None = None
) -> OfferReadinessGate:
    failing = [c for c in _REQUIRED_CHECKS if not checks.get(c, False)]
    return OfferReadinessGate(
        offer_id=offer_id,
        ready=not failing,
        failing_checks=failing,
        notes=list(notes or []),
    )
