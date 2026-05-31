"""
Revenue Marketing OS — Dealix's Money Loop control plane.

التسويق الذي يربط كل إشارة سوق بعرض، كل عرض بحملة، كل حملة بصفقة،
كل صفقة بدخل موثق، وكل دخل بتعلم يحسن منابع المال.

Marketing here is NOT campaign-publishing. It is a revenue infrastructure:

    Market Signal → ICP → Pain → Offer → Message → Channel →
    Lead → Call → Proposal → Revenue → Outcome → Learning → Better Campaign

All external sends are draft-only. All revenue must be verified.
All attribution must be traced. All claims must pass the no-overclaim
register before publishing.
"""

from dealix.revenue_marketing_os.schemas import (
    AttributionRecord,
    CampaignRecord,
    LeadRecord,
    OfferRecord,
    RevenueRecord,
    TouchRecord,
)
from dealix.revenue_marketing_os.scoring import (
    compute_lead_score,
    compute_revenue_quality_score,
)
from dealix.revenue_marketing_os.store import get_revenue_marketing_store

__all__ = [
    "AttributionRecord",
    "CampaignRecord",
    "LeadRecord",
    "OfferRecord",
    "RevenueRecord",
    "TouchRecord",
    "compute_lead_score",
    "compute_revenue_quality_score",
    "get_revenue_marketing_store",
]
