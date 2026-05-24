"""Renewal Advisor — recommends the renewal motion based on health."""

from __future__ import annotations

from dealix.hermes.customer.health_score import CustomerHealth


class RenewalAdvisor:
    def recommend(self, health: CustomerHealth) -> dict:
        if health.renewal_risk == "low":
            return {
                "motion": "auto_renew_with_upsell",
                "draft_email": (
                    "Quick renewal note: another month of value delivered. "
                    "Happy to add the upsell discussion to next week's review."
                ),
                "external_send": False,
            }
        if health.renewal_risk == "medium":
            return {
                "motion": "renewal_check_in",
                "draft_email": "Let's review value before renewal — propose a 30-minute call.",
                "external_send": False,
            }
        return {
            "motion": "escalate_to_sami",
            "note": "Renewal at risk; surface to Sami before any renewal motion.",
        }
