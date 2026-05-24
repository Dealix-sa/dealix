"""
Proposal factory — turns an opportunity + rung into a bilingual draft.

Output is always a draft. Sending and pricing approval are sovereign.
"""

from __future__ import annotations

from pydantic import BaseModel

from dealix.hermes.core.schemas import HermesOpportunity
from dealix.hermes.money.pricing import PricingRung, recommend_rung


class ProposalDraft(BaseModel):
    title_en: str
    title_ar: str
    body_en: str
    body_ar: str
    rung: PricingRung
    quoted_amount_sar: float
    sovereign_approval_required: bool


def build_proposal(opportunity: HermesOpportunity) -> ProposalDraft:
    rung = recommend_rung(opportunity.estimated_value_sar)
    quoted = rung.min_sar
    approval_required = rung.sovereign_approval_required or quoted >= 5000

    title_en = f"{rung.name} — {opportunity.title}"
    title_ar = f"{rung.name} — {opportunity.title}"

    body_en = (
        f"Scope: {opportunity.description}\n"
        f"Rung: {rung.name}\n"
        f"Indicative price: {int(quoted)} SAR\n"
        "Outcome: a measurable improvement, recorded as a Dealix asset.\n"
        "Approval: this draft requires sovereign sign-off before sending."
    )
    body_ar = (
        f"النطاق: {opportunity.description}\n"
        f"الفئة: {rung.name}\n"
        f"السعر التأشيري: {int(quoted)} ريال\n"
        "المخرَج: تحسين قابل للقياس، يُسجَّل كأصل في Dealix.\n"
        "الموافقة: هذه المسودة تحتاج موافقة سامي قبل الإرسال."
    )
    return ProposalDraft(
        title_en=title_en,
        title_ar=title_ar,
        body_en=body_en,
        body_ar=body_ar,
        rung=rung,
        quoted_amount_sar=quoted,
        sovereign_approval_required=approval_required,
    )
