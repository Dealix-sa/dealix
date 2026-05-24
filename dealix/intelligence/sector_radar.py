"""خادم الذكاء — SectorRadar.

Static `SECTOR_PROFILES` table + a `snapshot(sector_name)` helper. The
profiles cover Clinics, Real Estate, Retail, B2B SaaS and Manufacturing
at a minimum — these are the verticals Dealix prioritises in §35.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SectorSnapshot(BaseModel):
    """A static-but-structured snapshot of a sector."""

    model_config = ConfigDict(extra="forbid")

    sector: str = Field(..., min_length=1, max_length=64)
    buyer: str = Field(..., min_length=1, max_length=120)
    common_pain: str = Field(..., min_length=1, max_length=400)
    seasonal_flags: list[str] = Field(default_factory=list, max_length=8)
    growth_outlook: str = Field(..., min_length=1, max_length=120)
    notable_regulators: list[str] = Field(default_factory=list, max_length=8)


SECTOR_PROFILES: dict[str, SectorSnapshot] = {
    "clinics": SectorSnapshot(
        sector="clinics",
        buyer="Clinic owner / operations manager",
        common_pain="No-show losses, manual follow-up, fragmented patient records",
        seasonal_flags=["Ramadan slowdown", "Back-to-school spike"],
        growth_outlook="steady",
        notable_regulators=["MOH", "PDPL"],
    ),
    "real_estate": SectorSnapshot(
        sector="real_estate",
        buyer="Real-estate broker / agency owner",
        common_pain="Long sales cycles, low qualified-lead conversion",
        seasonal_flags=["Q4 closing rush", "Summer slowdown"],
        growth_outlook="cyclical",
        notable_regulators=["REGA", "ZATCA"],
    ),
    "retail": SectorSnapshot(
        sector="retail",
        buyer="Retail multi-store operator",
        common_pain="Stock visibility gaps, weak customer-data foundation",
        seasonal_flags=["Ramadan spike", "Back-to-school", "Hajj surge"],
        growth_outlook="expansion",
        notable_regulators=["ZATCA", "SFDA"],
    ),
    "b2b_saas": SectorSnapshot(
        sector="b2b_saas",
        buyer="Head of Revenue / Head of CS",
        common_pain="Renewal churn, soft upsell motions, missing trust artefacts",
        seasonal_flags=["End-of-FY budget freeze"],
        growth_outlook="strong",
        notable_regulators=["PDPL", "SDAIA"],
    ),
    "manufacturing": SectorSnapshot(
        sector="manufacturing",
        buyer="Plant manager / supply chain lead",
        common_pain="Late deliveries, manual quality reporting, no proactive risk",
        seasonal_flags=["Public-holiday production gaps"],
        growth_outlook="industrial-policy tailwind",
        notable_regulators=["MODON", "SASO"],
    ),
}


class SectorRadar:
    """Lookup helper for the static sector knowledge base."""

    def snapshot(self, sector_name: str) -> SectorSnapshot:
        key = sector_name.lower().strip().replace("-", "_").replace(" ", "_")
        try:
            return SECTOR_PROFILES[key]
        except KeyError as exc:
            raise KeyError(
                f"unknown sector: {sector_name!r} (known: {sorted(SECTOR_PROFILES)})"
            ) from exc

    def known_sectors(self) -> list[str]:
        return sorted(SECTOR_PROFILES.keys())


__all__ = ["SECTOR_PROFILES", "SectorRadar", "SectorSnapshot"]
