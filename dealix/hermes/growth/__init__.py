"""
Growth layer.

Sub-modules:
- attribution:   multi-layer revenue attribution
- geo:           Generative Engine Optimization (AI search)
- entity_data:   canonical entity schemas for consistency across surfaces
- trust_signals: trust-signal coverage + scoring
"""

from __future__ import annotations

from dealix.hermes.growth.entity_consistency import (
    EntityConsistencyReport,
    check_entity_consistency,
)
from dealix.hermes.growth.public_methodology import (
    PublicMethodology,
    score_public_methodology,
)
from dealix.hermes.growth.review_engine import (
    ReviewProfile,
    review_visibility,
)
from dealix.hermes.growth.revenue_status import (
    RevenueLifecycle,
    advance_revenue_status,
)
from dealix.hermes.growth.trust_signals import (
    TrustSignal,
    TrustSignalReport,
    score_trust_signals,
)

__all__ = [
    "TrustSignal",
    "TrustSignalReport",
    "score_trust_signals",
    "ReviewProfile",
    "review_visibility",
    "EntityConsistencyReport",
    "check_entity_consistency",
    "PublicMethodology",
    "score_public_methodology",
    "RevenueLifecycle",
    "advance_revenue_status",
]
