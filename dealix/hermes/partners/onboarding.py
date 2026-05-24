"""Partner Onboarding — produces the checklist a partner must complete."""

from __future__ import annotations

from typing import Any


class PartnerOnboarding:
    def checklist(self, partner_name: str) -> dict[str, Any]:
        return {
            "partner_name": partner_name,
            "steps": [
                "Sign mutual NDA (S4 approval)",
                "Sign revenue-share addendum (S4 approval)",
                "Map first 10 target customers",
                "Train on Offer Library",
                "Agree on monthly value review cadence",
            ],
            "blocking_until_approved": True,
        }
