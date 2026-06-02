"""Cold-email draft factory — deterministic, no external sends.

Produces up to 250 drafts/day in the canonical mix. Every body carries an
opt-out line and an accurate sender block so drafts can pass the compliance
gate; nothing is ever sent here — drafts are queued for the founder.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.market_production_os.models import OFFERS, SenderIdentity, new_id

# canonical daily mix (sums to 250)
DEFAULT_MIX: dict[str, int] = {
    "first_touch": 100,
    "follow_up_1": 75,
    "follow_up_2": 50,
    "proposal_intro": 15,
    "breakup": 10,
}

_DEFAULT_OFFER: dict[str, str] = {
    "first_touch": "revenue_diagnostic",
    "follow_up_1": "revenue_diagnostic",
    "follow_up_2": "lead_intelligence_sprint",
    "proposal_intro": "lead_intelligence_sprint",
    "breakup": "free_diagnostic",
}

_OPT_OUT = {
    "ar": "للإيقاف: ردّ بكلمة «إيقاف» وسنزيل بريدك فوراً.",
    "en": "To opt out, reply STOP and we will remove you immediately.",
}

_DEFAULT_PAIN = {
    "ar": "كثير من الشركات في قطاعكم تفقد فرصاً بسبب تشتّت المتابعة وضعف التقارير.",
    "en": "Many companies in your sector lose opportunities to scattered follow-up and weak reporting.",
}


def _offer_phrase(offer: str, language: str) -> tuple[str, str]:
    o = OFFERS.get(offer, {})
    name = o.get("name_ar" if language == "ar" else "name_en", offer)
    lo = int(o.get("price_sar_min", 0))
    hi = int(o.get("price_sar_max", 0))
    recurring = bool(o.get("recurring", False))
    if lo == 0 and hi == 0:
        price = "مجاناً" if language == "ar" else "free"
        return name, price
    unit = ("/شهر" if language == "ar" else "/mo") if recurring else ""
    if lo == hi:
        price = f"{lo:,} ريال{unit}" if language == "ar" else f"SAR {lo:,}{unit}"
    else:
        price = f"{lo:,}–{hi:,} ريال{unit}" if language == "ar" else f"SAR {lo:,}–{hi:,}{unit}"
    return name, price


def _sender_block(sender: dict[str, Any], language: str) -> str:
    lines = [sender.get("from_name", "Dealix"), sender.get("from_email", "")]
    addr = sender.get("physical_address", "")
    if addr:
        lines.append(addr)
    return "\n".join(x for x in lines if x)


def _render(
    prospect: dict[str, Any], touch_type: str, offer: str, language: str
) -> tuple[str, str, str]:
    company = prospect.get("company", "")
    note = prospect.get("personalization_note", "")
    pain = prospect.get("pain_hypothesis", "") or _DEFAULT_PAIN[language]
    offer_name, price = _offer_phrase(offer, language)

    if language == "ar":
        opener = "السلام عليكم،"
        intro = "نحن Dealix — نظام تشغيل الإيرادات للشركات السعودية."
        offer_line = f"نقترح نبدأ بـ {offer_name} ({price}): يوضّح أين تضيع الفرص وكيف ترتّبون المتابعة، بمسودات جاهزة وبموافقتكم قبل أي إرسال."
        subjects = {
            "first_touch": f"{company} — ملاحظة عن متابعة الفرص",
            "follow_up_1": f"{company} — متابعة سريعة",
            "follow_up_2": f"{company} — آخر ملاحظة من Dealix",
            "proposal_intro": f"{company} — مقترح مختصر: {offer_name}",
            "breakup": f"{company} — نغلق الملف (مع خيار مجاني)",
        }
        ctas = {
            "first_touch": "إذا يناسبكم، نبدأ بمكالمة ١٥ دقيقة هذا الأسبوع؟",
            "follow_up_1": "هل أرسل لكم مثالاً مختصراً على المخرجات؟",
            "follow_up_2": "إذا التوقيت غير مناسب الآن، أخبرونا متى نعاود.",
            "proposal_intro": "أرفق مقترحاً من صفحة واحدة عند موافقتكم.",
            "breakup": "نغلق الملف الآن، ويبقى عرض التشخيص المجاني متاحاً لكم.",
        }
    else:
        opener = "Hello,"
        intro = "We are Dealix — the Saudi B2B Revenue Operating System."
        offer_line = f"We suggest starting with {offer_name} ({price}): it shows where opportunities leak and how to organize follow-up, with ready drafts and your approval before anything is sent."
        subjects = {
            "first_touch": f"{company} — a note on opportunity follow-up",
            "follow_up_1": f"{company} — quick follow-up",
            "follow_up_2": f"{company} — last note from Dealix",
            "proposal_intro": f"{company} — short proposal: {offer_name}",
            "breakup": f"{company} — closing the loop (free option)",
        }
        ctas = {
            "first_touch": "If useful, could we do a 15-minute call this week?",
            "follow_up_1": "Want a short example of the deliverables?",
            "follow_up_2": "If the timing is off, tell us when to circle back.",
            "proposal_intro": "I will attach a one-page proposal once you are open to it.",
            "breakup": "We will close the file now; the free diagnostic stays open to you.",
        }

    subject = subjects.get(touch_type, subjects["first_touch"])
    cta = ctas.get(touch_type, ctas["first_touch"])
    parts = [opener, "", note or pain, "", intro, offer_line, "", cta]
    body = "\n".join(p for p in parts if p is not None)
    return subject, body, cta


def build_draft(
    prospect: dict[str, Any],
    *,
    touch_type: str = "first_touch",
    offer: str | None = None,
    sender_identity: SenderIdentity | dict[str, Any],
    language: str | None = None,
) -> dict[str, Any]:
    language = language or prospect.get("language", "ar")
    offer = offer or _DEFAULT_OFFER.get(touch_type, "revenue_diagnostic")
    subject, body, cta = _render(prospect, touch_type, offer, language)
    sender = (
        sender_identity.to_dict()
        if isinstance(sender_identity, SenderIdentity)
        else dict(sender_identity)
    )
    full_body = f"{body}\n\n{_sender_block(sender, language)}\n\n{_OPT_OUT[language]}"
    return {
        "schema_version": "1.0",
        "draft_id": new_id("dr"),
        "prospect_id": prospect.get("prospect_id", ""),
        "company": prospect.get("company", ""),
        "sector": prospect.get("sector", ""),
        "recipient_role": prospect.get("decision_maker_role", ""),
        "source": prospect.get("source", ""),
        "pain_hypothesis": prospect.get("pain_hypothesis", ""),
        "personalization_note": prospect.get("personalization_note", ""),
        "personalization_level": prospect.get("personalization_level", "P0"),
        "offer": offer,
        "touch_type": touch_type,
        "subject": subject,
        "body": full_body,
        "cta": cta,
        "language": language,
        "evidence_level": "L1",
        "risk_level": prospect.get("risk_level", "low"),
        "sender_identity": sender,
        "unsubscribe_included": True,
        "unsubscribe_method": "reply_keyword",
        "compliance_status": "pending",
        "compliance_failures": [],
        "approval_status": "pending",
        "send_status": "not_sent",
        "created_at": datetime.now(UTC).isoformat(),
    }


def produce_daily(
    prospects: list[dict[str, Any]],
    *,
    sender_identity: SenderIdentity | dict[str, Any],
    target: int = 250,
    mix: dict[str, int] | None = None,
    offer_by_sector: dict[str, str] | None = None,
    language: str | None = None,
) -> list[dict[str, Any]]:
    """Produce the daily mix of drafts by cycling through prospects."""
    mix = mix or DEFAULT_MIX
    offer_by_sector = offer_by_sector or {}
    drafts: list[dict[str, Any]] = []
    if not prospects:
        return drafts
    n = len(prospects)
    idx = 0
    for touch_type, count in mix.items():
        for _ in range(count):
            if len(drafts) >= target:
                return drafts
            prospect = prospects[idx % n]
            idx += 1
            offer = offer_by_sector.get(prospect.get("sector", ""), _DEFAULT_OFFER.get(touch_type))
            drafts.append(
                build_draft(
                    prospect,
                    touch_type=touch_type,
                    offer=offer,
                    sender_identity=sender_identity,
                    language=language,
                )
            )
    return drafts[:target]
