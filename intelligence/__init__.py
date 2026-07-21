"""
Dealix Intelligence Layer — unified entry point.

Provides:
- IntelligenceRouter: route tasks to the right model
- SaudiMarketIntelligence: score Saudi B2B prospects and sectors
- RevenueIntelligenceEngine: analyze pipeline health and revenue risk
- EvidenceSynthesizer: build governed evidence packs for decisions
- PricingEngine: value-based pricing for Saudi B2B services
- ProposalGeneratorAgent: generate commercial proposals
- ContractRiskAnalyzer: analyze contract risk signals
- SaudiLeadMachine: enrich and score Saudi leads
- CustomerSuccessScorecard: customer health scoring
- CompetitorBattlecards: competitive positioning
- GTMCampaignOrchestrator: approval-first campaign planning
- ProductLedGrowthFlow: self-service diagnostic flow
- RevenueForecastingEngine: grounded revenue forecasts
- ExecutiveDashboardData: unified executive view
"""

from intelligence.competitor_battlecards import CompetitorBattlecards
from intelligence.contract_risk_analyzer import (
    ContractAnalysis,
    ContractRiskAnalyzer,
    RiskFinding,
    RiskLevel,
)
from intelligence.customer_success_scorecard import (
    CustomerHealthScore,
    CustomerSuccessScorecard,
    HealthTier,
)
from intelligence.evidence_synthesizer import (
    DecisionType,
    EvidenceItem,
    EvidencePack,
    EvidenceSynthesizer,
    EvidenceType,
)
from intelligence.executive_dashboard import ExecutiveDashboardData
from intelligence.gtm_campaign_orchestrator import (
    CampaignStatus,
    CampaignStep,
    GTMCampaign,
    GTMCampaignOrchestrator,
)
from intelligence.pricing_engine import PackageTier, PricingEngine, PricingRecommendation
from intelligence.product_led_growth import PLGRecommendation, ProductLedGrowthFlow
from intelligence.proposal_generator import GeneratedProposal, ProposalGeneratorAgent
from intelligence.revenue_forecasting import RevenueForecast, RevenueForecastingEngine
from intelligence.revenue_intelligence import (
    Deal,
    RevenueIntelligence,
    RevenueIntelligenceEngine,
    StageStats,
)
from intelligence.router import (
    IntelligenceRouter,
    RoutingDecision,
    TaskType,
    Urgency,
)
from intelligence.saudi_lead_machine import EnrichedLead, SaudiLeadMachine
from intelligence.saudi_market_intelligence import (
    ICPScore,
    SaudiCompanyProfile,
    SaudiMarketIntelligence,
    SectorSignal,
)

__all__ = [
    "CompetitorBattlecards",
    "ContractAnalysis",
    "ContractRiskAnalyzer",
    "RiskFinding",
    "RiskLevel",
    "CustomerHealthScore",
    "CustomerSuccessScorecard",
    "HealthTier",
    "DecisionType",
    "EvidenceItem",
    "EvidencePack",
    "EvidenceSynthesizer",
    "EvidenceType",
    "ExecutiveDashboardData",
    "CampaignStatus",
    "CampaignStep",
    "GTMCampaign",
    "GTMCampaignOrchestrator",
    "PackageTier",
    "PricingEngine",
    "PricingRecommendation",
    "PLGRecommendation",
    "ProductLedGrowthFlow",
    "GeneratedProposal",
    "ProposalGeneratorAgent",
    "RevenueForecast",
    "RevenueForecastingEngine",
    "Deal",
    "RevenueIntelligence",
    "RevenueIntelligenceEngine",
    "StageStats",
    "IntelligenceRouter",
    "RoutingDecision",
    "TaskType",
    "Urgency",
    "EnrichedLead",
    "SaudiLeadMachine",
    "ICPScore",
    "SaudiCompanyProfile",
    "SaudiMarketIntelligence",
    "SectorSignal",
]
