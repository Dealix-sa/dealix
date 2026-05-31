"""Sovereignty module — protects Sami's decision authority."""

from dealix.hermes.sovereignty.approvals import ApprovalCenter, ApprovalRequest, ApprovalState
from dealix.hermes.sovereignty.classifier import classify_action, ActionContext
from dealix.hermes.sovereignty.kill_switch import KillSwitch, KillTarget
from dealix.hermes.sovereignty.levels import (
    SovereigntyLevel,
    is_autonomous,
    requires_human,
    requires_memo,
)

__all__ = [
    "ActionContext",
    "ApprovalCenter",
    "ApprovalRequest",
    "ApprovalState",
    "KillSwitch",
    "KillTarget",
    "SovereigntyLevel",
    "classify_action",
    "is_autonomous",
    "requires_human",
    "requires_memo",
]
