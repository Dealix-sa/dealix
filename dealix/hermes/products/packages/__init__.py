"""
Productized offer packages.

This module is intentionally lightweight: each package is described as a
data dictionary so the offers can be edited without changing code.
"""

from __future__ import annotations

PACKAGES: dict[str, dict[str, object]] = {
    "revenue_hunter_pilot": {
        "name": "Revenue Hunter Pilot",
        "tier": "entry",
        "starting_price_sar": 1500,
        "duration_weeks": 2,
        "outcomes": ["qualified-pipeline list", "first message bank", "intent map"],
    },
    "ai_trust_kit": {
        "name": "AI Trust Kit",
        "tier": "core",
        "starting_price_sar": 9500,
        "duration_weeks": 3,
        "outcomes": [
            "AI permission matrix",
            "AI risk register",
            "approval flow doc",
            "policy + mini-training session",
        ],
    },
    "agency_white_label_kit": {
        "name": "Agency White-label Kit",
        "tier": "core",
        "starting_price_sar": 14000,
        "duration_weeks": 4,
        "outcomes": [
            "partner enablement pack",
            "approved claims library",
            "delivery playbook adaptation",
        ],
    },
    "agentic_control_plane": {
        "name": "Agentic Control Plane (Enterprise)",
        "tier": "enterprise",
        "starting_price_sar": 65000,
        "duration_weeks": 6,
        "outcomes": [
            "agent + tool registry deployment",
            "permission matrix",
            "approval center integration",
            "evidence packs",
            "governance dashboard",
        ],
    },
}
