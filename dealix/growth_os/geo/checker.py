"""GEO page compliance checker — validates a structured page payload."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.geo.content_structure import (
    GEO_REQUIRED_SECTIONS,
    blueprint_for,
)


class GEOComplianceReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    is_compliant: bool
    missing_sections: list[str] = Field(default_factory=list)
    short_sections: list[str] = Field(default_factory=list)
    score: float = Field(..., ge=0.0, le=1.0)
    notes_ar: str = ""
    notes_en: str = ""


def validate_geo_page(structure: dict[str, Any]) -> GEOComplianceReport:
    """Validate a page dict shaped as ``{"path": str, "sections": {key: str}}``.

    Returns a report listing missing or under-length sections.
    """
    path = str(structure.get("path", ""))
    sections = structure.get("sections", {}) or {}

    missing: list[str] = []
    short: list[str] = []
    present_count = 0

    for key in GEO_REQUIRED_SECTIONS:
        body = sections.get(key)
        if not body or not isinstance(body, str) or not body.strip():
            missing.append(key)
            continue
        present_count += 1
        bp = blueprint_for(key)
        if len(body.strip()) < bp.min_chars:
            short.append(key)

    total = len(GEO_REQUIRED_SECTIONS)
    score = present_count / total if total else 0.0
    is_compliant = not missing and not short

    notes_ar = "صفحة GEO جاهزة" if is_compliant else "نواقص في الأقسام أو الأطوال"
    notes_en = (
        "GEO page is ready" if is_compliant else "Missing or under-length sections"
    )

    return GEOComplianceReport(
        path=path,
        is_compliant=is_compliant,
        missing_sections=missing,
        short_sections=short,
        score=round(score, 4),
        notes_ar=notes_ar,
        notes_en=notes_en,
    )


__all__ = ["GEOComplianceReport", "validate_geo_page"]
