"""Check that brand entity attributes are consistent across listings."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EntityListing:
    source: str
    name: str
    domain: str
    description: str
    industry: str


@dataclass(frozen=True)
class ConsistencyReport:
    consistent: bool
    mismatches: tuple[tuple[str, str], ...] = field(default_factory=tuple)


def check(canonical: EntityListing, listings: list[EntityListing]) -> ConsistencyReport:
    """Return ConsistencyReport flagging any listings whose fields diverge from canonical."""
    mismatches: list[tuple[str, str]] = []
    for listing in listings:
        for field_name in ("name", "domain", "description", "industry"):
            canonical_value = getattr(canonical, field_name)
            value = getattr(listing, field_name)
            if value != canonical_value:
                mismatches.append((listing.source, field_name))
    return ConsistencyReport(consistent=not mismatches, mismatches=tuple(mismatches))
