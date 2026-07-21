"""
Dealix Intelligence Layer — unified entry point.

Provides:
- IntelligenceRouter: route tasks to the right model
- SaudiMarketIntelligence: score Saudi B2B prospects and sectors
- RevenueIntelligenceEngine: analyze pipeline health and revenue risk
- EvidenceSynthesizer: build governed evidence packs for decisions
"""

from intelligence.router import (
    IntelligenceRouter,
    RoutingDecision,
    TaskType,
    Urgency,
)
from intelligence.saudi_market_intelligence import (
    SaudiCompanyProfile,
    SaudiMarketIntelligence,
    ICPScore,
)
from intelligence.revenue_intelligence import (
    Deal,
    RevenueIntelligence,
    RevenueIntelligenceEngine,
    StageStats,
)
from intelligence.evidence_synthesizer import (
    EvidenceItem,
    EvidencePack,
    EvidenceSynthesizer,
    EvidenceType,
    DecisionType,
)

__all__ = [
    "IntelligenceRouter",
    "RoutingDecision",
    "TaskType",
    "Urgency",
    "SaudiCompanyProfile",
    "SaudiMarketIntelligence",
    "ICPScore",
    "Deal",
    "RevenueIntelligence",
    "RevenueIntelligenceEngine",
    "StageStats",
    "EvidenceItem",
    "EvidencePack",
    "EvidenceSynthesizer",
    "EvidenceType",
    "DecisionType",
]
