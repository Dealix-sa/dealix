"""Dealix Revenue Marketing Engine.

Turns market signals into measurable revenue loops:
Signal → Segment → Pain → Offer → Message → Channel → Lead → Deal →
Revenue → Outcome → Learning → Asset → Scale / Kill.

Draft-first and approval-gated. No outbound send happens here.
"""

from dealix.revenue_marketing.attribution import (
    attribute_revenue,
    influenced_assets,
    money_quality_score,
)
from dealix.revenue_marketing.experiments import (
    decide_experiment,
    experiment_card,
)
from dealix.revenue_marketing.funnel import (
    bottleneck_diagnosis,
    funnel_conversion_rates,
)
from dealix.revenue_marketing.lead_scoring import (
    revenue_marketing_lead_score,
)
from dealix.revenue_marketing.loop import (
    run_marketing_loop,
)
from dealix.revenue_marketing.offer_ladder import (
    ladder_offer_by_id,
    offer_ladder_catalog,
)
from dealix.revenue_marketing.portfolio import (
    portfolio_dashboard,
    stream_money_quality,
)
from dealix.revenue_marketing.quality_gates import (
    campaign_quality_gate,
    content_quality_gate,
)
from dealix.revenue_marketing.store import (
    get_revenue_marketing_store,
    reset_revenue_marketing_store_for_tests,
)

__all__ = [
    "attribute_revenue",
    "bottleneck_diagnosis",
    "campaign_quality_gate",
    "content_quality_gate",
    "decide_experiment",
    "experiment_card",
    "funnel_conversion_rates",
    "get_revenue_marketing_store",
    "influenced_assets",
    "ladder_offer_by_id",
    "money_quality_score",
    "offer_ladder_catalog",
    "portfolio_dashboard",
    "reset_revenue_marketing_store_for_tests",
    "revenue_marketing_lead_score",
    "run_marketing_loop",
    "stream_money_quality",
]
