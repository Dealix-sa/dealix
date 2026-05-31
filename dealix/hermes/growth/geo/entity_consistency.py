"""
GEO entity check — wraps the general entity_consistency check with the
specific surfaces that GEO cares about (homepage, FAQ, product pages,
schema.org JSON-LD blob, social profiles).
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.growth.entity_consistency import (
    EntityConsistencyReport,
    check_entity_consistency,
)


@dataclass
class GEOEntityCheck:
    report: EntityConsistencyReport
    geo_surfaces_checked: list[str]


_GEO_SURFACES = (
    "homepage",
    "product_page",
    "faq_page",
    "schema_org_jsonld",
    "social_linkedin",
    "social_x",
)


def check_geo_entity_alignment(
    canonical: dict[str, str], surfaces: list[dict[str, str]]
) -> GEOEntityCheck:
    surface_ids = [s.get("surface_id", "") for s in surfaces]
    missing = [name for name in _GEO_SURFACES if name not in surface_ids]
    report = check_entity_consistency(canonical, surfaces)
    if missing:
        report.discrepancies.append(f"missing_geo_surfaces:{missing}")
        report.consistent = False
    return GEOEntityCheck(report=report, geo_surfaces_checked=surface_ids)
