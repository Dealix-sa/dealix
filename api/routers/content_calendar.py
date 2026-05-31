"""
Saudi B2B content calendar with Hijri awareness.

Provides a structured annual content calendar for B2B marketing in Saudi Arabia,
incorporating national holidays, Ramadan, Vision 2030 milestones, LEAP conference,
and quarter-end budget cycles. Helps Dealix and clients plan campaigns.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/content-calendar", tags=["Sales"])

# ---------------------------------------------------------------------------
# Fixed Gregorian events with marketing context
# ---------------------------------------------------------------------------

_ANNUAL_EVENTS: list[dict[str, Any]] = [
    {
        "event": "Saudi Founding Day",
        "event_ar": "يوم التأسيس",
        "gregorian_month": 2,
        "gregorian_day": 22,
        "type": "national_holiday",
        "campaign_window_days_before": 7,
        "campaign_window_days_after": 3,
        "b2b_opportunity_en": (
            "Post Vision 2030 alignment content. "
            "Theme: building Saudi legacy through AI innovation."
        ),
        "b2b_opportunity_ar": (
            "انشر محتوى توافق رؤية 2030. "
            "المحور: بناء الإرث السعودي من خلال الابتكار في الذكاء الاصطناعي."
        ),
        "content_ideas": [
            "LinkedIn post: How AI supports Saudi legacy businesses",
            "Email: '3 ways Dealix helps you achieve your Vision 2030 KPIs'",
            "Case study: [Saudi client] + Founding Day theme",
        ],
        "avoid_en": "Avoid promotional tone on the day itself — respect is key.",
        "avoid_ar": "تجنب الأسلوب الترويجي في اليوم نفسه — الاحترام هو المفتاح.",
    },
    {
        "event": "LEAP Conference (Riyadh)",
        "event_ar": "مؤتمر ليب (الرياض)",
        "gregorian_month": 2,
        "gregorian_day": 9,
        "type": "industry_event",
        "campaign_window_days_before": 21,
        "campaign_window_days_after": 14,
        "b2b_opportunity_en": (
            "Biggest tech event in MENA. Saudi AI companies launch at LEAP. "
            "Publish thought leadership, attend in person, book meetings at venue."
        ),
        "b2b_opportunity_ar": (
            "أكبر فعالية تقنية في الشرق الأوسط وشمال أفريقيا. تطلق شركات الذكاء الاصطناعي السعودية منتجاتها في ليب. "
            "انشر قيادة الفكر، احضر شخصياً، احجز اجتماعات في الموقع."
        ),
        "content_ideas": [
            "Pre-LEAP: '5 AI trends shaping Saudi business in 2025'",
            "At LEAP: Live LinkedIn updates, team photos, client meetings",
            "Post-LEAP: '3 insights from LEAP for Saudi B2B leaders'",
        ],
        "avoid_en": "Note: LEAP dates shift ~2 weeks each year. Verify exact dates annually.",
        "avoid_ar": "ملاحظة: تواريخ ليب تتحول ~أسبوعين كل سنة. تحقق من التواريخ الدقيقة سنوياً.",
    },
    {
        "event": "Saudi National Day",
        "event_ar": "اليوم الوطني السعودي",
        "gregorian_month": 9,
        "gregorian_day": 23,
        "type": "national_holiday",
        "campaign_window_days_before": 10,
        "campaign_window_days_after": 3,
        "b2b_opportunity_en": (
            "Largest national celebration. Saudi companies run campaigns. "
            "Theme: Saudi identity + technology leadership."
        ),
        "b2b_opportunity_ar": (
            "أكبر احتفال وطني. تنفّذ الشركات السعودية حملات. "
            "المحور: الهوية السعودية + الريادة التقنية."
        ),
        "content_ideas": [
            "Arabic-first content: What does Saudi AI mean for our country?",
            "Customer video testimonial in Arabic",
            "Special National Day offer: 10% off sprint engagement (limited)",
        ],
        "avoid_en": "All content must be Arabic-first. Avoid English-only messaging.",
        "avoid_ar": "يجب أن يكون المحتوى عربياً أولاً. تجنب الرسائل الإنجليزية فقط.",
    },
    {
        "event": "Q1 Budget Kickoff",
        "event_ar": "انطلاق ميزانية الربع الأول",
        "gregorian_month": 1,
        "gregorian_day": 10,
        "type": "business_cycle",
        "campaign_window_days_before": 0,
        "campaign_window_days_after": 45,
        "b2b_opportunity_en": (
            "January: new fiscal year budgets active. "
            "Best time to pitch managed services and annual contracts."
        ),
        "b2b_opportunity_ar": (
            "يناير: ميزانيات السنة المالية الجديدة نشطة. "
            "أفضل وقت لتقديم الخدمات المُدارة والعقود السنوية."
        ),
        "content_ideas": [
            "Email campaign: 'Start 2025 with AI-powered revenue intelligence'",
            "LinkedIn: '5 Saudi B2B predictions for 2025'",
            "Webinar: Saudi AI trends for the year ahead",
        ],
        "avoid_en": None,
        "avoid_ar": None,
    },
    {
        "event": "ZATCA Phase 2 Compliance Deadline",
        "event_ar": "موعد امتثال المرحلة الثانية لهيئة الزكاة",
        "gregorian_month": 6,
        "gregorian_day": 1,
        "type": "compliance_deadline",
        "campaign_window_days_before": 60,
        "campaign_window_days_after": 30,
        "b2b_opportunity_en": (
            "Ongoing rollout by company size. "
            "ZATCA compliance is a powerful outreach hook for CFOs."
        ),
        "b2b_opportunity_ar": (
            "طرح مستمر بحسب حجم الشركة. "
            "الامتثال لهيئة الزكاة خطاف تواصل قوي للمديرين الماليين."
        ),
        "content_ideas": [
            "Email: 'Is your business ZATCA Phase 2 ready? [Free checklist]'",
            "LinkedIn: ZATCA Phase 2 explained in 60 seconds (Arabic infographic)",
            "Webinar: ZATCA + AI automation — the case for combined compliance",
        ],
        "avoid_en": "Do not make specific legal compliance claims — always say 'consult your tax advisor'.",
        "avoid_ar": "لا تدّع الامتثال القانوني المحدد — قل دائماً 'استشر مستشارك الضريبي'.",
    },
    {
        "event": "Saudi Fintech Forum",
        "event_ar": "منتدى التقنية المالية السعودي",
        "gregorian_month": 10,
        "gregorian_day": 1,
        "type": "industry_event",
        "campaign_window_days_before": 14,
        "campaign_window_days_after": 7,
        "b2b_opportunity_en": "Annual FinTech event in Riyadh. Great for Islamic finance + BNPL sector outreach.",
        "b2b_opportunity_ar": "فعالية التقنية المالية السنوية في الرياض. ممتازة للتواصل مع قطاع التمويل الإسلامي و BNPL.",
        "content_ideas": [
            "Thought leadership: AI for SAMA-regulated FinTechs",
            "Partner announcement if applicable",
        ],
        "avoid_en": None,
        "avoid_ar": None,
    },
]

# ---------------------------------------------------------------------------
# Ramadan / Eid calendar (approximate, adjusts annually)
# ---------------------------------------------------------------------------

_RAMADAN_CONTENT_STRATEGY: dict[str, Any] = {
    "weeks": [
        {
            "week": 1,
            "theme_en": "Reflection & Preparation",
            "theme_ar": "التأمل والاستعداد",
            "content_approach_en": (
                "Post Ramadan greetings (Arabic first). "
                "Publish 'how Dealix helps during Ramadan' — shorter hours, Suhoor decision windows."
            ),
            "content_approach_ar": (
                "انشر تهاني رمضان (العربية أولاً). "
                "اشرح 'كيف تساعد ديليكس في رمضان' — ساعات أقصر، نوافذ قرار السحور."
            ),
            "post_cadence": "2-3 posts/week (reduced from normal)",
            "avoid": "No sales pitches in week 1 of Ramadan",
        },
        {
            "week": 2,
            "theme_en": "Community & Values",
            "theme_ar": "المجتمع والقيم",
            "content_approach_en": "Human stories. Saudi client spotlight. Team community activities.",
            "content_approach_ar": "قصص إنسانية. تسليط الضوء على العميل السعودي. أنشطة مجتمع الفريق.",
            "post_cadence": "2 posts/week",
            "avoid": "Avoid heavy data/product content",
        },
        {
            "week": 3,
            "theme_en": "Achievement & Growth",
            "theme_ar": "الإنجاز والنمو",
            "content_approach_en": (
                "Begin soft Eid campaign prep. Post 'Saudi business checklist before Eid'."
            ),
            "content_approach_ar": (
                "ابدأ تحضير حملة عيد ناعمة. انشر 'قائمة مراجعة الأعمال السعودية قبل العيد'."
            ),
            "post_cadence": "2-3 posts/week",
            "avoid": None,
        },
        {
            "week": 4,
            "theme_en": "Eid Preparation",
            "theme_ar": "التحضير للعيد",
            "content_approach_en": (
                "Wind down. Plant 'post-Eid' meeting seeds. "
                "Wish clients Eid Mubarak personally (WhatsApp, not broadcast)."
            ),
            "content_approach_ar": (
                "خفّف الإيقاع. ازرع بذور اجتماعات 'ما بعد العيد'. "
                "تمنَّ على العملاء عيداً مباركاً شخصياً (واتساب، ليس بث جماعي)."
            ),
            "post_cadence": "1 post/week",
            "avoid": "NEVER send cold sales messages during Eid break",
        },
    ],
    "post_eid_window": {
        "timing_en": "First 3 business days after Eid al-Fitr",
        "timing_ar": "أول 3 أيام عمل بعد عيد الفطر",
        "strategy_en": (
            "Peak B2B decision window. Executives refreshed. Budget Q2 still open. "
            "Send: 'Eid Mubarak + let's connect this week' emails. Response rates peak here."
        ),
        "strategy_ar": (
            "ذروة نافذة قرار B2B. المسؤولون التنفيذيون في أفضل حالاتهم. ميزانية الربع الثاني لا تزال مفتوحة. "
            "أرسل: بريد 'عيد مبارك + لنتواصل هذا الأسبوع'. معدلات الاستجابة في ذروتها هنا."
        ),
    },
}

# ---------------------------------------------------------------------------
# Monthly B2B themes
# ---------------------------------------------------------------------------

_MONTHLY_THEMES: list[dict[str, Any]] = [
    {"month": 1, "theme_en": "New Year Planning", "theme_ar": "تخطيط السنة الجديدة",
     "focus": "Annual contracts, new budget pitches", "content_type": "educational + offer"},
    {"month": 2, "theme_en": "LEAP + Founding Day", "theme_ar": "ليب + يوم التأسيس",
     "focus": "Tech thought leadership, Saudi pride", "content_type": "thought leadership + celebration"},
    {"month": 3, "theme_en": "Ramadan (varies)", "theme_ar": "رمضان (متغير)",
     "focus": "Community, values, relationship building", "content_type": "community + soft"},
    {"month": 4, "theme_en": "Post-Eid Momentum", "theme_ar": "زخم ما بعد العيد",
     "focus": "Peak sales month, close Q1 deals", "content_type": "sales + case studies"},
    {"month": 5, "theme_en": "Growth & Execution", "theme_ar": "النمو والتنفيذ",
     "focus": "Client results, ROI reports, upsell", "content_type": "proof + expansion"},
    {"month": 6, "theme_en": "Mid-Year Review", "theme_ar": "مراجعة منتصف العام",
     "focus": "H1 results, ZATCA compliance, H2 planning", "content_type": "analytical + compliance"},
    {"month": 7, "theme_en": "Summer Slowdown", "theme_ar": "تباطؤ الصيف",
     "focus": "Long reads, evergreen content, relationship building", "content_type": "educational"},
    {"month": 8, "theme_en": "Back to Business", "theme_ar": "العودة للعمل",
     "focus": "Q3 campaign launch, new prospect outreach", "content_type": "campaigns"},
    {"month": 9, "theme_en": "National Day", "theme_ar": "اليوم الوطني",
     "focus": "Saudi pride, Vision 2030 stories, client spotlights", "content_type": "celebration + proof"},
    {"month": 10, "theme_en": "Q4 Push", "theme_ar": "دفعة الربع الرابع",
     "focus": "Budget spend-down, annual renewals, new pilots", "content_type": "sales + urgency"},
    {"month": 11, "theme_en": "Year-End Intelligence", "theme_ar": "ذكاء نهاية العام",
     "focus": "Annual reports, benchmarks, predictions", "content_type": "thought leadership"},
    {"month": 12, "theme_en": "Planning Season", "theme_ar": "موسم التخطيط",
     "focus": "2026 planning, annual deals, relationship visits", "content_type": "relationship + planning"},
]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/annual-events", summary="Key Saudi B2B marketing events for the year")
async def get_annual_events(
    month: int | None = Query(None, ge=1, le=12, description="Filter by Gregorian month"),
) -> dict[str, Any]:
    events = _ANNUAL_EVENTS
    if month is not None:
        events = [e for e in _ANNUAL_EVENTS if e["gregorian_month"] == month]

    return {
        "events": events,
        "total": len(events),
        "note_en": "Event dates approximate — verify LEAP and Islamic holiday dates annually.",
        "note_ar": "تواريخ الفعاليات تقريبية — تحقق من تواريخ ليب والأعياد الإسلامية سنوياً.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/ramadan-strategy", summary="Content strategy framework for Ramadan")
async def get_ramadan_strategy() -> dict[str, Any]:
    return {
        **_RAMADAN_CONTENT_STRATEGY,
        "key_rule_en": "Ramadan = relationship investment, NOT sales pressure.",
        "key_rule_ar": "رمضان = استثمار في العلاقة، وليس ضغط على المبيعات.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/monthly-themes", summary="Monthly B2B content themes for the Saudi market")
async def get_monthly_themes(
    month: int | None = Query(None, ge=1, le=12),
) -> dict[str, Any]:
    themes = _MONTHLY_THEMES
    if month is not None:
        themes = [t for t in _MONTHLY_THEMES if t["month"] == month]
        if not themes:
            raise HTTPException(status_code=404, detail=f"Month {month} not found.")
    return {
        "themes": themes,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
