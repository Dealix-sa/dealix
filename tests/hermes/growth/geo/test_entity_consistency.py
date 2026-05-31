"""Entity consistency check flags mismatched listings."""

from __future__ import annotations

from dealix.hermes.growth.geo.entity_consistency import EntityListing, check


def test_consistency_flags_mismatch() -> None:
    canonical = EntityListing("internal", "Dealix", "dealix.ai", "AI sales OS", "saas")
    listings = [
        EntityListing("crunchbase", "Dealix", "dealix.ai", "AI sales OS", "saas"),
        EntityListing("dir_b", "Dealix Inc", "dealix.io", "AI", "tech"),
    ]
    report = check(canonical, listings)
    assert report.consistent is False
    assert any(s == "dir_b" for s, _ in report.mismatches)
