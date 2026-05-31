"""
Marketplace readiness gate. Until every requirement is checked off
*and* S4 approval is granted, no asset / agent / package may be
published to the marketplace.
"""

from __future__ import annotations

from dataclasses import dataclass


MARKETPLACE_REQUIREMENTS: tuple[str, ...] = (
    "asset_quality_review",
    "trust_review",
    "publisher_verification",
    "payments",
    "refund_policy",
    "versioning",
    "ratings",
    "liability",
    "security_review",
    "s4_approval",
)


@dataclass
class MarketplaceReadiness:
    ready: bool
    missing: tuple[str, ...]
    notes: str


def evaluate_readiness(checks: dict[str, bool]) -> MarketplaceReadiness:
    missing = tuple(req for req in MARKETPLACE_REQUIREMENTS if not checks.get(req))
    notes = "All requirements satisfied." if not missing else f"Missing: {', '.join(missing)}"
    return MarketplaceReadiness(ready=not missing, missing=missing, notes=notes)
