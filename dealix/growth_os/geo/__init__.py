"""Generative Engine Optimization (GEO) — content blueprint + page registry."""

from __future__ import annotations

from dealix.growth_os.geo.checker import (
    GEOComplianceReport,
    validate_geo_page,
)
from dealix.growth_os.geo.content_structure import (
    GEO_REQUIRED_SECTIONS,
    GEOContentSection,
    blueprint_for,
)
from dealix.growth_os.geo.pages_registry import GEO_PAGES, GEOPage, get_page

__all__ = [
    "GEO_PAGES",
    "GEO_REQUIRED_SECTIONS",
    "GEOComplianceReport",
    "GEOContentSection",
    "GEOPage",
    "blueprint_for",
    "get_page",
    "validate_geo_page",
]
