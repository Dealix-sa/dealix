"""Partner Pitch — drafts the white-label / channel pitch (no external send)."""

from __future__ import annotations

from typing import Any

from dealix.hermes.partners.fit_score import PartnerFit


class PartnerPitch:
    def draft(self, fit: PartnerFit, *, commercial_model: str = "setup + monthly + 25% revenue share") -> dict[str, Any]:
        return {
            "title": f"Partnership proposal — {fit.partner_name}",
            "partner_type": fit.partner_type,
            "fit_score": fit.fit_score,
            "next_action": fit.next_action,
            "produces": fit.produces,
            "commercial_model": commercial_model,
            "asks": [
                "30-day pilot with one shared customer",
                "Joint pricing on a single SKU",
                "Co-branded value report at the end of the pilot",
            ],
            "draft_only": True,
            "external_send": False,
        }
