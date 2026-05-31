"""
Hermes Growth — Section 50.

Rules enforced in code (not docs):
    - لا Campaign بلا Offer (Campaign.offer_id required).
    - لا Lead بلا Source (Lead.source required).
    - لا Experiment بلا Decision Rule (Experiment.decision_rule required).
    - لا Channel بلا Attribution (channels emit AttributionLink).
"""

from .campaign_registry import Campaign, CampaignRegistry, CampaignStatus
from .icp_registry import ICP, ICPRegistry
from .funnel_analytics import FunnelAnalytics, FunnelStage, FunnelSnapshot
from .growth_experiments import Experiment, ExperimentResult, GrowthExperimentBook

__all__ = [
    "Campaign",
    "CampaignRegistry",
    "CampaignStatus",
    "Experiment",
    "ExperimentResult",
    "FunnelAnalytics",
    "FunnelSnapshot",
    "FunnelStage",
    "GrowthExperimentBook",
    "ICP",
    "ICPRegistry",
]
