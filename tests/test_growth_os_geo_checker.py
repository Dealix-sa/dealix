"""GEO content compliance tests."""

from __future__ import annotations

from dealix.growth_os.geo.checker import validate_geo_page
from dealix.growth_os.geo.content_structure import (
    GEO_REQUIRED_SECTIONS,
    blueprint_for,
)
from dealix.growth_os.geo.pages_registry import GEO_PAGES


def _complete_sections() -> dict[str, str]:
    out: dict[str, str] = {}
    for key in GEO_REQUIRED_SECTIONS:
        bp = blueprint_for(key)
        out[key] = "x" * (bp.min_chars + 10)
    return out


def test_pages_registry_has_required_paths() -> None:
    required = {
        "/ai-governance-saudi-companies",
        "/agentic-control-plane",
        "/ai-revenue-hunter",
        "/agency-ai-white-label",
        "/ai-agents-permissions-approvals",
        "/mcp-risk-review",
    }
    assert required == set(GEO_PAGES.keys())


def test_complete_page_passes() -> None:
    report = validate_geo_page(
        {"path": "/ai-revenue-hunter", "sections": _complete_sections()}
    )
    assert report.is_compliant is True
    assert report.missing_sections == []
    assert report.short_sections == []
    assert report.score == 1.0


def test_missing_sections_fails() -> None:
    secs = _complete_sections()
    del secs["faq"]
    del secs["sources"]
    report = validate_geo_page({"path": "/x", "sections": secs})
    assert report.is_compliant is False
    assert "faq" in report.missing_sections
    assert "sources" in report.missing_sections
    assert report.score < 1.0


def test_short_sections_fails_even_when_present() -> None:
    secs = _complete_sections()
    secs["definition"] = "short"  # under min_chars
    report = validate_geo_page({"path": "/x", "sections": secs})
    assert report.is_compliant is False
    assert "definition" in report.short_sections
