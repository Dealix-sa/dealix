"""Pricing Intelligence API — Saudi B2B SaaS pricing psychology and positioning.

Helps the Dealix sales team navigate price objections, anchor correctly,
and simulate ROI for prospects.

Endpoints:
  GET  /api/v1/pricing-intelligence/principles     — 6 pricing principles
  GET  /api/v1/pricing-intelligence/anchor-scripts — 5 pricing conversation scripts
  GET  /api/v1/pricing-intelligence/tier-psychology — psychological positioning per tier
  POST /api/v1/pricing-intelligence/simulate-roi   — ROI simulation from prospect inputs

GET endpoints return governance_decision: ALLOW_WITH_REVIEW.
POST /simulate-roi returns governance_decision: APPROVAL_FIRST.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/pricing-intelligence", tags=["Sales"])

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_WRITE = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Pricing psychology principles
# ---------------------------------------------------------------------------

_PRICING_PSYCHOLOGY: dict[str, dict[str, Any]] = {
    "anchor_high_first": {
        "principle_id": "anchor_high_first",
        "title_en": "Anchor High First",
        "title_ar": "ابدأ بالعرض الأعلى قيمةً أولًا",
        "description_en": (
            "Always present the most premium option first in any pricing conversation. "
            "The first number mentioned becomes the cognitive anchor. "
            "Starting with the custom enterprise tier (SAR 5K–25K) makes the "
            "managed ops tier (SAR 2,999–4,999/mo) feel accessible by comparison."
        ),
        "description_ar": (
            "قدّم دائمًا الخيار الأعلى قيمةً أولًا في أي محادثة تسعير. "
            "الرقم الأول المذكور يُصبح المرساة الإدراكية. "
            "البدء بمستوى المؤسسات المخصص (5,000–25,000 ريال) يجعل "
            "مستوى العمليات المُدارة (2,999–4,999 ريال/شهر) يبدو في متناول اليد بالمقارنة."
        ),
        "application_en": "Open every pricing conversation with the Custom AI tier before descending.",
        "application_ar": "افتح كل محادثة تسعير بمستوى الذكاء الاصطناعي المخصص قبل النزول إلى الأدنى.",
    },
    "zatca_roi_anchor": {
        "principle_id": "zatca_roi_anchor",
        "title_en": "ZATCA ROI Anchor",
        "title_ar": "مرساة عائد الاستثمار في الامتثال الضريبي",
        "description_en": (
            "ZATCA non-compliance fines start at SAR 10,000 per violation and can reach "
            "SAR 50,000 for repeat offences. "
            "A single ZATCA fine covers more than 20 months of the SAR 499 sprint. "
            "Always quantify the compliance cost before presenting the product price."
        ),
        "description_ar": (
            "غرامات عدم الامتثال لزكاة تبدأ من 10,000 ريال للمخالفة الواحدة وقد تصل "
            "إلى 50,000 ريال للمخالفات المتكررة. "
            "غرامة زكاة واحدة تُغطي أكثر من 20 شهرًا من سبرينت 499 ريال. "
            "قيّم دائمًا تكلفة الامتثال قبل تقديم سعر المنتج."
        ),
        "application_en": (
            "Ask: 'Have you received any ZATCA notices in the past 12 months?' "
            "Then present fine risk before product price."
        ),
        "application_ar": (
            "اسأل: 'هل تلقيتم أي إشعارات من هيئة الزكاة خلال الـ12 شهرًا الماضية؟' "
            "ثم قدّم مخاطر الغرامات قبل سعر المنتج."
        ),
    },
    "ramadan_sensitivity": {
        "principle_id": "ramadan_sensitivity",
        "title_en": "Ramadan Timing Sensitivity",
        "title_ar": "حساسية التوقيت في رمضان",
        "description_en": (
            "Never push for a price commitment during Ramadan weeks 1–2. "
            "Decision-making is culturally deprioritised during this period. "
            "Use Ramadan to build relationship, send educational content, and "
            "prepare a post-Eid proposal. "
            "The strongest closing window is the 2 weeks immediately after Eid al-Fitr."
        ),
        "description_ar": (
            "لا تضغط أبداً على التزام بالسعر خلال الأسبوعين الأولين من رمضان. "
            "اتخاذ القرارات مُؤجَّل ثقافيًا خلال هذه الفترة. "
            "استخدم رمضان لبناء العلاقة وإرسال محتوى تثقيفي "
            "وإعداد مقترح ما بعد العيد. "
            "نافذة الإغلاق الأقوى هي الأسبوعان اللذان يليان عيد الفطر مباشرةً."
        ),
        "application_en": "Set all post-Ramadan proposals to send on day 3 post-Eid.",
        "application_ar": "اضبط جميع مقترحات ما بعد رمضان لترسل في اليوم الثالث بعد العيد.",
    },
    "relationship_before_price": {
        "principle_id": "relationship_before_price",
        "title_en": "Relationship Before Price",
        "title_ar": "العلاقة قبل السعر",
        "description_en": (
            "Saudi B2B buyers need to trust the person before they trust the price. "
            "Rushing to a price conversation before establishing rapport leads to "
            "price objections that are really trust objections in disguise. "
            "Use the free diagnostic as a trust-building mechanism, "
            "not just a sales qualifier."
        ),
        "description_ar": (
            "يحتاج المشترون في B2B السعودي إلى الوثوق بالشخص قبل الوثوق بالسعر. "
            "التسرع في محادثة السعر قبل بناء العلاقة يؤدي إلى اعتراضات سعرية "
            "هي في الحقيقة اعتراضات ثقة مُقنَّعة. "
            "استخدم التشخيص المجاني كآلية لبناء الثقة وليس فقط كمؤهل مبيعات."
        ),
        "application_en": (
            "Complete at least one in-person or video meeting before sending any pricing. "
            "Reference shared context (sector, city, Vision 2030 goals) in the proposal."
        ),
        "application_ar": (
            "أكمل اجتماعًا شخصيًا أو عبر الفيديو على الأقل قبل إرسال أي تسعير. "
            "أشر إلى السياق المشترك (القطاع، المدينة، أهداف رؤية 2030) في المقترح."
        ),
    },
    "arabic_price_framing": {
        "principle_id": "arabic_price_framing",
        "title_en": "Arabic Price Framing",
        "title_ar": "صياغة السعر بالعربية",
        "description_en": (
            "When presenting prices to Arabic-speaking prospects, use Arabic numerals "
            "and frame the spend as an investment (استثمار) rather than a cost (تكلفة). "
            "Break monthly prices into daily equivalents — "
            "SAR 499 = SAR 16/day, less than a business lunch."
        ),
        "description_ar": (
            "عند تقديم الأسعار للعملاء المحتملين الناطقين بالعربية، استخدم الأرقام العربية "
            "وصغ الإنفاق باعتباره استثمارًا وليس تكلفة. "
            "قسّم الأسعار الشهرية إلى معادلات يومية — "
            "499 ريال = 16 ريالًا/يوم، أقل من تكلفة غداء عمل."
        ),
        "application_en": (
            "In Arabic proposals, always show: monthly price, daily equivalent, "
            "and annual ROI in that order."
        ),
        "application_ar": (
            "في المقترحات العربية، اعرض دائمًا: السعر الشهري، المعادل اليومي، "
            "والعائد السنوي على الاستثمار بهذا الترتيب."
        ),
    },
    "competitor_price_anchoring": {
        "principle_id": "competitor_price_anchoring",
        "title_en": "Competitor Price Anchoring",
        "title_ar": "مرساة أسعار المنافسين",
        "description_en": (
            "Big 4 consulting firms (McKinsey, BCG, Deloitte) charge SAR 200,000+ "
            "for a revenue intelligence engagement. "
            "Dealix delivers comparable insight at 50x less cost. "
            "Always anchor against a credible high-price alternative before presenting "
            "Dealix pricing — it reframes the entire value conversation."
        ),
        "description_ar": (
            "تتقاضى شركات الاستشارات الكبرى (ماكنزي، BCG، ديلويت) أكثر من 200,000 ريال "
            "لمشاركة استخبارات الإيرادات. "
            "تُقدّم Dealix رؤى مقارنة بتكلفة أقل بـ50 مرة. "
            "قارن دائمًا بالبديل عالي السعر الموثوق قبل تقديم تسعير Dealix — "
            "إذ يُعيد ذلك صياغة محادثة القيمة بأكملها."
        ),
        "application_en": (
            "Say: 'A Big 4 firm would charge SAR 200K for this analysis. "
            "We deliver the same result for SAR 499 in 7 days.'"
        ),
        "application_ar": (
            "قل: 'شركة استشارات كبرى ستتقاضى 200,000 ريال لهذا التحليل. "
            "نحن نُقدّم نفس النتيجة بـ499 ريال في 7 أيام.'"
        ),
    },
}

# ---------------------------------------------------------------------------
# Pricing anchor scripts
# ---------------------------------------------------------------------------

_PRICE_ANCHOR_SCRIPTS: list[dict[str, Any]] = [
    {
        "scenario_en": "Prospect says price is too high",
        "scenario_ar": "العميل المحتمل يقول إن السعر مرتفع جدًا",
        "script_en": (
            "Completely understand. Let's put it in perspective: "
            "SAR 499 is SAR 16 per day — less than a business lunch. "
            "Over the 7-day sprint, we'll identify at least one revenue leak "
            "worth 10x that amount. "
            "If we find nothing worth fixing, I'll give you a full refund."
        ),
        "script_ar": (
            "أفهم ذلك تمامًا. لنضع الأمر في سياقه: "
            "499 ريال تعني 16 ريالًا في اليوم — أقل من تكلفة غداء عمل. "
            "خلال سبرينت الـ7 أيام، سنحدد تسربًا واحدًا على الأقل في الإيرادات "
            "يساوي 10 أضعاف هذا المبلغ. "
            "إذا لم نجد شيئًا يستحق المعالجة، سأعيد إليك المبلغ كاملًا."
        ),
        "avoid_en": "Never justify the price with feature lists alone — always anchor to ROI first.",
        "avoid_ar": "لا تُبرّر السعر بقوائم الميزات وحدها — ابدأ دائمًا بمرساة العائد على الاستثمار.",
    },
    {
        "scenario_en": "Prospect asks for a discount",
        "scenario_ar": "العميل المحتمل يطلب خصمًا",
        "script_en": (
            "Rather than discounting, let me offer you something more valuable: "
            "a free 30-minute diagnostic before you commit to anything. "
            "We'll identify exactly where your revenue is leaking "
            "and then you can decide if the sprint is worth it. "
            "A discount saves you SAR 50 — the diagnostic could save you SAR 50,000."
        ),
        "script_ar": (
            "بدلًا من الخصم، دعني أقدّم لك شيئًا أكثر قيمةً: "
            "تشخيص مجاني لمدة 30 دقيقة قبل أن تلتزم بأي شيء. "
            "سنحدد بالضبط أين يتسرب إيرادك "
            "وبعدها يمكنك أن تقرر إذا كان السبرينت يستحق ذلك. "
            "الخصم يوفر 50 ريالًا — أما التشخيص فقد يوفر 50,000 ريال."
        ),
        "avoid_en": (
            "Never offer a discount as a first response to a discount request. "
            "Always offer a free diagnostic or extended sprint scope instead."
        ),
        "avoid_ar": (
            "لا تقدّم خصمًا كردة فعل أولى على طلب الخصم. "
            "قدّم دائمًا تشخيصًا مجانيًا أو نطاق سبرينت موسّعًا بدلًا من ذلك."
        ),
    },
    {
        "scenario_en": "Prospect compares to a cheaper tool",
        "scenario_ar": "العميل المحتمل يقارن بأداة أرخص",
        "script_en": (
            "That tool was built for a global market. "
            "We were built for Saudi Arabia: "
            "ZATCA Phase 2 integration is native, not a plugin. "
            "Arabic NLP is core, not an add-on. "
            "Prayer-time scheduling is built in. "
            "How many months will it take them to configure Arabic language support? "
            "We're live in 7 days."
        ),
        "script_ar": (
            "تلك الأداة مُصمَّمة للسوق العالمي. "
            "نحن مُصمَّمون للمملكة العربية السعودية: "
            "تكامل زكاة المرحلة الثانية أصيل وليس إضافةً خارجية. "
            "معالجة اللغة الطبيعية بالعربية أساسية وليست ميزةً إضافية. "
            "جدولة أوقات الصلاة مدمجة. "
            "كم شهرًا سيستغرقهم ضبط دعم اللغة العربية؟ "
            "نحن نعمل خلال 7 أيام."
        ),
        "avoid_en": "Never attack the competitor directly — differentiate on Saudi-specific value only.",
        "avoid_ar": "لا تهاجم المنافس مباشرةً — فرّق نفسك بالقيمة السعودية المحددة فقط.",
    },
    {
        "scenario_en": "CFO asks for ROI justification",
        "scenario_ar": "المدير المالي يطلب مسوّغ العائد على الاستثمار",
        "script_en": (
            "Happy to walk through the numbers with you. "
            "Three buckets: "
            "One — ZATCA fine avoidance: at SAR 10K per violation, one avoided fine "
            "pays for 20 months of our service. "
            "Two — reporting time savings: if your team spends 10 hours/week on manual reports, "
            "we automate 70% of that — that is SAR 30,000+ in analyst time annually. "
            "Three — pipeline acceleration: faster data means faster decisions. "
            "Would you like me to build a model with your actual numbers?"
        ),
        "script_ar": (
            "يسعدني استعراض الأرقام معك. "
            "ثلاثة محاور: "
            "أولًا — تجنب غرامات زكاة: بـ10,000 ريال للمخالفة الواحدة، غرامة واحدة مُتجنَّبة "
            "تُغطي 20 شهرًا من خدمتنا. "
            "ثانيًا — توفير وقت إعداد التقارير: إذا أمضى فريقك 10 ساعات أسبوعيًا في تقارير يدوية، "
            "نحن نؤتمت 70% منها — ما يعني أكثر من 30,000 ريال في تكلفة المحللين سنويًا. "
            "ثالثًا — تسريع خط الأنابيب: البيانات الأسرع تعني قرارات أسرع. "
            "هل تريد مني بناء نموذج بأرقامك الفعلية؟"
        ),
        "avoid_en": (
            "Never present ROI as a guarantee. Always use 'estimated' and "
            "'based on your inputs' language."
        ),
        "avoid_ar": (
            "لا تقدّم عائد الاستثمار باعتباره ضمانًا. استخدم دائمًا لغة 'مُقدَّر' "
            "و'بناءً على مدخلاتك'."
        ),
    },
    {
        "scenario_en": "Prospect wants to start small",
        "scenario_ar": "العميل المحتمل يريد البدء بشكل صغير",
        "script_en": (
            "Starting small is exactly right — that is what we designed for. "
            "The path is: "
            "Free diagnostic today — zero commitment, 30 minutes. "
            "If we find a real problem, SAR 499 sprint over 7 days to fix it and prove the value. "
            "If that sprint delivers, Data Pack at SAR 1,500 to lock in the improvements. "
            "From there, managed ops at SAR 2,999/month when you are ready to scale. "
            "You are in control of every step."
        ),
        "script_ar": (
            "البدء بشكل صغير هو الصواب تمامًا — هذا ما صمّمنا المنتج من أجله. "
            "المسار هو: "
            "تشخيص مجاني اليوم — بدون أي التزام، 30 دقيقة. "
            "إذا وجدنا مشكلة حقيقية، سبرينت 499 ريال على مدى 7 أيام لإصلاحها وإثبات القيمة. "
            "إذا حقق السبرينت نتائج، حزمة البيانات بـ1,500 ريال لترسيخ التحسينات. "
            "ومن هناك، عمليات مُدارة بـ2,999 ريال/شهر عندما تكون مستعدًا للتوسع. "
            "أنت تتحكم في كل خطوة."
        ),
        "avoid_en": (
            "Never let 'start small' become 'stay small'. "
            "Always present the full upsell path in the first conversation."
        ),
        "avoid_ar": (
            "لا تدع 'البدء بشكل صغير' يتحول إلى 'البقاء صغيرًا'. "
            "قدّم دائمًا مسار الترقية الكامل في المحادثة الأولى."
        ),
    },
]

# ---------------------------------------------------------------------------
# Tier psychological positioning
# ---------------------------------------------------------------------------

_TIER_PSYCHOLOGY: dict[str, dict[str, Any]] = {
    "free_diagnostic": {
        "tier_id": "free_diagnostic",
        "price_sar": 0,
        "positioning_en": (
            "Zero risk entry — Saudi buyers need to feel before committing. "
            "The diagnostic removes the psychological barrier of spending money "
            "on an unknown vendor. It is the trust handshake, not a product demo."
        ),
        "positioning_ar": (
            "نقطة دخول بدون مخاطر — يحتاج المشتري السعودي إلى الإحساس بالقيمة قبل الالتزام. "
            "التشخيص يزيل الحاجز النفسي للإنفاق على مورد غير معروف. "
            "إنه مصافحة الثقة وليس عرضًا تجريبيًا للمنتج."
        ),
        "frame_en": "Cost of inaction vs cost of 30 minutes",
        "frame_ar": "تكلفة عدم التصرف مقابل تكلفة 30 دقيقة",
    },
    "sprint_499": {
        "tier_id": "sprint_499",
        "price_sar": 499,
        "positioning_en": (
            "SAR 499 is a rounding error in any Saudi B2B budget. "
            "Frame it as the cost of one business lunch, not a procurement decision. "
            "The champion can approve this without a committee. "
            "Speed is the sale: '7 days, one deliverable, no contract required.'"
        ),
        "positioning_ar": (
            "499 ريال خطأ تقريب في أي ميزانية B2B سعودية. "
            "صغها باعتبارها تكلفة غداء عمل واحد، وليس قرارًا للمشتريات. "
            "يمكن للبطل الموافقة عليها دون لجنة. "
            "السرعة هي البيعة: '7 أيام، تسليم واحد، لا يلزم عقد.'"
        ),
        "frame_en": "Less than one business lunch; approved in 5 minutes",
        "frame_ar": "أقل من غداء عمل واحد؛ موافقة في 5 دقائق",
    },
    "data_pack_1500": {
        "tier_id": "data_pack_1500",
        "price_sar": 1_500,
        "positioning_en": (
            "SAR 1,500 is less than one employee's monthly cost for any knowledge role. "
            "Frame it against the manual reporting burden: "
            "if your analyst spends 10 hours/week on reports, "
            "this pack pays back in the first week."
        ),
        "positioning_ar": (
            "1,500 ريال أقل من تكلفة موظف واحد شهريًا في أي دور معرفي. "
            "صغها في مقابل عبء إعداد التقارير اليدوية: "
            "إذا أمضى المحلل 10 ساعات أسبوعيًا في التقارير، "
            "فإن هذه الحزمة تُؤدي ثمنها في الأسبوع الأول."
        ),
        "frame_en": "Less than one week of a junior analyst's time",
        "frame_ar": "أقل من أسبوع عمل محلل مبتدئ",
    },
    "managed_ops_2999_4999": {
        "tier_id": "managed_ops_2999_4999",
        "price_sar_min": 2_999,
        "price_sar_max": 4_999,
        "positioning_en": (
            "CFO logic: SAR 4,999/month versus hiring a data analyst at SAR 12,000/month. "
            "You get a full ops team, not one person. "
            "Frame as headcount replacement, not software cost. "
            "Annual commitment (SAR 60K) is still below open-tender threshold."
        ),
        "positioning_ar": (
            "منطق المدير المالي: 4,999 ريال/شهر مقابل توظيف محلل بيانات بـ12,000 ريال/شهر. "
            "تحصل على فريق عمليات كامل وليس شخصًا واحدًا. "
            "صغها باعتبارها بديلًا للاستئجار، وليست تكلفة برمجيات. "
            "الالتزام السنوي (60,000 ريال) لا يزال أقل من حد المناقصة المفتوحة."
        ),
        "frame_en": "Headcount replacement: full team vs one hire",
        "frame_ar": "بديل توظيف: فريق كامل مقابل موظف واحد",
    },
    "custom_ai_5k_25k": {
        "tier_id": "custom_ai_5k_25k",
        "price_sar_min": 5_000,
        "price_sar_max": 25_000,
        "positioning_en": (
            "Enterprise anchor: present alongside Vision 2030 ROI, not just operational savings. "
            "The CFO conversation is about programme-level impact — "
            "how many Vision 2030 KPIs does this accelerate? "
            "Reference comparable Big 4 engagement costs (SAR 200K–500K) "
            "to make SAR 25K feel like a fraction."
        ),
        "positioning_ar": (
            "مرساة المؤسسات: قدّمها إلى جانب عائد استثمار رؤية 2030، وليس الوفورات التشغيلية فقط. "
            "محادثة المدير المالي تدور حول التأثير على مستوى البرنامج — "
            "كم من مؤشرات الأداء في رؤية 2030 تُسرّع هذه الخدمة؟ "
            "أشر إلى تكاليف المشاركة المقارنة لشركات الاستشارات الكبرى (200,000–500,000 ريال) "
            "ليبدو 25,000 ريال كجزء صغير من ذلك."
        ),
        "frame_en": "Vision 2030 programme ROI; a fraction of Big 4 consulting cost",
        "frame_ar": "عائد استثمار برنامج رؤية 2030؛ جزء صغير من تكلفة استشارات الكبار",
    },
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class PriceSimulatorInput(BaseModel):
    annual_manual_reporting_hours: float = Field(
        ge=0,
        description="Hours per year spent on manual reporting that could be automated.",
    )
    hourly_fully_loaded_cost_sar: float = Field(
        ge=0,
        default=75.0,
        description="Fully loaded cost per hour for the staff doing manual reporting (SAR).",
    )
    zatca_non_compliance_risk_sar: float = Field(
        ge=0,
        default=0.0,
        description="Estimated annual ZATCA non-compliance fine exposure (SAR).",
    )
    missed_deals_per_year: int = Field(
        ge=0,
        default=0,
        description="Number of deals estimated to be lost annually due to slow pipeline.",
    )
    avg_deal_size_sar: float = Field(
        ge=0,
        default=3500.0,
        description="Average deal size in SAR.",
    )


# ---------------------------------------------------------------------------
# Pure computation
# ---------------------------------------------------------------------------

_SPRINT_PRICE_SAR: float = 499.0
_MANAGED_OPS_ANNUAL_SAR: float = 48_000.0  # SAR 4,000/mo * 12


def _simulate_price_roi(inp: PriceSimulatorInput) -> dict[str, Any]:
    """Compute estimated ROI from a prospect's cost inputs.

    All percentage assumptions (0.7, 0.8, 0.3) are conservative estimates
    used for illustration. They are not guarantees of outcome.
    """
    annual_reporting_savings: float = (
        inp.annual_manual_reporting_hours
        * inp.hourly_fully_loaded_cost_sar
        * 0.7
    )
    compliance_savings: float = inp.zatca_non_compliance_risk_sar * 0.8
    pipeline_uplift: float = (
        inp.missed_deals_per_year * inp.avg_deal_size_sar * 0.3
    )
    total_annual_value: float = (
        annual_reporting_savings + compliance_savings + pipeline_uplift
    )

    roi_at_sprint: float = (
        (total_annual_value - _SPRINT_PRICE_SAR) / _SPRINT_PRICE_SAR * 100
        if _SPRINT_PRICE_SAR > 0
        else 0.0
    )
    roi_at_managed_ops: float = (
        (total_annual_value - _MANAGED_OPS_ANNUAL_SAR) / _MANAGED_OPS_ANNUAL_SAR * 100
        if _MANAGED_OPS_ANNUAL_SAR > 0
        else 0.0
    )

    payback_months_sprint: float = (
        _SPRINT_PRICE_SAR / (total_annual_value / 12)
        if total_annual_value > 0
        else 999.0
    )
    payback_months_managed_ops: float = (
        _MANAGED_OPS_ANNUAL_SAR / total_annual_value * 12
        if total_annual_value > 0
        else 999.0
    )

    if total_annual_value >= _MANAGED_OPS_ANNUAL_SAR * 1.5:
        recommended_tier = "managed_ops_2999_4999"
    elif total_annual_value >= _SPRINT_PRICE_SAR * 20:
        recommended_tier = "data_pack_1500"
    elif total_annual_value > 0:
        recommended_tier = "sprint_499"
    else:
        recommended_tier = "free_diagnostic"

    return {
        "annual_reporting_savings_sar": round(annual_reporting_savings, 2),
        "compliance_savings_sar": round(compliance_savings, 2),
        "pipeline_uplift_sar": round(pipeline_uplift, 2),
        "total_annual_value_sar": round(total_annual_value, 2),
        "roi_at_sprint_pct": round(roi_at_sprint, 1),
        "roi_at_managed_ops_pct": round(roi_at_managed_ops, 1),
        "payback_months_sprint": round(payback_months_sprint, 1),
        "payback_months_managed_ops": round(payback_months_managed_ops, 1),
        "recommended_tier": recommended_tier,
        "assumptions_en": {
            "reporting_automation_rate": "70% of manual reporting hours automated",
            "compliance_risk_reduction": "80% reduction in ZATCA fine exposure",
            "deal_recovery_rate": "30% of missed deals recovered via faster pipeline",
        },
        "assumptions_ar": {
            "reporting_automation_rate": "70% من ساعات التقارير اليدوية مُؤتمتة",
            "compliance_risk_reduction": "80% تخفيض في مخاطر غرامات زكاة",
            "deal_recovery_rate": "30% من الصفقات الضائعة مُستردة عبر خط أنابيب أسرع",
        },
        "disclaimer_en": (
            "All figures are estimates based on the inputs provided. "
            "Actual results depend on implementation quality and client engagement. "
            "These are not guarantees of outcome."
        ),
        "disclaimer_ar": (
            "جميع الأرقام تقديرات مبنية على المدخلات المقدمة. "
            "تعتمد النتائج الفعلية على جودة التنفيذ ومستوى مشاركة العميل. "
            "هذه ليست ضمانات بالنتائج."
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/principles")
async def get_pricing_principles() -> dict[str, Any]:
    """Return all 6 pricing psychology principles for Saudi B2B selling."""
    return {
        "governance_decision": _GOV_READ,
        "total_principles": len(_PRICING_PSYCHOLOGY),
        "principles": list(_PRICING_PSYCHOLOGY.values()),
    }


@router.get("/anchor-scripts")
async def get_anchor_scripts() -> dict[str, Any]:
    """Return all 5 pricing conversation scripts with bilingual guidance."""
    return {
        "governance_decision": _GOV_READ,
        "total_scripts": len(_PRICE_ANCHOR_SCRIPTS),
        "scripts": _PRICE_ANCHOR_SCRIPTS,
    }


@router.get("/tier-psychology")
async def get_tier_psychology() -> dict[str, Any]:
    """Return psychological positioning rationale for each Dealix pricing tier."""
    return {
        "governance_decision": _GOV_READ,
        "total_tiers": len(_TIER_PSYCHOLOGY),
        "tiers": list(_TIER_PSYCHOLOGY.values()),
    }


@router.post("/simulate-roi")
async def simulate_roi(body: PriceSimulatorInput) -> dict[str, Any]:
    """Compute estimated annual value and payback period from prospect cost inputs.

    All computed figures are estimates, not guaranteed outcomes.
    Results should be reviewed with the prospect before being used in a proposal.
    """
    result = _simulate_price_roi(body)
    return {
        "governance_decision": _GOV_WRITE,
        "inputs": body.model_dump(),
        "currency": "SAR",
        **result,
    }
