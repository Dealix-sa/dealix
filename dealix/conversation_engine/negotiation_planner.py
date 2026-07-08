"""Negotiation planner — builds a per-target negotiation plan.

Concession rules never drop price first: reduce scope, start with a pilot, ask
for proof permission, tie payment to a clear deliverable. Never promises an
uncertain result.
"""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine import company_brain
from dealix.conversation_engine.objection_handler import relevant_objections

CONCESSION_RULES = [
    "لا تخفض السعر مباشرة.",
    "قلل النطاق بدل السعر.",
    "ابدأ بـ pilot صغير.",
    "اطلب إذن proof بدل خصم.",
    "اربط الدفع بمخرج واضح.",
    "لا تعد بنتيجة غير مضمونة.",
    "لا تقبل نطاقًا مفتوحًا بدون سعر.",
]


def build_plan(target: dict[str, Any], match: dict[str, Any]) -> dict[str, Any]:
    offer = match.get("primary_offer", {})
    company = target.get("company", "")

    objections = relevant_objections(target, offer)
    likely = [ob["trigger_ar"] for ob in objections]
    strategy = [
        {
            "objection": ob["trigger_ar"],
            "response": ob["short_ar"],
            "next_move": ob["negotiation_move"],
        }
        for ob in objections
    ]

    return {
        "target": company,
        "offer": offer.get("name_en") or offer.get("id") or "",
        "offer_id": offer.get("id", ""),
        "starting_position": (
            f"نبدأ بـ«{offer.get('name_ar', '')}» بسعر {offer.get('price_display', '')} "
            f"مع نطاق واضح ومقاييس محددة."
        ),
        "minimum_commitment": "pilot صغير (7 أيام) بأصغر نطاق يثبت القيمة.",
        "value_proof": offer.get("value_angle_ar", ""),
        "likely_objections": likely,
        "response_strategy": strategy,
        "concession_rules": CONCESSION_RULES,
        "close_question": "هل يناسب نبدأ بـ pilot صغير مقيس هذا الأسبوع؟",
        "next_best_action": "إرسال ملخص صفحة واحدة للاعتماد (draft-only).",
        "approval_required": True,
    }
