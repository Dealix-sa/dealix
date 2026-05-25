"""Partner tiers: referral, white_label, implementation, strategic."""

from __future__ import annotations

from dataclasses import dataclass

VALID_TIERS = ("referral", "white_label", "implementation", "strategic")


@dataclass(frozen=True)
class Partner:
    partner_id: str
    name: str
    tier: str
    region: str = ""


_PARTNERS: dict[str, Partner] = {}


def register(partner_id: str, name: str, tier: str, region: str = "") -> Partner:
    """Register a partner; raises ValueError when tier is unknown."""
    if tier not in VALID_TIERS:
        raise ValueError(f"unknown tier: {tier}; expected one of {VALID_TIERS}")
    p = Partner(partner_id=partner_id, name=name, tier=tier, region=region)
    _PARTNERS[partner_id] = p
    return p


def get(partner_id: str) -> Partner | None:
    """Return Partner by id or None."""
    return _PARTNERS.get(partner_id)


def list_all(tier: str | None = None) -> list[Partner]:
    """Return all partners, optionally filtered by tier."""
    if tier is None:
        return list(_PARTNERS.values())
    return [p for p in _PARTNERS.values() if p.tier == tier]


def reset() -> None:
    """Clear the partner registry (test helper)."""
    _PARTNERS.clear()
