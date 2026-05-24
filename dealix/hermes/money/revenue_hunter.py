"""
Revenue Hunter — turns a customer signal into a draft, never sends.

Designed to be the fastest path from "signal arrived" to "draft ready
for Sami to send personally". No outbound automation. No CRM writes.
"""

from __future__ import annotations

from pydantic import BaseModel

from dealix.hermes.core.schemas import HermesOpportunity
from dealix.hermes.money.pricing import PricingRung, recommend_rung


class HuntDraft(BaseModel):
    target: str
    headline: str
    body: str
    recommended_rung: PricingRung
    send_via: str  # "sami_manual_whatsapp" | "sami_manual_email" | "sami_manual_linkedin"
    sovereign_approval_required: bool = True


def draft_hunt(opportunity: HermesOpportunity, channel: str = "sami_manual_whatsapp") -> HuntDraft:
    rung = recommend_rung(opportunity.estimated_value_sar)
    headline = f"Quick idea for {opportunity.target_entity or 'your team'}"
    body = (
        f"بناءً على ما لاحظته في سوقكم: {opportunity.description}\n\n"
        f"عندي اقتراح صغير على شكل {rung.name} يبدأ من {int(rung.min_sar)} ريال.\n"
        "إذا يهمكم، أرسل لكم التفاصيل خلال 24 ساعة."
    )
    return HuntDraft(
        target=opportunity.target_entity or "unknown",
        headline=headline,
        body=body,
        recommended_rung=rung,
        send_via=channel,
        sovereign_approval_required=True,
    )
