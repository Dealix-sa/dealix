"""Dealix Revenue Marketing Engine.

Turns marketing into a measurable revenue system:
Signal -> Segment -> Offer -> Campaign -> Lead -> Deal -> Revenue -> Outcome -> Learning.

All agent outputs are draft-first; no external send/publish from this module.
Revenue is counted only when a deal has payment_received or signed_agreement.
"""

from __future__ import annotations

from dealix.revenue_marketing.agents import (
    MARKETING_AGENTS,
    AttributionAgent,
    AudienceResearchAgent,
    CampaignPlannerAgent,
    CaseStudyAgent,
    ContentStrategistAgent,
    ConversionOptimizerAgent,
    CopywriterAgent,
    ICPBuilderAgent,
    LandingPageAgent,
    LeadScoringAgent,
    MarketRadarAgent,
    OfferPositioningAgent,
    propose_via_agent,
)
from dealix.revenue_marketing.attribution import (
    attribution_chain_for_deal,
    record_attribution,
    revenue_by_dimension,
)
from dealix.revenue_marketing.dashboard import dashboard_snapshot
from dealix.revenue_marketing.experiments import (
    create_experiment,
    decide,
    record_result,
)
from dealix.revenue_marketing.marketing_graph import (
    best_message_variants_by_reply_rate,
    build_graph,
    pains_by_call_rate,
    partners_by_revenue,
    top_channels_by_qualified_leads,
    top_offers_by_close_rate,
)
from dealix.revenue_marketing.quality_gates import (
    enforce_no_vanity,
    validate_campaign,
    validate_content,
)
from dealix.revenue_marketing.revenue_portfolio import (
    Stream,
    current_streams,
    portfolio_health,
)
from dealix.revenue_marketing.schemas import (
    Audience,
    CaseStudyDraft,
    Lead,
    MarketingCampaign,
    MarketingExperiment,
    MarketingTouch,
    MarketSignal,
    MessageVariant,
    Offer,
    RevenueAttribution,
    compute_lead_score,
)
from dealix.revenue_marketing.scoring import (
    classify_outcome,
    compute_money_quality_score,
)
from dealix.revenue_marketing.store import (
    RevenueMarketingStore,
    get_revenue_marketing_store,
    reset_revenue_marketing_store_for_tests,
    uid,
)

__all__ = [
    "MARKETING_AGENTS",
    "AttributionAgent",
    "Audience",
    "AudienceResearchAgent",
    "CampaignPlannerAgent",
    "CaseStudyAgent",
    "CaseStudyDraft",
    "ContentStrategistAgent",
    "ConversionOptimizerAgent",
    "CopywriterAgent",
    "ICPBuilderAgent",
    "LandingPageAgent",
    "Lead",
    "LeadScoringAgent",
    "MarketRadarAgent",
    "MarketSignal",
    "MarketingCampaign",
    "MarketingExperiment",
    "MarketingTouch",
    "MessageVariant",
    "Offer",
    "OfferPositioningAgent",
    "RevenueAttribution",
    "RevenueMarketingStore",
    "Stream",
    "attribution_chain_for_deal",
    "best_message_variants_by_reply_rate",
    "build_graph",
    "classify_outcome",
    "compute_lead_score",
    "compute_money_quality_score",
    "create_experiment",
    "current_streams",
    "dashboard_snapshot",
    "decide",
    "enforce_no_vanity",
    "get_revenue_marketing_store",
    "pains_by_call_rate",
    "partners_by_revenue",
    "portfolio_health",
    "propose_via_agent",
    "record_attribution",
    "record_result",
    "reset_revenue_marketing_store_for_tests",
    "revenue_by_dimension",
    "top_channels_by_qualified_leads",
    "top_offers_by_close_rate",
    "uid",
    "validate_campaign",
    "validate_content",
]
