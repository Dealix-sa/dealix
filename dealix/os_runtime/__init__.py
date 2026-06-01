"""
Dealix OS Runtime
=================
Operational Python layer for Dealix Company OS.
Reads YAML/JSON configs from os/ and exposes scoring, routing, and gate logic.
"""

from dealix.os_runtime import (
    anti_ban_guardian,
    approval_gate,
    channel_router,
    company_scorer,
    config_loader,
    daily_brief,
    delivery_gate,
    finance,
    offer_router,
    persuasion_dossier,
)

__version__ = "1.0.0"
__all__ = [
    "config_loader",
    "company_scorer",
    "offer_router",
    "channel_router",
    "approval_gate",
    "anti_ban_guardian",
    "persuasion_dossier",
    "daily_brief",
    "finance",
    "delivery_gate",
]
