#!/usr/bin/env python3
"""Verify the Distribution War Machine + growth docs are present."""

from __future__ import annotations

from _verify_common import Verifier


def populate(v: Verifier) -> None:
    v.check_files(
        [
            "docs/growth/DISTRIBUTION_WAR_MACHINE.md",
            "docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md",
            "docs/growth/OUTBOUND_DRAFT_MACHINE.md",
            "docs/growth/LINKEDIN_QUEUE_MACHINE.md",
            "docs/growth/EMAIL_DRAFT_MACHINE.md",
            "docs/growth/CONTACT_FORM_QUEUE_MACHINE.md",
            "docs/growth/FOLLOW_UP_MACHINE.md",
            "docs/growth/REPLY_ROUTER_MACHINE.md",
            "docs/growth/NURTURE_MACHINE.md",
            "docs/growth/PARTNER_REFERRAL_MACHINE.md",
            "docs/growth/ABM_STRATEGIC_ACCOUNT_MACHINE.md",
            "docs/growth/PROOF_TO_DEMAND_MACHINE.md",
            "docs/intelligence/SECTOR_RANKING_SYSTEM.md",
            "docs/intelligence/ICP_SEGMENTATION_SYSTEM.md",
            "docs/intelligence/BUYER_PERSONA_SYSTEM.md",
            "docs/intelligence/COMPETITIVE_INTELLIGENCE_SYSTEM.md",
            "docs/intelligence/TRIGGER_EVENT_SYSTEM.md",
            "docs/intelligence/ACCOUNT_SCORING_MODEL.md",
        ]
    )


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("growth-system", populate)
