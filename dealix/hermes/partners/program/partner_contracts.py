"""PartnerProfile — a registered partner with tier, contract, and status."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from dealix.hermes.partners.program.partner_tiers import PartnerTier


@dataclass
class PartnerProfile:
    partner_id: str
    legal_name: str
    tier: PartnerTier
    contact_email: str
    contract_signed_at: datetime | None = None
    status: str = "pending"  # "pending" | "active" | "suspended" | "terminated"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


PARTNER_REGISTRY: dict[str, PartnerProfile] = {}


def register_partner(profile: PartnerProfile) -> PartnerProfile:
    PARTNER_REGISTRY[profile.partner_id] = profile
    return profile
