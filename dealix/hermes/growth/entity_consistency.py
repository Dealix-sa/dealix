"""
Entity consistency — same name, description, offer, social, etc. across
every surface where the brand appears.

AI search rewards consistency; inconsistency dilutes brand visibility.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EntityConsistencyReport:
    consistent: bool
    discrepancies: list[str]
    canonical_fields: dict[str, str]


_REQUIRED_FIELDS = (
    "company_name",
    "company_description",
    "offer_starting_price_sar",
    "primary_url",
    "primary_industry",
    "primary_locale",
)


def check_entity_consistency(
    canonical: dict[str, str], surfaces: list[dict[str, str]]
) -> EntityConsistencyReport:
    missing_canonical = [f for f in _REQUIRED_FIELDS if not canonical.get(f)]
    discrepancies: list[str] = []
    if missing_canonical:
        discrepancies.append(f"canonical_missing:{missing_canonical}")

    for i, surface in enumerate(surfaces):
        surface_id = surface.get("surface_id", f"surface_{i}")
        for field in _REQUIRED_FIELDS:
            if field not in surface:
                continue
            cv = (canonical.get(field) or "").strip().casefold()
            sv = (surface.get(field) or "").strip().casefold()
            if cv != sv:
                discrepancies.append(f"{surface_id}.{field}: {sv!r} != canonical {cv!r}")
    return EntityConsistencyReport(
        consistent=not discrepancies,
        discrepancies=discrepancies,
        canonical_fields={k: canonical.get(k, "") for k in _REQUIRED_FIELDS},
    )
