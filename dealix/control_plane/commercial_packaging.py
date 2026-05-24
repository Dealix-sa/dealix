"""
Section 78 — Commercial Packaging.

Inside, Dealix is a massive Control Plane. *Outside*, the customer sees
three tiers — Entry, Expansion, Enterprise — each as a small catalogue of
named offers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class CommercialOfferTier(StrEnum):
    ENTRY = "entry"
    EXPANSION = "expansion"
    ENTERPRISE = "enterprise"


_ENTRY_OFFERS: tuple[str, ...] = (
    "Revenue Hunter Pilot",
    "AI Trust Kit",
    "Agency White-label Kit",
)

_EXPANSION_OFFERS: tuple[str, ...] = (
    "Founder OS",
    "Market Radar",
    "Executive PMO",
    "Partner OS",
    "Customer Health OS",
    "AI Governance OS",
)

_ENTERPRISE_OFFERS: tuple[str, ...] = (
    "Governed AI Workforce",
    "Agent Governance OS",
    "Executive Agentic PMO",
    "AI Control Plane",
)


@dataclass(frozen=True)
class _OfferLine:
    name: str
    tier: CommercialOfferTier


@dataclass
class CommercialPackaging:
    entry: list[_OfferLine] = field(
        default_factory=lambda: [
            _OfferLine(n, CommercialOfferTier.ENTRY) for n in _ENTRY_OFFERS
        ]
    )
    expansion: list[_OfferLine] = field(
        default_factory=lambda: [
            _OfferLine(n, CommercialOfferTier.EXPANSION) for n in _EXPANSION_OFFERS
        ]
    )
    enterprise: list[_OfferLine] = field(
        default_factory=lambda: [
            _OfferLine(n, CommercialOfferTier.ENTERPRISE) for n in _ENTERPRISE_OFFERS
        ]
    )

    def list_tier(self, tier: CommercialOfferTier) -> list[str]:
        bucket = {
            CommercialOfferTier.ENTRY: self.entry,
            CommercialOfferTier.EXPANSION: self.expansion,
            CommercialOfferTier.ENTERPRISE: self.enterprise,
        }[tier]
        return [line.name for line in bucket]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry": self.list_tier(CommercialOfferTier.ENTRY),
            "expansion": self.list_tier(CommercialOfferTier.EXPANSION),
            "enterprise": self.list_tier(CommercialOfferTier.ENTERPRISE),
        }
