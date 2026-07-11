"""Dealix multi-department Commercial Universe public surface."""

from .approval_adapter import to_approval_request
from .contracts import (
    ActionEnvelope,
    ActionMode,
    ApprovalOption,
    Channel,
    CommercialObjective,
    Department,
    LifecycleStage,
    MeetingPlan,
    ObjectiveType,
    OfferType,
    PermissionStatus,
    RelationshipContext,
    RelationshipType,
    RiskLevel,
    StrategicOffer,
    StrategicRecommendation,
    ValueExchange,
)
from .strategy import build_action_envelope, build_meeting_plan, recommend_strategy

__all__ = [
    "ActionEnvelope",
    "ActionMode",
    "ApprovalOption",
    "Channel",
    "CommercialObjective",
    "Department",
    "LifecycleStage",
    "MeetingPlan",
    "ObjectiveType",
    "OfferType",
    "PermissionStatus",
    "RelationshipContext",
    "RelationshipType",
    "RiskLevel",
    "StrategicOffer",
    "StrategicRecommendation",
    "ValueExchange",
    "build_action_envelope",
    "build_meeting_plan",
    "recommend_strategy",
    "to_approval_request",
]
