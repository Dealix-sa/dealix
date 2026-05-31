"""
Marketplace readiness — §106.

10-item checklist + 7 listing categories. Mirrors PublicAPIReadiness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


MARKETPLACE_LISTING_CATEGORIES: tuple[str, ...] = (
    "agents",
    "tools",
    "playbooks",
    "templates",
    "datasets",
    "evaluations",
    "integrations",
)


@dataclass
class MarketplaceReadiness:
    vendor_vetting: bool = False
    listing_review: bool = False
    revenue_share_terms: bool = False
    payout_pipeline: bool = False
    trust_check_per_listing: bool = False
    sovereign_kill_switch: bool = False
    customer_reviews: bool = False
    refund_policy: bool = False
    dispute_workflow: bool = False
    compliance_audit: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}

    def assess(self) -> tuple[bool, list[str]]:
        missing = [k for k, v in self.to_dict().items() if v is False]
        return (len(missing) == 0), missing
