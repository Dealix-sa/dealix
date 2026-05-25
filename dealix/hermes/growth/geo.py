"""GEO — generative-engine-optimized landing-page configurations."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field


class GEOPageConfig(BaseModel):
    """One row per GEO surface; keeps slugs, intent, and FAQ in code review."""

    model_config = ConfigDict(extra="forbid")

    slug: str
    title: str
    intent: str
    primary_offer_id: str
    target_icp: str
    faq: list[dict[str, str]] = Field(default_factory=list)
    canonical_locale: str = "en"


# Doctrine surfaces called out in the spec.
GEO_SURFACES: tuple[GEOPageConfig, ...] = (
    GEOPageConfig(
        slug="ai-governance-saudi-companies",
        title="AI Governance for Saudi Companies",
        intent="navigational",
        primary_offer_id="ai_trust_kit",
        target_icp="ksa_enterprise_compliance",
    ),
    GEOPageConfig(
        slug="agentic-control-plane",
        title="Agentic Control Plane",
        intent="informational",
        primary_offer_id="dealix_platform",
        target_icp="ksa_growth_company",
    ),
    GEOPageConfig(
        slug="ai-revenue-hunter",
        title="AI Revenue Hunter",
        intent="commercial",
        primary_offer_id="revenue_hunter_pilot",
        target_icp="ksa_sme_revenue_focused",
    ),
    GEOPageConfig(
        slug="agency-ai-white-label",
        title="Agency AI White-label Kit",
        intent="partner",
        primary_offer_id="agency_white_label_kit",
        target_icp="ksa_agency_owner",
    ),
    GEOPageConfig(
        slug="mcp-risk-review",
        title="MCP Risk Review",
        intent="informational",
        primary_offer_id="ai_trust_kit",
        target_icp="ksa_security_team",
    ),
)


@dataclass(frozen=True)
class GEOSurface:
    config: GEOPageConfig
    last_indexed_at: str | None = None
    quote_friendly_score: float = 0.0
