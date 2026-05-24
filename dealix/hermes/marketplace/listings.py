"""Marketplace listings.

Listing → quality_review → trust_review → priced → published. Publication
is S4 — only Sami can flip the switch.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class ListingKind(str, Enum):
    AGENT_TEMPLATE = "agent_template"
    WORKFLOW = "workflow"
    POLICY_PACK = "policy_pack"
    TRAINING_KIT = "training_kit"
    SECTOR_KIT = "sector_kit"
    MCP_CONNECTOR = "mcp_connector"
    PARTNER_SERVICE = "partner_service"
    REPORT = "report"


class ListingStatus(str, Enum):
    DRAFT = "draft"
    QUALITY_REVIEWED = "quality_reviewed"
    TRUST_REVIEWED = "trust_reviewed"
    PRICED = "priced"
    PUBLISHED = "published"
    RETIRED = "retired"


@dataclass
class Listing:
    id: str
    title: str
    kind: ListingKind
    price_sar: float | None = None
    status: ListingStatus = ListingStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Marketplace:
    _by_id: dict[str, Listing] = field(default_factory=dict)
    sovereign_publisher: str = "sami"

    def draft(self, *, title: str, kind: ListingKind) -> Listing:
        listing = Listing(
            id=f"lst_{uuid.uuid4().hex[:10]}",
            title=title,
            kind=kind,
        )
        self._by_id[listing.id] = listing
        return listing

    def quality_review(self, listing_id: str) -> Listing:
        l = self._by_id[listing_id]
        l.status = ListingStatus.QUALITY_REVIEWED
        return l

    def trust_review(self, listing_id: str) -> Listing:
        l = self._by_id[listing_id]
        if l.status != ListingStatus.QUALITY_REVIEWED:
            raise ValueError("Trust review requires quality_reviewed.")
        l.status = ListingStatus.TRUST_REVIEWED
        return l

    def set_price(self, listing_id: str, *, price_sar: float) -> Listing:
        l = self._by_id[listing_id]
        if price_sar <= 0:
            raise ValueError("Price must be > 0.")
        if l.status != ListingStatus.TRUST_REVIEWED:
            raise ValueError("Pricing requires trust_reviewed.")
        l.price_sar = float(price_sar)
        l.status = ListingStatus.PRICED
        return l

    def publish(self, listing_id: str, *, by: str = "sami") -> Listing:
        if by != self.sovereign_publisher:
            raise PermissionError("Marketplace publication is S4 — sovereign only.")
        l = self._by_id[listing_id]
        if l.status != ListingStatus.PRICED:
            raise ValueError("Publication requires priced status.")
        l.status = ListingStatus.PUBLISHED
        return l

    def all(self) -> list[Listing]:
        return list(self._by_id.values())


__all__ = ["Listing", "ListingKind", "ListingStatus", "Marketplace"]
