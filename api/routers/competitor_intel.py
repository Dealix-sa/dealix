"""Competitive Intelligence API Router.

ADMIN-GATED. Provides competitive landscape data, battlecards,
and win/loss patterns for the Saudi B2B AI/SaaS market.
All competitor data uses fictional company names.

Prefix: /api/v1/competitor-intel
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/competitor-intel",
    tags=["competitor-intel"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Competitor profiles (fictional companies, Saudi B2B AI/SaaS market)
# ---------------------------------------------------------------------------

_COMPETITORS: dict[str, dict[str, Any]] = {
    "alpha_revenue": {
        "id": "alpha_revenue",
        "name": "AlphaRevenue",
        "name_ar": "ألفا ريفينيو",
        "category": "Generic CRM",
        "category_ar": "إدارة علاقات العملاء العامة",
        "pricing_sar_range": {"min": 8_000, "max": 25_000, "unit": "month"},
        "strengths_en": [
            "Established brand in MENA region",
            "Large ecosystem of third-party integrations",
            "Well-funded with strong sales team",
        ],
        "strengths_ar": [
            "علامة تجارية راسخة في منطقة الشرق الأوسط وشمال أفريقيا",
            "نظام بيئي واسع من تكاملات الطرف الثالث",
            "تمويل جيد مع فريق مبيعات قوي",
        ],
        "weaknesses_en": [
            "No Arabic UI — English only",
            "No ZATCA Phase 2 compliance features",
            "No PDPL data governance",
            "No AI governance or approval-first workflow",
            "No verifiable Proof Pack — relies on marketing claims",
            "No compliance-first design for Saudi market",
        ],
        "weaknesses_ar": [
            "لا واجهة عربية — إنجليزية فقط",
            "لا ميزات امتثال لزاتكا المرحلة الثانية",
            "لا حوكمة لبيانات نظام PDPL",
            "لا حوكمة للذكاء الاصطناعي أو سير عمل الموافقة أولاً",
            "لا حزمة إثبات موثقة — يعتمد على ادعاءات تسويقية",
            "لا تصميم مبني على الامتثال للسوق السعودي",
        ],
        "target_segment_en": "Large enterprises, multi-national accounts",
        "target_segment_ar": "المؤسسات الكبيرة والحسابات متعددة الجنسيات",
    },
    "nexus_ops": {
        "id": "nexus_ops",
        "name": "NexusOps KSA",
        "name_ar": "نيكسوس أوبس السعودية",
        "category": "Operations Automation",
        "category_ar": "أتمتة العمليات",
        "pricing_sar_range": {"min": 5_000, "max": 15_000, "unit": "month"},
        "strengths_en": [
            "Partial Arabic interface for core workflows",
            "Strong operations automation templates",
            "Local support team in Riyadh",
        ],
        "strengths_ar": [
            "واجهة عربية جزئية للسير الرئيسية",
            "قوالب أتمتة عمليات قوية",
            "فريق دعم محلي في الرياض",
        ],
        "weaknesses_en": [
            "No AI governance layer",
            "Partial Arabic — key modules remain English",
            "No ZATCA e-invoicing native integration",
            "No PDPL compliance tooling",
            "No tiered service ladder — one-size pricing",
            "No proof metrics or verifiable outcome tracking",
        ],
        "weaknesses_ar": [
            "لا طبقة حوكمة للذكاء الاصطناعي",
            "عربية جزئية — الوحدات الرئيسية لا تزال إنجليزية",
            "لا تكامل أصلي لفوترة زاتكا الإلكترونية",
            "لا أدوات امتثال PDPL",
            "لا سلم خدمات متدرج — تسعير موحد",
            "لا مقاييس إثبات أو تتبع نتائج موثق",
        ],
        "target_segment_en": "Mid-market operations-heavy businesses",
        "target_segment_ar": "الشركات متوسطة الحجم كثيفة العمليات",
    },
    "dataflow_arabia": {
        "id": "dataflow_arabia",
        "name": "DataFlow Arabia",
        "name_ar": "ديتافلو عربية",
        "category": "Data Analytics",
        "category_ar": "تحليلات البيانات",
        "pricing_sar_range": {"min": 10_000, "max": 40_000, "unit": "month"},
        "strengths_en": [
            "Strong Arabic localization for dashboards",
            "Good data visualization capabilities",
            "Experienced Saudi leadership team",
        ],
        "strengths_ar": [
            "توطين عربي قوي للوحات المعلومات",
            "قدرات تصوير بيانات جيدة",
            "فريق قيادي سعودي متمرس",
        ],
        "weaknesses_en": [
            "No AI capabilities — pure analytics only",
            "Significantly more expensive than alternatives",
            "No governance or approval workflow",
            "No PDPL-aware data handling",
            "Long implementation timelines (6–12 months)",
            "No entry-level tier — requires large upfront commitment",
        ],
        "weaknesses_ar": [
            "لا قدرات ذكاء اصطناعي — تحليلات بيانات فقط",
            "أعلى تكلفة بشكل ملحوظ مقارنة بالبدائل",
            "لا حوكمة أو سير عمل للموافقة",
            "لا معالجة بيانات مدركة لـ PDPL",
            "جداول تنفيذ طويلة (6–12 شهراً)",
            "لا مستوى أساسي — يتطلب التزاماً مسبقاً كبيراً",
        ],
        "target_segment_en": "Enterprise data teams, government adjacent",
        "target_segment_ar": "فرق البيانات المؤسسية وما يجاور القطاع الحكومي",
    },
    "riyadh_tech": {
        "id": "riyadh_tech",
        "name": "RiyadhTech Suite",
        "name_ar": "حزمة رياض تك",
        "category": "All-in-One Business Suite",
        "category_ar": "حزمة الأعمال الشاملة",
        "pricing_sar_range": {"min": 3_000, "max": 12_000, "unit": "month"},
        "strengths_en": [
            "Wide feature coverage — HR, finance, CRM bundled",
            "Moderate Arabic support",
            "Established Saudi client base",
        ],
        "strengths_ar": [
            "تغطية واسعة للميزات — الموارد البشرية والمالية وإدارة العملاء مجمّعة",
            "دعم عربي معتدل",
            "قاعدة عملاء سعودية راسخة",
        ],
        "weaknesses_en": [
            "Outdated UX — clients report frustration with interface",
            "No AI features or intelligent automation",
            "No ZATCA Phase 2 compliance",
            "No PDPL-specific compliance features",
            "No governance layer",
            "Fragmented product — quality varies by module",
        ],
        "weaknesses_ar": [
            "واجهة مستخدم قديمة — يشكو العملاء من التجربة",
            "لا ميزات ذكاء اصطناعي أو أتمتة ذكية",
            "لا امتثال لزاتكا المرحلة الثانية",
            "لا ميزات امتثال PDPL محددة",
            "لا طبقة حوكمة",
            "منتج مجزأ — الجودة تتفاوت حسب الوحدة",
        ],
        "target_segment_en": "Small and medium Saudi businesses",
        "target_segment_ar": "الشركات الصغيرة والمتوسطة السعودية",
    },
    "jadara_saas": {
        "id": "jadara_saas",
        "name": "Jadara SaaS",
        "name_ar": "جدارة ساس",
        "category": "Arabic-First Startup SaaS",
        "category_ar": "شركة ناشئة SaaS عربية أولاً",
        "pricing_sar_range": {"min": 2_000, "max": 8_000, "unit": "month"},
        "strengths_en": [
            "Arabic-first UI design philosophy",
            "Competitive entry pricing",
            "Culturally attuned product team",
        ],
        "strengths_ar": [
            "فلسفة تصميم واجهة عربية أولاً",
            "تسعير تنافسي للدخول",
            "فريق منتج يفهم الثقافة المحلية",
        ],
        "weaknesses_en": [
            "Weak on delivery — client complaints about delayed projects",
            "No ZATCA or PDPL compliance features",
            "No governance or approval-first workflow",
            "No proof metrics or verifiable outcomes",
            "Early-stage — limited support capacity",
            "No enterprise-grade features",
        ],
        "weaknesses_ar": [
            "ضعف في التسليم — شكاوى عملاء من تأخر المشاريع",
            "لا ميزات امتثال زاتكا أو PDPL",
            "لا حوكمة أو سير عمل موافقة أولاً",
            "لا مقاييس إثبات أو نتائج موثقة",
            "مرحلة مبكرة — طاقة دعم محدودة",
            "لا ميزات على مستوى المؤسسات",
        ],
        "target_segment_en": "Small Saudi businesses, early digital adopters",
        "target_segment_ar": "الشركات الصغيرة السعودية، المتبنون الأوائل للرقمنة",
    },
}

# ---------------------------------------------------------------------------
# Dealix competitive advantages
# ---------------------------------------------------------------------------

_DEALIX_ADVANTAGES: list[dict[str, str]] = [
    {
        "id": "governance_layer",
        "en": "Governance layer with APPROVAL_FIRST workflow — no AI action executes without authorization",
        "ar": "طبقة حوكمة مع سير عمل الموافقة أولاً — لا يُنفَّذ أي إجراء ذكاء اصطناعي دون تفويض",
    },
    {
        "id": "zatca_native",
        "en": "ZATCA Phase 2 native compliance — e-invoicing built in, not bolted on",
        "ar": "امتثال أصلي لزاتكا المرحلة الثانية — الفوترة الإلكترونية مدمجة وليست مضافة",
    },
    {
        "id": "pdpl_builtin",
        "en": "PDPL compliance built in — data sovereignty, consent tracking, DSAR workflows",
        "ar": "امتثال PDPL مدمج — سيادة البيانات، تتبع الموافقة، سير عمل طلبات حقوق الأفراد",
    },
    {
        "id": "arabic_first",
        "en": "Arabic-first UI — not translated, natively designed for Arabic business context",
        "ar": "واجهة عربية أولاً — مصممة أصلاً للسياق التجاري العربي وليست مترجمة",
    },
    {
        "id": "proof_pack",
        "en": "Proof Pack with verifiable metrics — evidence-based outcomes, no unverifiable claims",
        "ar": "حزمة إثبات بمقاييس قابلة للتحقق — نتائج مبنية على الأدلة، لا ادعاءات غير قابلة للتحقق",
    },
    {
        "id": "five_tier_ladder",
        "en": "5-tier service ladder: free diagnostic entry through enterprise custom AI",
        "ar": "سلم خدمات من 5 مستويات: من التشخيص المجاني إلى الذكاء الاصطناعي المؤسسي المخصص",
    },
]

# ---------------------------------------------------------------------------
# Battlecard data (objections + winning responses per competitor, bilingual)
# ---------------------------------------------------------------------------

_BATTLECARDS: dict[str, dict[str, Any]] = {
    "alpha_revenue": {
        "competitor_id": "alpha_revenue",
        "competitor_name": "AlphaRevenue",
        "competitor_name_ar": "ألفا ريفينيو",
        "objections": [
            {
                "objection_en": "AlphaRevenue has more integrations and a bigger ecosystem.",
                "objection_ar": "ألفا ريفينيو لديها تكاملات أكثر ونظام بيئي أكبر.",
                "response_en": (
                    "Integrations are only useful when you can actually use them. "
                    "AlphaRevenue has no Arabic interface, no ZATCA compliance, and no PDPL governance — "
                    "meaning every integration you touch creates a compliance risk. "
                    "Our smaller set of integrations are ZATCA-certified and PDPL-safe by design."
                ),
                "response_ar": (
                    "التكاملات مفيدة فقط عندما يمكنك استخدامها فعلاً. "
                    "ألفا ريفينيو ليس لديها واجهة عربية ولا امتثال زاتكا ولا حوكمة PDPL — "
                    "مما يعني أن كل تكامل تلمسه يخلق خطراً على الامتثال. "
                    "مجموعتنا الأصغر من التكاملات معتمدة من زاتكا وآمنة لـ PDPL بالتصميم."
                ),
            },
            {
                "objection_en": "AlphaRevenue is a well-known brand — lower risk for us.",
                "objection_ar": "ألفا ريفينيو علامة معروفة — أقل خطراً علينا.",
                "response_en": (
                    "Brand recognition does not equal regulatory compliance. "
                    "With ZATCA Phase 2 enforcement and PDPL fines up to 5M SAR, "
                    "the real risk is using a tool that was never built for Saudi law. "
                    "Every Dealix client gets a Proof Pack with documented compliance outcomes."
                ),
                "response_ar": (
                    "الشهرة لا تعني الامتثال التنظيمي. "
                    "مع تطبيق زاتكا المرحلة الثانية وغرامات PDPL تصل إلى 5 ملايين ريال، "
                    "الخطر الحقيقي هو استخدام أداة لم تُبنَ أصلاً لتلبية القانون السعودي. "
                    "كل عميل في ديليكس يحصل على حزمة إثبات بنتائج امتثال موثقة."
                ),
            },
            {
                "objection_en": "AlphaRevenue offers more features.",
                "objection_ar": "ألفا ريفينيو تقدم ميزات أكثر.",
                "response_en": (
                    "More features mean more surface area for compliance gaps. "
                    "We focus on the 20 percent of features that drive 80 percent of Saudi B2B outcomes — "
                    "with a governance layer that ensures every AI action is approved before execution."
                ),
                "response_ar": (
                    "الميزات الأكثر تعني مساحة أكبر لثغرات الامتثال. "
                    "نركز على 20% من الميزات التي تحقق 80% من نتائج الأعمال B2B السعودية — "
                    "مع طبقة حوكمة تضمن الموافقة على كل إجراء ذكاء اصطناعي قبل التنفيذ."
                ),
            },
        ],
        "win_conditions_en": [
            "Prospect has ZATCA Phase 2 deadline pressure",
            "Prospect has PDPL audit risk",
            "Prospect requires Arabic-first interface for team adoption",
            "Prospect was burned by unverifiable ROI claims",
        ],
        "win_conditions_ar": [
            "لدى العميل المحتمل ضغط موعد زاتكا المرحلة الثانية",
            "لدى العميل المحتمل خطر تدقيق PDPL",
            "يتطلب العميل المحتمل واجهة عربية أولاً لتبني الفريق",
            "تضرر العميل المحتمل من ادعاءات ROI غير قابلة للتحقق",
        ],
    },
    "nexus_ops": {
        "competitor_id": "nexus_ops",
        "competitor_name": "NexusOps KSA",
        "competitor_name_ar": "نيكسوس أوبس السعودية",
        "objections": [
            {
                "objection_en": "NexusOps has a local support team already.",
                "objection_ar": "نيكسوس أوبس لديها فريق دعم محلي بالفعل.",
                "response_en": (
                    "Local support for a product without AI governance means faster access to compliance gaps. "
                    "Dealix is built governance-first: every AI recommendation goes through an approval workflow "
                    "before it affects your business processes."
                ),
                "response_ar": (
                    "الدعم المحلي لمنتج بدون حوكمة ذكاء اصطناعي يعني وصولاً أسرع لثغرات الامتثال. "
                    "ديليكس مبني على الحوكمة أولاً: كل توصية ذكاء اصطناعي تمر عبر سير عمل الموافقة "
                    "قبل أن تؤثر على عمليات أعمالك."
                ),
            },
            {
                "objection_en": "NexusOps is cheaper per month.",
                "objection_ar": "نيكسوس أوبس أرخص شهرياً.",
                "response_en": (
                    "Start with our free diagnostic to verify whether you have ZATCA or PDPL exposure. "
                    "If you do, a single regulatory fine can exceed 12 months of Dealix fees. "
                    "Our Sprint tier begins at a comparable price point and includes compliance tooling."
                ),
                "response_ar": (
                    "ابدأ بتشخيصنا المجاني للتحقق مما إذا كان لديك تعرض لزاتكا أو PDPL. "
                    "إذا كان الأمر كذلك، فإن غرامة تنظيمية واحدة يمكن أن تتجاوز 12 شهراً من رسوم ديليكس. "
                    "مستوى Sprint لدينا يبدأ بسعر مقارب ويشمل أدوات الامتثال."
                ),
            },
            {
                "objection_en": "We already use NexusOps for operations — switching is disruptive.",
                "objection_ar": "نستخدم نيكسوس أوبس بالفعل للعمليات — التحويل مُعطِّل.",
                "response_en": (
                    "Dealix integrates alongside existing tools — we do not require a rip-and-replace. "
                    "Our Data Pack tier can layer governance and compliance on top of your current stack "
                    "without operational disruption."
                ),
                "response_ar": (
                    "ديليكس يتكامل مع الأدوات الموجودة — لا نتطلب استبدالاً شاملاً. "
                    "مستوى حزمة البيانات لدينا يمكنه إضافة الحوكمة والامتثال فوق بنيتك الحالية "
                    "دون تعطيل تشغيلي."
                ),
            },
        ],
        "win_conditions_en": [
            "Client is growing beyond NexusOps operational templates",
            "AI governance gap creates internal risk",
            "ZATCA or PDPL compliance not addressed by current stack",
        ],
        "win_conditions_ar": [
            "العميل ينمو تجاوز قوالب عمليات نيكسوس أوبس",
            "فجوة حوكمة الذكاء الاصطناعي تخلق مخاطر داخلية",
            "امتثال زاتكا أو PDPL غير معالج في البنية الحالية",
        ],
    },
    "dataflow_arabia": {
        "competitor_id": "dataflow_arabia",
        "competitor_name": "DataFlow Arabia",
        "competitor_name_ar": "ديتافلو عربية",
        "objections": [
            {
                "objection_en": "DataFlow Arabia has better dashboards.",
                "objection_ar": "ديتافلو عربية لديها لوحات معلومات أفضل.",
                "response_en": (
                    "Dashboards are outputs, not outcomes. DataFlow Arabia shows you data; "
                    "Dealix acts on it — with AI recommendations that require human approval before execution. "
                    "Our Proof Pack shows clients what changed after actions were taken."
                ),
                "response_ar": (
                    "لوحات المعلومات مخرجات، ليست نتائج. ديتافلو عربية تعرض البيانات؛ "
                    "ديليكس يتصرف بناء عليها — مع توصيات ذكاء اصطناعي تتطلب موافقة بشرية قبل التنفيذ. "
                    "حزمة الإثبات لدينا تُظهر للعملاء ما الذي تغير بعد اتخاذ الإجراءات."
                ),
            },
            {
                "objection_en": "DataFlow Arabia is well-established in the Saudi market.",
                "objection_ar": "ديتافلو عربية راسخة في السوق السعودي.",
                "response_en": (
                    "Established does not mean current. DataFlow Arabia has no AI capabilities "
                    "and no compliance features. As Saudi Vision 2030 accelerates AI adoption, "
                    "pure analytics tools without governance are becoming a liability."
                ),
                "response_ar": (
                    "الرسوخ لا يعني الحداثة. ديتافلو عربية ليس لديها قدرات ذكاء اصطناعي "
                    "ولا ميزات امتثال. مع تسارع رؤية السعودية 2030 لتبني الذكاء الاصطناعي، "
                    "أدوات التحليلات البحتة بدون حوكمة تصبح عبئاً."
                ),
            },
            {
                "objection_en": "DataFlow Arabia's implementation team is experienced.",
                "objection_ar": "فريق تنفيذ ديتافلو عربية متمرس.",
                "response_en": (
                    "Their 6–12 month implementation timeline versus our 2-week Sprint pilot. "
                    "You can validate actual results from Dealix before DataFlow Arabia even completes discovery."
                ),
                "response_ar": (
                    "جدول تنفيذهم 6–12 شهراً مقابل تجربة Sprint لمدة أسبوعين لدينا. "
                    "يمكنك التحقق من نتائج فعلية من ديليكس قبل أن تنتهي ديتافلو عربية حتى من مرحلة الاستكشاف."
                ),
            },
        ],
        "win_conditions_en": [
            "Client frustrated with DataFlow Arabia implementation delays",
            "Client needs AI action, not just data visualization",
            "Budget sensitivity — DataFlow Arabia top tier is 40K SAR/month",
        ],
        "win_conditions_ar": [
            "العميل محبط من تأخيرات تنفيذ ديتافلو عربية",
            "العميل يحتاج إجراء ذكاء اصطناعي، ليس مجرد تصوير بيانات",
            "حساسية الميزانية — المستوى الأعلى لديتافلو عربية 40 ألف ريال/شهر",
        ],
    },
    "riyadh_tech": {
        "competitor_id": "riyadh_tech",
        "competitor_name": "RiyadhTech Suite",
        "competitor_name_ar": "حزمة رياض تك",
        "objections": [
            {
                "objection_en": "RiyadhTech covers everything — HR, finance, CRM in one platform.",
                "objection_ar": "رياض تك تغطي كل شيء — الموارد البشرية والمالية وإدارة العملاء في منصة واحدة.",
                "response_en": (
                    "Covering everything does not mean doing any of it well. "
                    "RiyadhTech's fragmented quality is a known issue — some modules are strong, "
                    "others are outdated. Dealix specializes in AI-driven revenue operations "
                    "with ZATCA and PDPL compliance, not a wide but shallow suite."
                ),
                "response_ar": (
                    "تغطية كل شيء لا تعني القيام بأي منها بشكل جيد. "
                    "الجودة المجزأة في رياض تك مشكلة معروفة — بعض الوحدات قوية، "
                    "وبعضها قديم. ديليكس متخصص في عمليات الإيرادات المدفوعة بالذكاء الاصطناعي "
                    "مع امتثال زاتكا و PDPL، وليس حزمة واسعة لكن ضحلة."
                ),
            },
            {
                "objection_en": "RiyadhTech is cheaper for the full suite.",
                "objection_ar": "رياض تك أرخص للحزمة الكاملة.",
                "response_en": (
                    "Compare scope to scope: RiyadhTech offers no AI features, no ZATCA compliance, "
                    "and no governance layer. Dealix's Sprint tier at a similar price point includes "
                    "all three. You are not comparing equivalents."
                ),
                "response_ar": (
                    "قارن النطاق بالنطاق: رياض تك لا تقدم ميزات ذكاء اصطناعي ولا امتثال زاتكا "
                    "ولا طبقة حوكمة. مستوى Sprint في ديليكس بسعر مماثل يشمل الثلاثة. "
                    "لا تقارن بين مكافئين."
                ),
            },
            {
                "objection_en": "Our team already knows RiyadhTech.",
                "objection_ar": "فريقنا يعرف رياض تك بالفعل.",
                "response_en": (
                    "Switching cost concern is valid — that is why we start with a free diagnostic "
                    "and a 2-week Sprint pilot that runs in parallel. "
                    "Your team sees results before any commitment is made."
                ),
                "response_ar": (
                    "قلق تكلفة التحويل مفهوم — لهذا نبدأ بتشخيص مجاني "
                    "وتجربة Sprint لأسبوعين تعمل بالتوازي. "
                    "فريقك يرى النتائج قبل أي التزام."
                ),
            },
        ],
        "win_conditions_en": [
            "UX frustration — team resists RiyadhTech interface",
            "ZATCA deadline forces compliance upgrade",
            "Management wants AI capabilities not available in RiyadhTech",
        ],
        "win_conditions_ar": [
            "إحباط من UX — الفريق يقاوم واجهة رياض تك",
            "موعد زاتكا يجبر على ترقية الامتثال",
            "الإدارة تريد قدرات ذكاء اصطناعي غير متوفرة في رياض تك",
        ],
    },
    "jadara_saas": {
        "competitor_id": "jadara_saas",
        "competitor_name": "Jadara SaaS",
        "competitor_name_ar": "جدارة ساس",
        "objections": [
            {
                "objection_en": "Jadara SaaS is Arabic-first — that is our top priority.",
                "objection_ar": "جدارة ساس عربية أولاً — هذه أولويتنا الأولى.",
                "response_en": (
                    "Dealix is also Arabic-first — and adds ZATCA compliance, PDPL governance, "
                    "and a Proof Pack that Jadara SaaS does not offer. "
                    "Arabic UI is a baseline requirement, not a differentiator on its own."
                ),
                "response_ar": (
                    "ديليكس أيضاً عربي أولاً — ويضيف امتثال زاتكا وحوكمة PDPL "
                    "وحزمة إثبات لا تقدمها جدارة ساس. "
                    "واجهة المستخدم العربية متطلب أساسي، وليست ميزة تمييزية بحد ذاتها."
                ),
            },
            {
                "objection_en": "Jadara SaaS is cheaper.",
                "objection_ar": "جدارة ساس أرخص.",
                "response_en": (
                    "Jadara SaaS's delivery track record has gaps — clients report project delays. "
                    "Dealix offers a 2-week Sprint pilot with verifiable deliverables before you commit "
                    "to a full retainer. You pay for outcomes, not promises."
                ),
                "response_ar": (
                    "سجل تسليم جدارة ساس يحتوي على ثغرات — يُبلغ العملاء عن تأخيرات المشاريع. "
                    "ديليكس يقدم تجربة Sprint لأسبوعين بنتائج قابلة للتحقق قبل الالتزام "
                    "بعقد كامل. تدفع مقابل النتائج، لا الوعود."
                ),
            },
            {
                "objection_en": "We want to support a local startup.",
                "objection_ar": "نريد دعم شركة ناشئة محلية.",
                "response_en": (
                    "Dealix is a Saudi-founded platform built for the Saudi market. "
                    "Supporting local is choosing the option that also delivers — "
                    "with compliance, governance, and verifiable results."
                ),
                "response_ar": (
                    "ديليكس منصة مؤسَّسة سعودياً مبنية للسوق السعودي. "
                    "دعم المحلي يعني اختيار الخيار الذي يُنجز أيضاً — "
                    "بالامتثال والحوكمة والنتائج القابلة للتحقق."
                ),
            },
        ],
        "win_conditions_en": [
            "Prospect was burned by Jadara SaaS delivery failure",
            "Compliance requirements exceed Jadara SaaS capabilities",
            "Prospect is scaling and needs enterprise-grade governance",
        ],
        "win_conditions_ar": [
            "تضرر العميل المحتمل من فشل تسليم جدارة ساس",
            "متطلبات الامتثال تتجاوز قدرات جدارة ساس",
            "العميل المحتمل ينمو ويحتاج حوكمة على مستوى المؤسسات",
        ],
    },
}

# ---------------------------------------------------------------------------
# Win/Loss patterns (demo data)
# ---------------------------------------------------------------------------

_WIN_LOSS_PATTERNS: list[dict[str, Any]] = [
    {
        "competitor_id": "alpha_revenue",
        "competitor_name": "AlphaRevenue",
        "competitor_name_ar": "ألفا ريفينيو",
        "deals_evaluated": 12,
        "deals_won": 9,
        "deals_lost": 3,
        "win_rate_pct": 75,
        "top_win_reason_en": "ZATCA compliance gap in AlphaRevenue",
        "top_win_reason_ar": "فجوة امتثال زاتكا في ألفا ريفينيو",
        "top_loss_reason_en": "Existing long-term contract with AlphaRevenue",
        "top_loss_reason_ar": "عقد طويل الأمد قائم مع ألفا ريفينيو",
        "sector_pattern_en": "Financial services and healthcare win most often",
        "sector_pattern_ar": "الخدمات المالية والرعاية الصحية تفوز في أغلب الأحيان",
    },
    {
        "competitor_id": "nexus_ops",
        "competitor_name": "NexusOps KSA",
        "competitor_name_ar": "نيكسوس أوبس السعودية",
        "deals_evaluated": 8,
        "deals_won": 5,
        "deals_lost": 3,
        "win_rate_pct": 63,
        "top_win_reason_en": "Client needed AI governance not available in NexusOps",
        "top_win_reason_ar": "احتاج العميل حوكمة ذكاء اصطناعي غير متوفرة في نيكسوس أوبس",
        "top_loss_reason_en": "NexusOps existing data integration lock-in",
        "top_loss_reason_ar": "تكامل بيانات نيكسوس أوبس القائم يصعب الخروج منه",
        "sector_pattern_en": "Technology sector wins most; logistics harder to displace",
        "sector_pattern_ar": "قطاع التقنية يفوز في أغلب الأحيان؛ اللوجستيات أصعب في الإزاحة",
    },
    {
        "competitor_id": "dataflow_arabia",
        "competitor_name": "DataFlow Arabia",
        "competitor_name_ar": "ديتافلو عربية",
        "deals_evaluated": 6,
        "deals_won": 5,
        "deals_lost": 1,
        "win_rate_pct": 83,
        "top_win_reason_en": "Client needed AI action capabilities beyond analytics",
        "top_win_reason_ar": "احتاج العميل قدرات إجراءات ذكاء اصطناعي تتجاوز التحليلات",
        "top_loss_reason_en": "Existing DataFlow Arabia multi-year enterprise contract",
        "top_loss_reason_ar": "عقد مؤسسي متعدد السنوات قائم مع ديتافلو عربية",
        "sector_pattern_en": "Win rate highest in SME segment where DataFlow pricing is prohibitive",
        "sector_pattern_ar": "معدل الفوز الأعلى في قطاع الشركات الصغيرة حيث تكون أسعار ديتافلو باهظة",
    },
    {
        "competitor_id": "riyadh_tech",
        "competitor_name": "RiyadhTech Suite",
        "competitor_name_ar": "حزمة رياض تك",
        "deals_evaluated": 15,
        "deals_won": 11,
        "deals_lost": 4,
        "win_rate_pct": 73,
        "top_win_reason_en": "ZATCA deadline created urgency to upgrade from RiyadhTech",
        "top_win_reason_ar": "موعد زاتكا أوجد إلحاحاً للترقية من رياض تك",
        "top_loss_reason_en": "Switching cost concern — team familiarity with RiyadhTech",
        "top_loss_reason_ar": "قلق تكلفة التحويل — الفريق معتاد على رياض تك",
        "sector_pattern_en": "Small retail and services businesses are best targets",
        "sector_pattern_ar": "شركات التجزئة والخدمات الصغيرة هي أفضل الأهداف",
    },
    {
        "competitor_id": "jadara_saas",
        "competitor_name": "Jadara SaaS",
        "competitor_name_ar": "جدارة ساس",
        "deals_evaluated": 10,
        "deals_won": 8,
        "deals_lost": 2,
        "win_rate_pct": 80,
        "top_win_reason_en": "Prospect had experienced a Jadara SaaS delivery failure",
        "top_win_reason_ar": "مر العميل المحتمل بتجربة فشل تسليم في جدارة ساس",
        "top_loss_reason_en": "Price sensitivity — Jadara SaaS entry tier is 2K SAR lower",
        "top_loss_reason_ar": "حساسية السعر — مستوى دخول جدارة ساس أقل بـ 2000 ريال",
        "sector_pattern_en": "Startups and early SMEs show highest win rate",
        "sector_pattern_ar": "الشركات الناشئة والشركات الصغيرة المبكرة تظهر أعلى معدل فوز",
    },
]

# ---------------------------------------------------------------------------
# Helper: build Dealix vs competitor comparison for a given competitor
# ---------------------------------------------------------------------------


def _build_positioning(competitor_id: str) -> dict[str, Any]:
    """Build a Dealix positioning summary against a specific competitor."""
    competitor = _COMPETITORS[competitor_id]
    return {
        "competitor": {
            "id": competitor["id"],
            "name": competitor["name"],
            "name_ar": competitor["name_ar"],
            "weaknesses_en": competitor["weaknesses_en"],
            "weaknesses_ar": competitor["weaknesses_ar"],
        },
        "dealix_advantages": _DEALIX_ADVANTAGES,
        "summary_en": (
            f"{competitor['name']} covers {competitor['category'].lower()} but lacks "
            "ZATCA compliance, PDPL governance, an AI approval workflow, and verifiable proof metrics. "
            "Dealix closes all four gaps with a governance-first architecture."
        ),
        "summary_ar": (
            f"{competitor['name_ar']} تغطي {competitor['category_ar']} لكنها تفتقر إلى "
            "امتثال زاتكا وحوكمة PDPL وسير عمل موافقة ذكاء اصطناعي ومقاييس إثبات قابلة للتحقق. "
            "ديليكس يسد الفجوات الأربع بهندسة قائمة على الحوكمة أولاً."
        ),
    }


def _compute_win_score(our_features: list[str], competitor_id: str) -> int:
    """
    Compute a win score (0–100) by matching our_features against
    the competitor's known weaknesses.

    Each matched weakness contributes equally to the score.
    """
    competitor = _COMPETITORS[competitor_id]
    weakness_keywords: list[str] = []
    for w in competitor["weaknesses_en"]:
        weakness_keywords.extend(w.lower().split())

    matched = 0
    for feature in our_features:
        feature_lower = feature.lower()
        for w in competitor["weaknesses_en"]:
            if any(word in w.lower() for word in feature_lower.split()):
                matched += 1
                break

    total_weaknesses = len(competitor["weaknesses_en"])
    if total_weaknesses == 0:
        return 50
    raw = (matched / total_weaknesses) * 100
    # Boost by base competitive strength (always at least 40 with any features)
    base = 40
    return min(100, max(0, int(base + raw * 0.6)))


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/landscape")
async def competitive_landscape() -> dict[str, Any]:
    """Full competitive landscape overview: all 5 competitors + Dealix positioning."""
    competitors_summary: list[dict[str, Any]] = []
    for comp in _COMPETITORS.values():
        competitors_summary.append(
            {
                "id": comp["id"],
                "name": comp["name"],
                "name_ar": comp["name_ar"],
                "category": comp["category"],
                "category_ar": comp["category_ar"],
                "pricing_sar_range": comp["pricing_sar_range"],
                "strengths_en": comp["strengths_en"],
                "strengths_ar": comp["strengths_ar"],
                "weaknesses_en": comp["weaknesses_en"],
                "weaknesses_ar": comp["weaknesses_ar"],
                "target_segment_en": comp["target_segment_en"],
                "target_segment_ar": comp["target_segment_ar"],
                "dealix_positioning": _build_positioning(comp["id"]),
            }
        )
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_competitors": len(competitors_summary),
        "market_en": "Saudi B2B AI/SaaS market — fictional competitor profiles for internal use only",
        "market_ar": "سوق B2B الذكاء الاصطناعي/SaaS السعودي — ملفات منافسين خيالية للاستخدام الداخلي فقط",
        "dealix_advantages": _DEALIX_ADVANTAGES,
        "competitors": competitors_summary,
    }


@router.get("/battlecards")
async def battlecards() -> dict[str, Any]:
    """Sales battlecard for each competitor: objections + winning responses, bilingual."""
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_battlecards": len(_BATTLECARDS),
        "note_en": "For internal sales use only. Competitor names are fictional.",
        "note_ar": "للاستخدام الداخلي في المبيعات فقط. أسماء المنافسين خيالية.",
        "battlecards": list(_BATTLECARDS.values()),
    }


@router.get("/win-loss-patterns")
async def win_loss_patterns() -> dict[str, Any]:
    """Win/loss data by competitor and sector patterns."""
    total_evaluated = sum(p["deals_evaluated"] for p in _WIN_LOSS_PATTERNS)
    total_won = sum(p["deals_won"] for p in _WIN_LOSS_PATTERNS)
    overall_win_rate = round(total_won / total_evaluated * 100, 1) if total_evaluated else 0

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "summary_en": "Win/loss patterns by competitor — demo data for internal review",
        "summary_ar": "أنماط الربح والخسارة حسب المنافس — بيانات تجريبية للمراجعة الداخلية",
        "overall": {
            "total_deals_evaluated": total_evaluated,
            "total_deals_won": total_won,
            "overall_win_rate_pct": overall_win_rate,
        },
        "patterns": _WIN_LOSS_PATTERNS,
        "note_en": "Data is estimated from internal deal reviews — not statistically verified.",
        "note_ar": "البيانات مقدَّرة من مراجعات صفقات داخلية — غير مُتحقَّق منها إحصائياً.",
    }


@router.get("/{competitor_id}")
async def competitor_detail(competitor_id: str) -> dict[str, Any]:
    """Deep dive on a single competitor: strengths, weaknesses, how to win."""
    if competitor_id not in _COMPETITORS:
        available = list(_COMPETITORS.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Competitor '{competitor_id}' not found. Available: {available}",
        )
    competitor = _COMPETITORS[competitor_id]
    battlecard = _BATTLECARDS.get(competitor_id, {})
    win_loss = next(
        (p for p in _WIN_LOSS_PATTERNS if p["competitor_id"] == competitor_id), {}
    )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "competitor": competitor,
        "positioning": _build_positioning(competitor_id),
        "battlecard": battlecard,
        "win_loss": win_loss,
    }


class CompareRequest(BaseModel):
    our_features: list[str] = Field(
        ...,
        min_length=1,
        description="List of Dealix features to compare",
    )
    competitor_id: str = Field(
        ...,
        description="Competitor ID (alpha_revenue, nexus_ops, dataflow_arabia, riyadh_tech, jadara_saas)",
    )


@router.post("/compare")
async def compare(body: CompareRequest = Body(...)) -> dict[str, Any]:
    """Side-by-side feature comparison: Dealix vs a competitor, with win score."""
    if body.competitor_id not in _COMPETITORS:
        available = list(_COMPETITORS.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Competitor '{body.competitor_id}' not found. Available: {available}",
        )

    competitor = _COMPETITORS[body.competitor_id]
    win_score = _compute_win_score(body.our_features, body.competitor_id)

    # Build side-by-side feature table
    comparison_rows: list[dict[str, Any]] = []
    for feature in body.our_features:
        feature_lower = feature.lower()
        # Check if this feature directly addresses a known weakness
        addresses = [
            w for w in competitor["weaknesses_en"]
            if any(word in w.lower() for word in feature_lower.split())
        ]
        comparison_rows.append(
            {
                "feature": feature,
                "dealix_has": True,
                "competitor_has": False,
                "competitor_weakness_addressed": addresses,
                "advantage_strength": "strong" if addresses else "neutral",
            }
        )

    # Build recommended talking points based on matched weaknesses
    talking_points: list[dict[str, str]] = []
    for adv in _DEALIX_ADVANTAGES:
        feature_lower = " ".join(body.our_features).lower()
        if any(word in adv["en"].lower() for word in feature_lower.split()):
            talking_points.append({"en": adv["en"], "ar": adv["ar"]})

    # Always include at least the top 2 advantages if no direct match
    if not talking_points:
        talking_points = [{"en": a["en"], "ar": a["ar"]} for a in _DEALIX_ADVANTAGES[:2]]

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "competitor_id": body.competitor_id,
        "competitor_name": competitor["name"],
        "competitor_name_ar": competitor["name_ar"],
        "win_score": win_score,
        "win_score_interpretation_en": (
            "High" if win_score >= 70 else "Medium" if win_score >= 50 else "Low"
        ),
        "win_score_interpretation_ar": (
            "مرتفع" if win_score >= 70 else "متوسط" if win_score >= 50 else "منخفض"
        ),
        "comparison": comparison_rows,
        "recommended_talking_points": talking_points,
        "note_en": "Win score is an internal estimate — not a guarantee of deal outcome.",
        "note_ar": "درجة الفوز تقدير داخلي — ليست ضماناً لنتيجة الصفقة.",
    }
