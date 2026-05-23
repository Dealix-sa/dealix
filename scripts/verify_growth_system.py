#!/usr/bin/env python3
"""Verify Dealix growth system docs and intelligence assets are present."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/intelligence/MARKET_DOMINATION_INTELLIGENCE.md",
    "docs/intelligence/SECTOR_RANKING_SYSTEM.md",
    "docs/intelligence/ICP_SEGMENTATION_SYSTEM.md",
    "docs/intelligence/BUYER_PERSONA_SYSTEM.md",
    "docs/intelligence/COMPETITIVE_INTELLIGENCE_SYSTEM.md",
    "docs/intelligence/TRIGGER_EVENT_SYSTEM.md",
    "docs/intelligence/ACCOUNT_SCORING_MODEL.md",
    "docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md",
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
    "docs/growth/CONTENT_TO_DEMAND_ENGINE.md",
    "docs/growth/CHANNEL_PORTFOLIO_SYSTEM.md",
]


def main() -> int:
    missing = [f for f in REQUIRED if not (REPO / f).exists()]
    print("[growth-system]")
    print(f"  missing files: {len(missing)}")
    for m in missing:
        print(f"    - {m}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
