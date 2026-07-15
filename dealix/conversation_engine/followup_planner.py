"""Follow-up planner — schedules the next low-pressure touch per target.

Cadence is conservative and permission-based. No auto-send — these are planned
drafts for the founder to approve.
"""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine.channel_adapter import EMAIL, WHATSAPP


def build_followups(target: dict[str, Any], channels_drafts: dict[str, Any]) -> list[dict[str, Any]]:
    company = target.get("company", "")
    band = target.get("band", "cold")

    # Hotter leads get a slightly tighter (but still gentle) cadence.
    timing = {
        "hot": ["day+2", "day+5"],
        "warm": ["day+3", "day+7"],
        "cold": ["day+5", "day+10"],
    }.get(band, ["day+3", "day+7"])

    email = channels_drafts.get(EMAIL, {})
    whatsapp = channels_drafts.get(WHATSAPP, {})

    return [
        {
            "target": company,
            "channel": EMAIL,
            "timing": timing[0],
            "message": email.get("followup_1", ""),
            "approval_required": True,
        },
        {
            "target": company,
            "channel": WHATSAPP,
            "timing": timing[1],
            "message": whatsapp.get("followup", ""),
            "approval_required": True,
            "note": "warm_only_no_cold",
        },
    ]
