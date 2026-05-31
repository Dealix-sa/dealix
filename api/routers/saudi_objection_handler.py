"""
Saudi B2B sales objection handler.

Provides categorized objections encountered in Saudi enterprise deals
with recommended responses, cultural context, and follow-up actions.
Covers price, timing, authority, trust, and technical objections
specific to the Saudi market.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/objection-handler", tags=["Sales"])

# ---------------------------------------------------------------------------
# Objection database
# ---------------------------------------------------------------------------

_OBJECTIONS: list[dict[str, Any]] = [
    # Price objections
    {
        "id": "price_too_expensive",
        "category": "price",
        "objection_en": "Your price is too high. We can build this ourselves.",
        "objection_ar": "سعركم مرتفع جداً. يمكننا بناء هذا بأنفسنا.",
        "frequency": "very_high",
        "response_strategy": "reframe_value",
        "recommended_response_en": (
            "I understand the instinct to build internally. "
            "Let's compare TCO: our solution deploys in 30 days vs. 12–18 months to build. "
            "At SAR {monthly_cost}/month, you'd need just {breakeven_months} months to pay back. "
            "What's your current cost for the process we're automating?"
        ),
        "recommended_response_ar": (
            "أفهم الرغبة في البناء الداخلي. "
            "لنقارن التكلفة الإجمالية: حلنا ينشر خلال 30 يوماً مقابل 12–18 شهراً للبناء الذاتي. "
            "بتكلفة {monthly_cost} ريال/شهر، تحتاج فقط {breakeven_months} شهراً للاسترداد. "
            "ما هي تكلفتكم الحالية للعملية التي نؤتمتها؟"
        ),
        "saudi_context_en": (
            "In Saudi B2B, 'too expensive' often means 'I haven't justified it to my CFO yet.' "
            "Offer to co-create the business case with them."
        ),
        "saudi_context_ar": (
            "في المبيعات B2B السعودية، 'مرتفع جداً' غالباً تعني 'لم أبرره لمديري المالي بعد'. "
            "عرض المشاركة في بناء مسوغ العمل معهم."
        ),
        "follow_up_action": "Send ROI calculator pre-filled with their sector benchmarks within 24h",
        "follow_up_action_ar": "أرسل حاسبة العائد على الاستثمار مُعبأة ببيانات قطاعهم خلال 24 ساعة",
        "red_flags": ["Budget is genuinely not there", "No executive sponsor"],
    },
    {
        "id": "price_compare_competitors",
        "category": "price",
        "objection_en": "Competitor X offers the same for less.",
        "objection_ar": "المنافس X يقدم نفس الشيء بسعر أقل.",
        "frequency": "high",
        "response_strategy": "differentiate_value",
        "recommended_response_en": (
            "Appreciate you comparing. Let's look at what's included: "
            "[List Saudi-specific features: ZATCA integration, bilingual AR/EN, prayer-time scheduling, PDPL compliance]. "
            "Does their solution handle Arabic-language AI natively and integrate with ZATCA Phase 2? "
            "Those aren't add-ons for us — they're built in."
        ),
        "recommended_response_ar": (
            "أقدّر مقارنتكم. لننظر إلى المحتوى: "
            "[سرد المزايا السعودية: تكامل زكاة، ثنائية العربية/الإنجليزية، جدولة أوقات الصلاة، امتثال PDPL]. "
            "هل يعالج حلهم الذكاء الاصطناعي بالعربية أصلاً ويتكامل مع مرحلة 2 من الفوترة الإلكترونية؟ "
            "هذه ليست إضافات لدينا — إنها مدمجة."
        ),
        "saudi_context_en": "Saudi enterprises heavily weight Saudi-specific compliance. Use ZATCA + PDPL as anchors.",
        "saudi_context_ar": "الشركات السعودية تُولي أهمية كبيرة للامتثال السعودي. استخدم ZATCA و PDPL كمراسي.",
        "follow_up_action": "Prepare feature comparison matrix with top 3 Saudi-market competitors",
        "follow_up_action_ar": "أعدّ مصفوفة مقارنة المزايا مع أفضل 3 منافسين في السوق السعودي",
        "red_flags": ["Prospect is using competitor to negotiate on price only"],
    },

    # Timing objections
    {
        "id": "timing_not_right_now",
        "category": "timing",
        "objection_en": "Now is not the right time. Let's revisit in Q3/Q4.",
        "objection_ar": "الوقت ليس مناسباً الآن. لنراجع في الربع الثالث/الرابع.",
        "frequency": "very_high",
        "response_strategy": "create_urgency",
        "recommended_response_en": (
            "I hear you. What's changing in Q3/Q4 that makes it a better fit? "
            "[Listen carefully.] "
            "One thing I'd flag: ZATCA Phase 2 penalties for non-compliance start accruing now. "
            "Our 30-day sprint can get you compliant before that window closes — "
            "would a scoped POC make sense to run in parallel while you plan Q3?"
        ),
        "recommended_response_ar": (
            "أفهم. ما الذي سيتغير في الربع الثالث/الرابع ليجعله أكثر ملاءمة؟ "
            "[استمع بعناية.] "
            "شيء أودّ الإشارة إليه: غرامات مرحلة 2 من الفوترة الإلكترونية تتراكم الآن. "
            "سبرينتنا لـ30 يوماً يمكنه تحقيق الامتثال قبل انتهاء تلك النافذة — "
            "هل من المنطقي تشغيل تجربة محدودة بالتوازي مع تخطيطكم للربع الثالث؟"
        ),
        "saudi_context_en": (
            "Saudi enterprise budget cycles typically set in H1 (Jan–Jun). "
            "If in Ramadan, this objection almost always means 'call me after Eid.'"
        ),
        "saudi_context_ar": (
            "دورات ميزانية الشركات السعودية تُحدد عادةً في النصف الأول (يناير–يونيو). "
            "إذا كان في رمضان، فهذا الاعتراض يعني دائماً تقريباً 'اتصل بعد العيد'."
        ),
        "follow_up_action": "Set calendar reminder for first day post-Eid or agreed Q3 date",
        "follow_up_action_ar": "اضبط تذكيراً في اليوم الأول بعد العيد أو تاريخ الربع الثالث المتفق عليه",
        "red_flags": ["No concrete Q3 event mentioned", "Budget freeze until next FY"],
    },
    {
        "id": "timing_busy_ramadan",
        "category": "timing",
        "objection_en": "We're in Ramadan — everyone is busy and decisions are slow.",
        "objection_ar": "نحن في رمضان — الجميع مشغول والقرارات بطيئة.",
        "frequency": "seasonal",
        "response_strategy": "align_and_plant",
        "recommended_response_en": (
            "Completely understand — Ramadan is a time for reflection and community. "
            "Let me use this time to prepare everything: proposal, ROI model, "
            "and a post-Eid implementation plan. "
            "Can we schedule 30 minutes in the first week after Eid?"
        ),
        "recommended_response_ar": (
            "أفهم تماماً — رمضان وقت للتأمل والمجتمع. "
            "دعني أستثمر هذا الوقت في تحضير كل شيء: المقترح، نموذج العائد على الاستثمار، "
            "وخطة تنفيذ ما بعد العيد. "
            "هل يمكننا جدولة 30 دقيقة في الأسبوع الأول بعد العيد؟"
        ),
        "saudi_context_en": "Never push for a decision during Ramadan. Plant seeds, confirm post-Eid.",
        "saudi_context_ar": "لا تضغط أبداً على قرار في رمضان. ازرع البذور، أكّد بعد العيد.",
        "follow_up_action": "Send a Ramadan-appropriate short note and book Eid follow-up immediately",
        "follow_up_action_ar": "أرسل رسالة قصيرة مناسبة لرمضان واحجز متابعة العيد فوراً",
        "red_flags": [],
    },

    # Authority objections
    {
        "id": "authority_not_decision_maker",
        "category": "authority",
        "objection_en": "I'm not the decision-maker. I'll need to check with my manager.",
        "objection_ar": "لست صاحب القرار. سأحتاج للرجوع إلى مديري.",
        "frequency": "very_high",
        "response_strategy": "multi_threading",
        "recommended_response_en": (
            "Of course — who should I include in the next conversation? "
            "It would help me tailor the presentation to what matters most to them. "
            "Is the CFO or CTO typically involved in decisions like this? "
            "I'm happy to prepare a one-page executive summary for them."
        ),
        "recommended_response_ar": (
            "بالطبع — من يجب أن أشرك في المحادثة التالية؟ "
            "سيساعدني ذلك في تصميم العرض وفق ما يهمهم أكثر. "
            "هل يشارك المدير المالي أو التقني عادةً في مثل هذه القرارات؟ "
            "يسعدني إعداد ملخص تنفيذي من صفحة واحدة لهم."
        ),
        "saudi_context_en": (
            "In Saudi companies, decisions above SAR 50K typically need VP+ approval. "
            "Multi-thread early: connect with both the champion and the economic buyer."
        ),
        "saudi_context_ar": (
            "في الشركات السعودية، القرارات فوق 50,000 ريال تحتاج عادةً لموافقة نائب رئيس أو أعلى. "
            "تعدد خيوط التواصل مبكراً: اربط بين البطل والمشتري الاقتصادي."
        ),
        "follow_up_action": "Request intro to economic buyer + send persona-specific brief",
        "follow_up_action_ar": "اطلب تعريفاً بالمشتري الاقتصادي + أرسل ملخصاً خاصاً بشخصيته",
        "red_flags": ["Champion has no internal influence", "Has been 'checking' for >3 weeks"],
    },

    # Trust objections
    {
        "id": "trust_new_vendor",
        "category": "trust",
        "objection_en": "You're a new company — we need proven vendors.",
        "objection_ar": "أنتم شركة جديدة — نحتاج موردين مُثبَتين.",
        "frequency": "high",
        "response_strategy": "social_proof",
        "recommended_response_en": (
            "Fair point. Here's what we can offer for confidence: "
            "1) Start with a bounded 7-day sprint — no long-term commitment. "
            "2) We'll provide a reference from [comparable Saudi company in same sector]. "
            "3) Escrow the deliverable: you only pay on acceptance. "
            "Would a no-risk pilot answer your concern?"
        ),
        "recommended_response_ar": (
            "وجهة نظر مقبولة. إليك ما يمكننا تقديمه لبناء الثقة: "
            "1) ابدأ بسبرينت محدود 7 أيام — بدون التزام طويل الأمد. "
            "2) سنقدم مرجعاً من [شركة سعودية مماثلة في نفس القطاع]. "
            "3) الحفظ الأمين للتسليمات: تدفع فقط عند القبول. "
            "هل يُجيب مشروع تجريبي بدون مخاطر على مخاوفك؟"
        ),
        "saudi_context_en": (
            "Saudi enterprises heavily weight wasta (relationships) and references. "
            "A reference from a respected Saudi company in their sector is 10× more powerful than marketing."
        ),
        "saudi_context_ar": (
            "الشركات السعودية تُولي أهمية كبيرة للعلاقات والمراجع. "
            "مرجع من شركة سعودية محترمة في قطاعهم أقوى 10 أضعاف من التسويق."
        ),
        "follow_up_action": "Identify and warm a Saudi reference client before next call",
        "follow_up_action_ar": "حدد عميلاً مرجعياً سعودياً وجهّزه قبل المكالمة التالية",
        "red_flags": ["No comparable reference available", "Procurement requires 3+ years track record"],
    },

    # Technical objections
    {
        "id": "tech_data_security",
        "category": "technical",
        "objection_en": "We have concerns about data security and where our data is stored.",
        "objection_ar": "لدينا مخاوف بشأن أمن البيانات ومكان تخزينها.",
        "frequency": "high",
        "response_strategy": "technical_assurance",
        "recommended_response_en": (
            "Data sovereignty is a priority for us too — especially in Saudi Arabia. "
            "Our data is hosted on AWS Riyadh Region (ap-me-south-1) within the Kingdom. "
            "We're PDPL-compliant with data minimization and deletion policies. "
            "I can share our security architecture document and NCA compliance summary today."
        ),
        "recommended_response_ar": (
            "سيادة البيانات أولوية لنا أيضاً — خاصةً في المملكة العربية السعودية. "
            "بياناتنا مستضافة على AWS منطقة الرياض (ap-me-south-1) داخل المملكة. "
            "نحن متوافقون مع نظام حماية البيانات الشخصية مع سياسات تقليل البيانات والحذف. "
            "يمكنني مشاركة وثيقة هندسة الأمن وملخص الامتثال للهيئة الوطنية للأمن السيبراني اليوم."
        ),
        "saudi_context_en": (
            "Saudi PDPL (Personal Data Protection Law) came into force September 2023. "
            "NCA (National Cybersecurity Authority) ECC controls are a hard requirement for government clients."
        ),
        "saudi_context_ar": (
            "نظام حماية البيانات الشخصية دخل حيز التنفيذ سبتمبر 2023. "
            "ضوابط الأمن السيبراني الأساسية للهيئة الوطنية للأمن السيبراني متطلب صارم للعملاء الحكوميين."
        ),
        "follow_up_action": "Send security one-pager and PDPL compliance checklist within 2h",
        "follow_up_action_ar": "أرسل صفحة أمن واحدة وقائمة امتثال PDPL خلال ساعتين",
        "red_flags": ["Client has classified data requiring government clearance"],
    },
]

_OBJECTIONS_BY_ID = {o["id"]: o for o in _OBJECTIONS}
_OBJECTIONS_BY_CATEGORY: dict[str, list[dict[str, Any]]] = {}
for obj in _OBJECTIONS:
    _OBJECTIONS_BY_CATEGORY.setdefault(obj["category"], []).append(obj)

_CATEGORIES = list(_OBJECTIONS_BY_CATEGORY.keys())

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/categories", summary="Objection categories in Saudi B2B sales")
async def list_categories() -> dict[str, Any]:
    return {
        "categories": [
            {
                "id": cat,
                "objection_count": len(_OBJECTIONS_BY_CATEGORY[cat]),
            }
            for cat in _CATEGORIES
        ],
        "total_objections": len(_OBJECTIONS),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/all", summary="All objections with responses")
async def list_all_objections(
    category: str | None = Query(None, description="Filter by category"),
) -> dict[str, Any]:
    if category:
        objs = _OBJECTIONS_BY_CATEGORY.get(category)
        if objs is None:
            raise HTTPException(
                status_code=404,
                detail=f"Category '{category}' not found. Valid: {_CATEGORIES}",
            )
        return {
            "category": category,
            "objections": objs,
            "governance_decision": "ALLOW_WITH_REVIEW",
        }
    return {
        "total": len(_OBJECTIONS),
        "objections": _OBJECTIONS,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/{objection_id}", summary="Get response for a specific objection")
async def get_objection(objection_id: str) -> dict[str, Any]:
    obj = _OBJECTIONS_BY_ID.get(objection_id)
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f"Objection '{objection_id}' not found.",
        )
    return {
        **obj,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
