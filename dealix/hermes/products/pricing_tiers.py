"""Tiered pricing on top of the sovereign PricingPolicy bands."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PricingTier:
    name: str
    monthly_sar: float
    includes: list[str]


@dataclass
class PricingTiers:
    tiers: dict[str, PricingTier] = field(default_factory=dict)

    def add(self, tier: PricingTier) -> None:
        if tier.monthly_sar <= 0:
            raise ValueError("Tier price must be > 0.")
        self.tiers[tier.name] = tier

    def get(self, name: str) -> PricingTier:
        return self.tiers[name]

    def names(self) -> list[str]:
        return sorted(self.tiers.keys())


__all__ = ["PricingTier", "PricingTiers"]
