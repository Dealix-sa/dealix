"""Sales Playbook API Router.

ADMIN-GATED. Discovery scripts, objection handling, tier recommendations,
follow-up cadences, and closing checklists for the Saudi B2B AI/SaaS sales process.

IMPORTANT: WhatsApp follow-up steps carry consent_required: true and
approval_required: true. Cold WhatsApp is never used.

Prefix: /api/v1/sales-playbook
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/sales-playbook",
    tags=["sales-playbook"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)

TierLiteral = Literal[
    "free_diagnostic", "sprint", "data_pack", "managed_ops", "custom_ai"
]

# ---------------------------------------------------------------------------
# Discovery call script — 8 stages, bilingual
# ---------------------------------------------------------------------------

_DISCOVERY_SCRIPT: list[dict[str, Any]] = [
    {
        "stage": 1,
        "stage_id": "opener",
        "stage_name_en": "Opener",
        "stage_name_ar": "افتتاح المكالمة",
        "duration_minutes": 2,
        "objective_en": "Build initial credibility and set the agenda.",
        "objective_ar": "بناء مصداقية أولية وتحديد جدول الأعمال.",
        "script_en": (
            "Thank you for making time today. I will keep this to 30 minutes maximum. "
            "My goal is to understand your current operations, share what we have observed "
            "in similar Saudi businesses, and see whether there is a fit worth exploring. "
            "Does that agenda work for you?"
        ),
        "script_ar": (
            "شكراً لتخصيصك وقتاً اليوم. سأحافظ على هذا في حدود 30 دقيقة كحد أقصى. "
            "هدفي هو فهم عملياتك الحالية، ومشاركة ما لاحظناه في أعمال سعودية مماثلة، "
            "ومعرفة ما إذا كان هناك توافق يستحق الاستكشاف. هل هذا الجدول يناسبك؟"
        ),
        "notes_en": "Do not pitch yet. Establish respect and mutual agenda ownership.",
        "notes_ar": "لا تبدأ العرض بعد. أسّس الاحترام وملكية الجدول المشترك.",
    },
    {
        "stage": 2,
        "stage_id": "rapport",
        "stage_name_en": "Rapport",
        "stage_name_ar": "بناء العلاقة",
        "duration_minutes": 4,
        "objective_en": "Establish personal and professional context.",
        "objective_ar": "إنشاء سياق شخصي ومهني.",
        "script_en": (
            "Before we get into the details — how long have you been in this role? "
            "What drew you to this industry? "
            "I ask because the challenges vary a lot depending on where you are in the growth curve."
        ),
        "script_ar": (
            "قبل أن ندخل في التفاصيل — كم المدة التي قضيتها في هذا الدور؟ "
            "ما الذي جذبك إلى هذه الصناعة؟ "
            "أسأل لأن التحديات تختلف كثيراً حسب موقعك في منحنى النمو."
        ),
        "notes_en": "Listen more than you speak. Reference sector knowledge to show credibility.",
        "notes_ar": "استمع أكثر مما تتكلم. ارجع إلى معرفة القطاع لإظهار المصداقية.",
    },
    {
        "stage": 3,
        "stage_id": "pain_discovery",
        "stage_name_en": "Pain Discovery",
        "stage_name_ar": "اكتشاف الألم",
        "duration_minutes": 8,
        "objective_en": "Uncover operational pain points that AI can address.",
        "objective_ar": "كشف نقاط الألم التشغيلي التي يمكن للذكاء الاصطناعي معالجتها.",
        "script_en": (
            "Walk me through a typical week in your operations. "
            "Where does your team spend the most time on manual tasks? "
            "If you could remove one bottleneck tomorrow, what would it be? "
            "What does it cost you — in time, money, or risk — when that bottleneck is not resolved?"
        ),
        "script_ar": (
            "خذني في جولة عبر أسبوع نموذجي في عملياتك. "
            "أين يقضي فريقك معظم الوقت في المهام اليدوية؟ "
            "إذا استطعت إزالة عائق واحد غداً، فما الذي سيكون؟ "
            "ما الكلفة التي تدفعها — في الوقت أو المال أو المخاطر — عندما لا يُحلّ هذا العائق؟"
        ),
        "notes_en": "Use silence. Let the prospect surface pain without prompting. Write down exact words they use.",
        "notes_ar": "استخدم الصمت. دع العميل المحتمل يكشف الألم دون توجيه. دوّن الكلمات الدقيقة التي يستخدمها.",
    },
    {
        "stage": 4,
        "stage_id": "zatca_pdpl_urgency",
        "stage_name_en": "ZATCA/PDPL Urgency",
        "stage_name_ar": "إلحاحية زاتكا/حماية البيانات",
        "duration_minutes": 5,
        "objective_en": "Surface regulatory exposure that creates urgency.",
        "objective_ar": "الكشف عن التعرض التنظيمي الذي يخلق إلحاحاً.",
        "script_en": (
            "Two areas that have been creating urgency for Saudi businesses this year — "
            "ZATCA Phase 2 e-invoicing compliance, and the Personal Data Protection Law. "
            "Where does your current system stand on e-invoicing? "
            "Have you done a data inventory for PDPL purposes? "
            "I ask because our Proof Pack includes documented compliance coverage — "
            "and the cost of non-compliance typically exceeds what we charge in a year."
        ),
        "script_ar": (
            "مجالان يخلقان إلحاحاً للأعمال السعودية هذا العام — "
            "امتثال الفوترة الإلكترونية لزاتكا المرحلة الثانية، ونظام حماية البيانات الشخصية. "
            "أين يقف نظامك الحالي من الفوترة الإلكترونية؟ "
            "هل أجريت جرد بيانات لأغراض نظام PDPL؟ "
            "أسأل لأن حزمة الإثبات لدينا تشمل تغطية الامتثال الموثقة — "
            "وتكلفة عدم الامتثال عادةً تتجاوز ما نتقاضاه في العام."
        ),
        "notes_en": "Present as genuine concern, not fear tactic. Quote regulatory amounts only from public sources.",
        "notes_ar": "قدّم كاهتمام حقيقي، لا كتكتيك تخويف. استشهد بالمبالغ التنظيمية من المصادر العامة فقط.",
    },
    {
        "stage": 5,
        "stage_id": "qualification",
        "stage_name_en": "Qualification",
        "stage_name_ar": "التأهيل",
        "duration_minutes": 4,
        "objective_en": "Confirm budget authority, timeline, and decision process.",
        "objective_ar": "تأكيد سلطة الميزانية والجدول الزمني وعملية القرار.",
        "script_en": (
            "To make sure I give you a relevant proposal — "
            "what is the approved budget range for a project like this? "
            "Who else is involved in making this decision? "
            "What would need to be true for you to move forward within the next 30 days?"
        ),
        "script_ar": (
            "لأتأكد من تقديم عرض ذي صلة — "
            "ما نطاق الميزانية المعتمدة لمشروع كهذا؟ "
            "من آخر متورط في اتخاذ هذا القرار؟ "
            "ما الذي يجب أن يتحقق لتتقدم خلال الـ 30 يوماً القادمة؟"
        ),
        "notes_en": "If they cannot answer budget, qualify with minimum. Confirm decision-maker is on the call.",
        "notes_ar": "إذا لم يستطيعوا الإجابة عن الميزانية، أهّل بالحد الأدنى. تأكد أن صانع القرار على المكالمة.",
    },
    {
        "stage": 6,
        "stage_id": "value_proposition",
        "stage_name_en": "Value Proposition",
        "stage_name_ar": "عرض القيمة",
        "duration_minutes": 4,
        "objective_en": "Connect Dealix capabilities directly to the pain uncovered in stage 3.",
        "objective_ar": "ربط قدرات ديليكس مباشرة بالألم الذي تم الكشف عنه في المرحلة 3.",
        "script_en": (
            "Based on what you have described — the manual bottleneck in [X] "
            "and the ZATCA exposure — here is what we typically deliver in a 2-week Sprint: "
            "automated [X] with an approval workflow, ZATCA-ready data pipeline, "
            "and a Proof Pack at the end showing exactly what changed and by how much. "
            "We do not make projected claims — you see verified outcomes before committing to a retainer."
        ),
        "script_ar": (
            "بناءً على ما وصفته — العائق اليدوي في [X] "
            "والتعرض لزاتكا — إليك ما نقدمه عادةً في Sprint لأسبوعين: "
            "أتمتة [X] مع سير عمل للموافقة، وخط بيانات جاهز لزاتكا، "
            "وحزمة إثبات في النهاية تُظهر بالضبط ما الذي تغير وبأي مقدار. "
            "لا نقدم ادعاءات متوقعة — ترى نتائج موثقة قبل الالتزام بعقد."
        ),
        "notes_en": (
            "Reference the specific pain they named. Never promise ROI percentages. "
            "Use Proof Pack as the differentiator."
        ),
        "notes_ar": (
            "ارجع إلى الألم المحدد الذي ذكروه. لا تعد بنسب عائد استثمار. "
            "استخدم حزمة الإثبات كعنصر تمييز."
        ),
    },
    {
        "stage": 7,
        "stage_id": "objection_handling",
        "stage_name_en": "Objection Handling",
        "stage_name_ar": "معالجة الاعتراضات",
        "duration_minutes": 5,
        "objective_en": "Neutralize the top 2–3 objections that surface at this point.",
        "objective_ar": "تحييد أكبر 2–3 اعتراضات تظهر في هذه النقطة.",
        "script_en": (
            "What concerns do you have about moving forward? "
            "[Listen and reflect back before answering.] "
            "That is a common concern — here is how other [sector] clients handled it: [evidence]."
        ),
        "script_ar": (
            "ما هي مخاوفك بشأن المضي قدماً؟ "
            "[استمع وعكس ما سمعته قبل الإجابة.] "
            "هذا قلق شائع — إليك كيف تعامل معه عملاء [القطاع] الآخرون: [الدليل]."
        ),
        "notes_en": "See /objections endpoint for the full objection database with winning responses.",
        "notes_ar": "راجع نقطة النهاية /objections للحصول على قاعدة بيانات الاعتراضات الكاملة مع الردود الفائزة.",
    },
    {
        "stage": 8,
        "stage_id": "next_step",
        "stage_name_en": "Next Step",
        "stage_name_ar": "الخطوة التالية",
        "duration_minutes": 3,
        "objective_en": "Close on a specific, time-bound next action.",
        "objective_ar": "الإغلاق على إجراء تالٍ محدد ومقيّد بوقت.",
        "script_en": (
            "Based on what we covered, the logical next step is a free diagnostic — "
            "takes 60 minutes, gives you a ZATCA/PDPL gap report, and no commitment required. "
            "Can we schedule that for this week or early next week?"
        ),
        "script_ar": (
            "بناءً على ما غطيناه، الخطوة التالية المنطقية هي تشخيص مجاني — "
            "تستغرق 60 دقيقة، وتمنحك تقرير الفجوات لزاتكا/PDPL، ولا يُشترط الالتزام. "
            "هل يمكننا جدولة ذلك هذا الأسبوع أو مطلع الأسبوع القادم؟"
        ),
        "notes_en": "Always propose a specific date and time. Do not leave next step open-ended.",
        "notes_ar": "اقترح دائماً تاريخاً ووقتاً محددين. لا تترك الخطوة التالية مفتوحة.",
    },
]

# ---------------------------------------------------------------------------
# Objections database — 15 objections + responses, bilingual
# ---------------------------------------------------------------------------

_OBJECTIONS: list[dict[str, Any]] = [
    {
        "id": "obj_001",
        "stage": "qualification",
        "objection_en": "We do not have budget approved right now.",
        "objection_ar": "ليس لدينا ميزانية معتمدة الآن.",
        "response_en": (
            "Our free diagnostic requires no budget — it surfaces the compliance gaps "
            "and gives you the business case to get budget approved. "
            "Most clients get internal approval within 2 weeks of seeing the gap report."
        ),
        "response_ar": (
            "تشخيصنا المجاني لا يتطلب ميزانية — يكشف فجوات الامتثال "
            "ويمنحك مبرر الأعمال للحصول على الموافقة على الميزانية. "
            "معظم العملاء يحصلون على الموافقة الداخلية خلال أسبوعين من رؤية تقرير الفجوات."
        ),
    },
    {
        "id": "obj_002",
        "stage": "qualification",
        "objection_en": "We need to involve our IT team before deciding.",
        "objection_ar": "نحتاج إلى إشراك فريق تقنية المعلومات قبل اتخاذ القرار.",
        "response_en": (
            "Absolutely. Can we set up a 30-minute technical session this week "
            "where both you and your IT lead can review the integration approach? "
            "Our architecture is API-first and does not require infrastructure changes."
        ),
        "response_ar": (
            "بالتأكيد. هل يمكننا تحديد جلسة تقنية لمدة 30 دقيقة هذا الأسبوع "
            "حيث يمكن لك ولمسؤول التقنية مراجعة نهج التكامل؟ "
            "بنيتنا التحتية تعتمد API أولاً ولا تتطلب تغييرات في البنية التحتية."
        ),
    },
    {
        "id": "obj_003",
        "stage": "value_proposition",
        "objection_en": "We already tried an AI tool and it did not work.",
        "objection_ar": "جربنا بالفعل أداة ذكاء اصطناعي ولم تنجح.",
        "response_en": (
            "That experience is common and valid. Most AI tools execute without a governance layer — "
            "they act before humans approve. "
            "Dealix runs every AI recommendation through an approval workflow. "
            "Nothing changes in your business without a human sign-off."
        ),
        "response_ar": (
            "هذه التجربة شائعة ومفهومة. معظم أدوات الذكاء الاصطناعي تنفذ بدون طبقة حوكمة — "
            "تتصرف قبل موافقة الإنسان. "
            "ديليكس يمرر كل توصية ذكاء اصطناعي عبر سير عمل الموافقة. "
            "لا شيء يتغير في عملك دون موافقة بشرية."
        ),
    },
    {
        "id": "obj_004",
        "stage": "value_proposition",
        "objection_en": "How do we know your results are real?",
        "objection_ar": "كيف نعرف أن نتائجك حقيقية؟",
        "response_en": (
            "You do not have to take our word for it. "
            "Every Sprint pilot ends with a Proof Pack — a documented report showing exactly "
            "what inputs were used, what actions were taken, and what measurable change occurred. "
            "We do not show you projections; we show you evidence."
        ),
        "response_ar": (
            "لا يجب أن تأخذ كلامنا على محمل الثقة. "
            "كل تجربة Sprint تنتهي بحزمة إثبات — تقرير موثق يُظهر بالضبط "
            "ما المدخلات المستخدمة، وما الإجراءات المتخذة، وما التغيير القابل للقياس الذي حدث. "
            "لا نُريك توقعات؛ نُريك أدلة."
        ),
    },
    {
        "id": "obj_005",
        "stage": "next_step",
        "objection_en": "We are too busy right now — call us in three months.",
        "objection_ar": "نحن مشغولون جداً الآن — اتصل بنا بعد ثلاثة أشهر.",
        "response_en": (
            "Understood. The businesses that are too busy are usually the ones "
            "with the highest bottleneck cost. "
            "Let me send you a one-page ZATCA gap checklist you can complete in 10 minutes — "
            "it will tell you whether the 3-month delay has a compliance cost attached."
        ),
        "response_ar": (
            "مفهوم. الأعمال المشغولة جداً عادةً هي التي تحمل أعلى تكلفة للعوائق. "
            "دعني أرسل لك قائمة تحقق فجوات زاتكا في صفحة واحدة يمكنك إكمالها في 10 دقائق — "
            "ستخبرك ما إذا كان التأخير لثلاثة أشهر يحمل تكلفة امتثال مرتبطة."
        ),
    },
    {
        "id": "obj_006",
        "stage": "qualification",
        "objection_en": "We are happy with our current vendor.",
        "objection_ar": "نحن راضون عن مزودنا الحالي.",
        "response_en": (
            "Good to hear. Two quick questions: Does your current vendor give you "
            "ZATCA Phase 2 certified e-invoicing? "
            "And does it handle PDPL consent workflows? "
            "If both answers are yes, there is no reason to talk further."
        ),
        "response_ar": (
            "سعيد بسماع ذلك. سؤالان سريعان: هل يمنحك مزودك الحالي "
            "فوترة إلكترونية معتمدة لزاتكا المرحلة الثانية؟ "
            "وهل يتعامل مع سير عمل موافقة PDPL؟ "
            "إذا كانت كلتا الإجابتين نعم، فلا داعي للاستمرار في الحديث."
        ),
    },
    {
        "id": "obj_007",
        "stage": "value_proposition",
        "objection_en": "Your product is too complex for our team.",
        "objection_ar": "منتجك معقد جداً لفريقنا.",
        "response_en": (
            "The governance layer actually makes it simpler — your team only sees "
            "the decisions that require their approval, in Arabic. "
            "The AI handles the complexity underneath; your team handles the judgment calls on top."
        ),
        "response_ar": (
            "طبقة الحوكمة في الواقع تجعله أبسط — فريقك يرى فقط "
            "القرارات التي تتطلب موافقتهم، باللغة العربية. "
            "الذكاء الاصطناعي يتعامل مع التعقيد في الخلفية؛ فريقك يتعامل مع قرارات الحكم فوقه."
        ),
    },
    {
        "id": "obj_008",
        "stage": "qualification",
        "objection_en": "We need to see a full demo first.",
        "objection_ar": "نحتاج أولاً إلى رؤية عرض توضيحي كامل.",
        "response_en": (
            "Absolutely — our free diagnostic is a live working session, not a slideshow. "
            "We use your actual data (anonymized if needed) to show you the gap analysis in real time. "
            "Can we schedule that for this week?"
        ),
        "response_ar": (
            "بالتأكيد — تشخيصنا المجاني هو جلسة عمل مباشرة، لا عرض شرائح. "
            "نستخدم بياناتك الفعلية (مجهولة الهوية إذا لزم) لنُريك تحليل الفجوات في الوقت الفعلي. "
            "هل يمكننا جدولة ذلك هذا الأسبوع؟"
        ),
    },
    {
        "id": "obj_009",
        "stage": "value_proposition",
        "objection_en": "We do not trust AI to make business decisions.",
        "objection_ar": "لا نثق بالذكاء الاصطناعي لاتخاذ قرارات الأعمال.",
        "response_en": (
            "That is exactly why Dealix uses an APPROVAL_FIRST model. "
            "The AI never makes a decision on its own — it generates recommendations "
            "that your team approves or rejects. You stay in control."
        ),
        "response_ar": (
            "هذا هو بالضبط لماذا يستخدم ديليكس نموذج الموافقة أولاً. "
            "الذكاء الاصطناعي لا يتخذ قراراً بمفرده أبداً — يُنشئ توصيات "
            "يوافق عليها أو يرفضها فريقك. تبقى أنت في التحكم."
        ),
    },
    {
        "id": "obj_010",
        "stage": "next_step",
        "objection_en": "Send me an email with the pricing.",
        "objection_ar": "أرسل لي بريداً إلكترونياً مع التسعير.",
        "response_en": (
            "I can do that — and pricing without context rarely makes sense. "
            "Let me include the free diagnostic offer so you can see the custom fit "
            "before a number means anything. Does that work?"
        ),
        "response_ar": (
            "يمكنني فعل ذلك — والتسعير بدون سياق نادراً ما يكون منطقياً. "
            "دعني أشمل عرض التشخيص المجاني حتى تتمكن من رؤية التوافق المخصص "
            "قبل أن يعني أي رقم شيئاً. هل هذا مناسب؟"
        ),
    },
    {
        "id": "obj_011",
        "stage": "opener",
        "objection_en": "I only have 10 minutes.",
        "objection_ar": "لدي 10 دقائق فقط.",
        "response_en": (
            "Ten minutes is enough. I will ask you two questions about ZATCA and PDPL exposure. "
            "If there is no fit, I will tell you in 5 minutes and we both save time."
        ),
        "response_ar": (
            "عشر دقائق كافية. سأسألك سؤالين عن تعرض زاتكا و PDPL. "
            "إذا لم يكن هناك توافق، سأخبرك في 5 دقائق ونوفر الوقت معاً."
        ),
    },
    {
        "id": "obj_012",
        "stage": "value_proposition",
        "objection_en": "We can build this in-house.",
        "objection_ar": "يمكننا بناء هذا داخلياً.",
        "response_en": (
            "Possibly. In-house AI with a governance layer, ZATCA integration, and PDPL compliance "
            "typically takes 8–14 months and a 3–5 person engineering team. "
            "Our Sprint delivers a verified proof of concept in 2 weeks. "
            "How does your in-house timeline compare?"
        ),
        "response_ar": (
            "ربما. الذكاء الاصطناعي الداخلي مع طبقة حوكمة وتكامل زاتكا وامتثال PDPL "
            "يستغرق عادةً 8–14 شهراً وفريق هندسة مكوّن من 3–5 أشخاص. "
            "Sprint لدينا يقدم دليل مفهوم موثق في أسبوعين. "
            "كيف يقارن الجدول الزمني الداخلي لديك؟"
        ),
    },
    {
        "id": "obj_013",
        "stage": "zatca_pdpl_urgency",
        "objection_en": "We are already ZATCA compliant.",
        "objection_ar": "نحن ممتثلون بالفعل لزاتكا.",
        "response_en": (
            "Phase 1 or Phase 2? Phase 2 requires real-time B2B e-invoicing integration "
            "with the ZATCA platform. Many businesses that passed Phase 1 "
            "are not yet integrated for Phase 2. Our free diagnostic verifies current status."
        ),
        "response_ar": (
            "المرحلة الأولى أم الثانية؟ المرحلة الثانية تتطلب تكامل الفوترة الإلكترونية B2B "
            "في الوقت الفعلي مع منصة زاتكا. كثير من الأعمال التي اجتازت المرحلة الأولى "
            "لم تتكامل بعد للمرحلة الثانية. تشخيصنا المجاني يتحقق من الحالة الحالية."
        ),
    },
    {
        "id": "obj_014",
        "stage": "zatca_pdpl_urgency",
        "objection_en": "PDPL does not apply to us — we are a B2B company.",
        "objection_ar": "PDPL لا ينطبق علينا — نحن شركة B2B.",
        "response_en": (
            "PDPL applies to any organization that processes personal data of Saudi residents — "
            "including employee records, HR systems, and supplier contacts. "
            "B2B companies are not exempt. Our diagnostic identifies which data assets need governance."
        ),
        "response_ar": (
            "PDPL ينطبق على أي منظمة تعالج البيانات الشخصية للمقيمين السعوديين — "
            "بما في ذلك سجلات الموظفين وأنظمة الموارد البشرية وجهات اتصال الموردين. "
            "الشركات B2B ليست معفاة. تشخيصنا يحدد أصول البيانات التي تحتاج حوكمة."
        ),
    },
    {
        "id": "obj_015",
        "stage": "next_step",
        "objection_en": "We will think about it and get back to you.",
        "objection_ar": "سنفكر في الأمر ونتواصل معك.",
        "response_en": (
            "Of course. Before we close — is there a specific concern that is making you hesitate? "
            "I would rather address it now than lose a month to email chains. "
            "And if it genuinely is not a fit, I would appreciate knowing now."
        ),
        "response_ar": (
            "بالطبع. قبل أن ننتهي — هل هناك مخاوف محددة تجعلك مترددًا؟ "
            "أفضل معالجتها الآن على أن نخسر شهراً في سلاسل بريد إلكتروني. "
            "وإذا لم يكن هناك توافق حقاً، فأقدّر معرفة ذلك الآن."
        ),
    },
]

# ---------------------------------------------------------------------------
# Follow-up cadence
# ---------------------------------------------------------------------------

_FOLLOW_UP_CADENCE: list[dict[str, Any]] = [
    {
        "day": 1,
        "step": "post_call_summary",
        "channel": "email",
        "approval_required": False,
        "consent_required": False,
        "template_en": (
            "Subject: Your ZATCA/PDPL Gap Summary — as discussed\n\n"
            "Thank you for the conversation today. "
            "As promised, attached is the gap summary for your review. "
            "The free diagnostic slot is available this week and next — "
            "reply to confirm a time that works."
        ),
        "template_ar": (
            "الموضوع: ملخص فجوات زاتكا/PDPL — كما نوقش\n\n"
            "شكراً على المحادثة اليوم. "
            "كما وعدت، مرفق ملخص الفجوات لمراجعتك. "
            "موعد التشخيص المجاني متاح هذا الأسبوع والأسبوع القادم — "
            "ردّ لتأكيد وقت مناسب."
        ),
    },
    {
        "day": 3,
        "step": "value_add_touchpoint",
        "channel": "email",
        "approval_required": False,
        "consent_required": False,
        "template_en": (
            "Subject: One data point on ZATCA Phase 2 deadlines\n\n"
            "Quick note — the ZATCA Phase 2 rollout schedule affects your sector "
            "in [Quarter X]. Wanted to make sure you had this before the diagnostic. "
            "Let me know if you have questions before we meet."
        ),
        "template_ar": (
            "الموضوع: نقطة بيانات واحدة حول مواعيد زاتكا المرحلة الثانية\n\n"
            "ملاحظة سريعة — جدول طرح زاتكا المرحلة الثانية يؤثر على قطاعك "
            "في [الربع X]. أردت التأكد من حصولك على هذه المعلومة قبل التشخيص. "
            "أخبرني إذا كانت لديك أسئلة قبل لقاءنا."
        ),
    },
    {
        "day": 7,
        "step": "diagnostic_reminder",
        "channel": "email",
        "approval_required": True,
        "consent_required": False,
        "template_en": (
            "Subject: Free diagnostic — still open this week\n\n"
            "Following up on the diagnostic offer. "
            "A 60-minute session produces a gap report that most clients use "
            "to get internal budget approval within 2 weeks. "
            "Two slots remaining this week — happy to reserve one."
        ),
        "template_ar": (
            "الموضوع: التشخيص المجاني — لا يزال متاحاً هذا الأسبوع\n\n"
            "متابعة لعرض التشخيص. "
            "جلسة مدتها 60 دقيقة تُنتج تقرير فجوات يستخدمه معظم العملاء "
            "للحصول على الموافقة الداخلية على الميزانية خلال أسبوعين. "
            "موعدان متبقيان هذا الأسبوع — يسعدني حجز أحدهما."
        ),
    },
    {
        "day": 14,
        "step": "whatsapp_consent_followup",
        "channel": "whatsapp",
        "approval_required": True,
        "consent_required": True,
        "template_en": (
            "[CONSENT REQUIRED before sending — verify opt-in record] "
            "Hi [Name], following up on the Dealix diagnostic we discussed. "
            "Happy to answer questions by voice call or message — just let me know what works best."
        ),
        "template_ar": (
            "[الموافقة مطلوبة قبل الإرسال — تحقق من سجل الاشتراك] "
            "مرحباً [الاسم]، أتابع التشخيص الذي ناقشناه مع ديليكس. "
            "يسعدني الإجابة على الأسئلة بمكالمة صوتية أو رسالة — أخبرني ما يناسبك أكثر."
        ),
        "governance_note_en": "WhatsApp message must only be sent to contacts who have explicitly opted in. Approval required.",
        "governance_note_ar": "رسالة واتساب يجب إرسالها فقط إلى جهات الاتصال التي وافقت صراحةً. الموافقة مطلوبة.",
    },
    {
        "day": 30,
        "step": "final_check_in",
        "channel": "email",
        "approval_required": False,
        "consent_required": False,
        "template_en": (
            "Subject: Checking in — any change in priorities?\n\n"
            "It has been about a month since we spoke. "
            "Saudi regulatory timelines move fast — wanted to check whether "
            "ZATCA or PDPL has moved up your priority list. "
            "If the timing still is not right, no pressure — happy to reconnect when it is."
        ),
        "template_ar": (
            "الموضوع: التحقق — هل هناك تغيير في الأولويات؟\n\n"
            "مضى حوالي شهر منذ تحدثنا. "
            "الجداول التنظيمية السعودية تتحرك بسرعة — أردت التحقق مما إذا كانت "
            "زاتكا أو PDPL قد تقدمت في قائمة أولوياتك. "
            "إذا لم يكن التوقيت مناسباً بعد، لا ضغط — يسعدني التواصل عندما يكون مناسباً."
        ),
    },
]

# ---------------------------------------------------------------------------
# Closing checklist — 10 items
# ---------------------------------------------------------------------------

_CLOSING_CHECKLIST: list[dict[str, Any]] = [
    {
        "item_id": "CLOSE-001",
        "item": 1,
        "id": "icp_score_confirmed",
        "item_ar": "تأكيد أن درجة ICP لا تقل عن 55",
        "item_en": "ICP score >= 55 confirmed",
        "gate_en": "ICP score >= 55 confirmed before issuing proposal.",
        "gate_ar": "تأكيد أن درجة ICP لا تقل عن 55 قبل إصدار العرض.",
        "critical": True,
        "required": True,
    },
    {
        "item_id": "CLOSE-002",
        "item": 2,
        "id": "decision_maker_confirmed",
        "item_ar": "تحديد صانع القرار وتأكيد صلاحياته",
        "item_en": "Decision maker identified and authority confirmed",
        "gate_en": "Confirmed that the contract signatory is the same person who attended the proposal.",
        "gate_ar": "تأكيد أن موقّع العقد هو نفس الشخص الذي حضر العرض.",
        "critical": True,
        "required": True,
    },
    {
        "item_id": "CLOSE-003",
        "item": 3,
        "id": "budget_confirmed",
        "item_ar": "تأكيد وجود ميزانية مخصصة أو موافقة مبدئية",
        "item_en": "Budget confirmed or preliminary approval obtained",
        "gate_en": "Budget approved and procurement channel identified (direct / purchase order).",
        "gate_ar": "الميزانية معتمدة وتم تحديد قناة الشراء (مباشر / أمر شراء).",
        "critical": True,
        "required": True,
    },
    {
        "item_id": "CLOSE-004",
        "item": 4,
        "id": "zatca_pdpl_context_shared",
        "item_ar": "مشاركة سياق ZATCA أو PDPL ذي الصلة مع العميل",
        "item_en": "Relevant ZATCA / PDPL context shared with prospect",
        "gate_en": "ZATCA scope documented and PDPL data inventory reviewed with client.",
        "gate_ar": "نطاق زاتكا موثق وجرد بيانات PDPL تمت مراجعته مع العميل.",
        "critical": False,
        "required": False,
    },
    {
        "item_id": "CLOSE-005",
        "item": 5,
        "id": "proof_pack_complete",
        "item_ar": "حزمة الإثبات (Proof Pack) جاهزة ومراجعة",
        "item_en": "Proof Pack ready and reviewed",
        "gate_en": "Proof Pack generated and reviewed with client — all 14 sections populated.",
        "gate_ar": "حزمة الإثبات تم إنشاؤها ومراجعتها مع العميل — جميع الـ 14 قسماً مكتملة.",
        "critical": True,
        "required": True,
    },
    {
        "item_id": "CLOSE-006",
        "item": 6,
        "id": "proposal_founder_approved",
        "item_ar": "العرض التجاري راجعه المؤسس قبل الإرسال (APPROVAL_FIRST)",
        "item_en": "Proposal reviewed by founder before sending (APPROVAL_FIRST)",
        "gate_en": "Proposal reviewed by founder before sending — no exceptions.",
        "gate_ar": "العرض مراجعه المؤسس قبل الإرسال — لا استثناءات.",
        "critical": True,
        "required": True,
    },
    {
        "item_id": "CLOSE-007",
        "item": 7,
        "id": "timeline_agreed",
        "item_ar": "الجدول الزمني للتنفيذ متفق عليه مع العميل",
        "item_en": "Implementation timeline agreed with prospect",
        "gate_en": "Onboarding start date confirmed and added to contract.",
        "gate_ar": "تاريخ بدء التعريف مؤكد ومضاف إلى العقد.",
        "critical": False,
        "required": False,
    },
    {
        "item_id": "CLOSE-008",
        "item": 8,
        "id": "payment_method_confirmed",
        "item_ar": "طريقة الدفع مؤكدة (تحويل بنكي أو بطاقة أو فاتورة)",
        "item_en": "Payment method confirmed (bank transfer, card, or invoice)",
        "gate_en": "Payment method confirmed before contract is issued.",
        "gate_ar": "طريقة الدفع مؤكدة قبل إصدار العقد.",
        "critical": True,
        "required": True,
    },
    {
        "item_id": "CLOSE-009",
        "item": 9,
        "id": "contract_draft_ready",
        "item_ar": "مسودة العقد جاهزة للمراجعة القانونية",
        "item_en": "Contract draft ready for legal review",
        "gate_en": "Contract draft reviewed for guaranteed-outcome language — none present.",
        "gate_ar": "مسودة العقد مراجعة للتأكد من غياب أي لغة نتائج مضمونة.",
        "critical": False,
        "required": False,
    },
    {
        "item_id": "CLOSE-010",
        "item": 10,
        "id": "no_outstanding_objections",
        "item_ar": "لا توجد اعتراضات مفتوحة غير معالجة",
        "item_en": "No outstanding unaddressed objections",
        "gate_en": "All objections logged and addressed — no open blockers.",
        "gate_ar": "جميع الاعتراضات موثقة ومعالجة — لا عوائق مفتوحة.",
        "critical": True,
        "required": True,
    },
]

# ---------------------------------------------------------------------------
# Tier recommendation logic (pure function)
# ---------------------------------------------------------------------------


def recommend_tier(
    icp_score: int,
    zatca_urgency: bool,
    pdpl_urgency: bool,
    company_size: int,
    annual_revenue_sar: float,
) -> dict[str, Any]:
    """
    Recommend the appropriate Dealix tier given qualifying signals.

    Tier ladder:
      free_diagnostic  — always available entry point
      sprint           — quick-win pilot (2 weeks, single use case)
      data_pack        — data governance + analytics layer
      managed_ops      — ongoing AI-driven operations management
      custom_ai        — bespoke enterprise AI development
    """
    urgency_boost = (10 if zatca_urgency else 0) + (10 if pdpl_urgency else 0)
    adjusted_score = min(100, icp_score + urgency_boost)

    if adjusted_score < 30 or annual_revenue_sar < 500_000:
        tier: TierLiteral = "free_diagnostic"
        close_days = 14
        reasoning_en = (
            "ICP score is below threshold for a paid engagement. "
            "Free diagnostic will surface whether a fit exists."
        )
        reasoning_ar = (
            "درجة ICP أقل من الحد للمشاركة المدفوعة. "
            "التشخيص المجاني سيكشف ما إذا كان هناك توافق."
        )
    elif adjusted_score < 50 or annual_revenue_sar < 2_000_000:
        tier = "sprint"
        close_days = 21
        reasoning_en = (
            "Moderate fit — Sprint pilot de-risks the engagement and produces "
            "verifiable proof before a full retainer commitment."
        )
        reasoning_ar = (
            "توافق معتدل — تجربة Sprint تقلل مخاطر الانخراط وتُنتج "
            "إثباتاً قابلاً للتحقق قبل الالتزام بعقد كامل."
        )
    elif adjusted_score < 65 or annual_revenue_sar < 5_000_000:
        tier = "data_pack"
        close_days = 28
        reasoning_en = (
            "Data governance gap detected. Data Pack addresses PDPL inventory, "
            "ZATCA data pipeline, and baseline analytics."
        )
        reasoning_ar = (
            "تم اكتشاف فجوة حوكمة البيانات. حزمة البيانات تعالج جرد PDPL، "
            "وخط بيانات زاتكا، والتحليلات الأساسية."
        )
    elif adjusted_score < 80 or company_size < 50:
        tier = "managed_ops"
        close_days = 35
        reasoning_en = (
            "Strong ICP fit with urgency signals. Managed Ops delivers ongoing "
            "AI-driven operations with monthly Proof Pack reporting."
        )
        reasoning_ar = (
            "توافق ICP قوي مع إشارات إلحاح. العمليات المُدارة تقدم عمليات "
            "مستمرة مدفوعة بالذكاء الاصطناعي مع تقارير حزمة الإثبات الشهرية."
        )
    else:
        tier = "custom_ai"
        close_days = 45
        reasoning_en = (
            "High ICP score, enterprise revenue, and regulatory urgency. "
            "Custom AI build warranted — bespoke governance architecture."
        )
        reasoning_ar = (
            "درجة ICP عالية، إيرادات مؤسسية، وإلحاح تنظيمي. "
            "بناء ذكاء اصطناعي مخصص مبرر — هندسة حوكمة بمواصفات خاصة."
        )

    tier_labels: dict[str, dict[str, str]] = {
        "free_diagnostic": {"en": "Free Diagnostic", "ar": "التشخيص المجاني"},
        "sprint": {"en": "Sprint (2-week pilot)", "ar": "Sprint (تجربة أسبوعين)"},
        "data_pack": {"en": "Data Pack", "ar": "حزمة البيانات"},
        "managed_ops": {"en": "Managed Ops", "ar": "العمليات المُدارة"},
        "custom_ai": {"en": "Custom AI", "ar": "الذكاء الاصطناعي المخصص"},
    }

    return {
        "recommended_tier": tier,
        "tier_label": tier_labels[tier],
        "reasoning_en": reasoning_en,
        "reasoning_ar": reasoning_ar,
        "expected_close_days": close_days,
        "adjusted_icp_score": adjusted_score,
        "urgency_flags": {
            "zatca": zatca_urgency,
            "pdpl": pdpl_urgency,
        },
    }


# ---------------------------------------------------------------------------
# Pydantic request model
# ---------------------------------------------------------------------------


class TierRecommendationRequest(BaseModel):
    icp_score: int = Field(..., ge=0, le=100, description="ICP qualification score 0–100")
    zatca_urgency: bool = Field(default=False, description="Client has a ZATCA compliance deadline")
    pdpl_urgency: bool = Field(default=False, description="Client has a PDPL compliance exposure")
    company_size: int = Field(..., ge=1, description="Number of employees")
    annual_revenue_sar: float = Field(..., ge=0.0, description="Annual revenue in SAR")


# Spec-canonical alias — imported by tests and external callers.
class RecommendTierBody(BaseModel):
    """Pydantic model matching the 90-day commercial plan spec."""

    icp_score: int = Field(default=50, ge=0, le=100)
    zatca_urgency: bool = False
    pdpl_urgency: bool = False
    company_size: int = Field(default=50, ge=1)
    annual_revenue_sar: float = Field(default=5_000_000, ge=0)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/discovery-script")
async def discovery_script() -> dict[str, Any]:
    """Full bilingual discovery call script, 8 stages."""
    total_duration = sum(s["duration_minutes"] for s in _DISCOVERY_SCRIPT)
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_stages": len(_DISCOVERY_SCRIPT),
        "total_duration_minutes": total_duration,
        "stages": _DISCOVERY_SCRIPT,
        "note_en": "Script is a guide — adapt to the specific prospect and conversation.",
        "note_ar": "النص دليل — كيّفه للعميل المحتمل والمحادثة المحددة.",
    }


@router.get("/objections")
async def objections(
    stage: str | None = Query(
        default=None,
        description="Filter by stage: opener, rapport, pain_discovery, zatca_pdpl_urgency, qualification, value_proposition, objection_handling, next_step",
    ),
) -> dict[str, Any]:
    """All 15 objections with winning responses. Filter by ?stage= query param."""
    filtered = _OBJECTIONS
    if stage:
        filtered = [o for o in _OBJECTIONS if o.get("stage") == stage]
        if not filtered:
            available_stages = sorted({o["stage"] for o in _OBJECTIONS})
            from fastapi import HTTPException
            raise HTTPException(
                status_code=404,
                detail=f"No objections found for stage '{stage}'. Available: {available_stages}",
            )
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total": len(filtered),
        "stage_filter": stage,
        "objections": filtered,
        "note_en": "Winning responses are guides — personalize to the prospect's exact words.",
        "note_ar": "الردود الفائزة هي أدلة — خصّصها وفق الكلمات الدقيقة للعميل المحتمل.",
    }


@router.post("/recommend-tier")
async def recommend_tier_endpoint(body: RecommendTierBody) -> dict[str, Any]:
    """Recommend the appropriate service tier based on ICP score and urgency signals."""
    recommendation = recommend_tier(
        icp_score=body.icp_score,
        zatca_urgency=body.zatca_urgency,
        pdpl_urgency=body.pdpl_urgency,
        company_size=body.company_size,
        annual_revenue_sar=body.annual_revenue_sar,
    )
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        **recommendation,
        "note_en": "Tier recommendation is a guide — founder review required before proposal is sent.",
        "note_ar": "توصية المستوى هي دليل — مراجعة المؤسس مطلوبة قبل إرسال العرض.",
    }


@router.get("/follow-up-cadence")
async def follow_up_cadence() -> dict[str, Any]:
    """Complete follow-up sequence: day, channel, template (AR + EN), approval flags."""
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_steps": len(_FOLLOW_UP_CADENCE),
        "whatsapp_policy_en": (
            "WhatsApp messages are only permitted for contacts with documented opt-in consent. "
            "Cold WhatsApp is never used. All WhatsApp steps carry approval_required: true."
        ),
        "whatsapp_policy_ar": (
            "رسائل واتساب مسموح بها فقط للجهات التي لديها موافقة موثقة على الاشتراك. "
            "واتساب الباردة لا تُستخدم أبداً. جميع خطوات واتساب تحمل approval_required: true."
        ),
        "cadence": _FOLLOW_UP_CADENCE,
    }


@router.get("/closing-checklist")
async def closing_checklist() -> dict[str, Any]:
    """Pre-close checklist: 10 gates that must be verified before sending the contract."""
    critical_count = sum(1 for item in _CLOSING_CHECKLIST if item["critical"])
    required_count = sum(1 for item in _CLOSING_CHECKLIST if item["required"])
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_items": len(_CLOSING_CHECKLIST),
        "critical_items": critical_count,
        "required_items": required_count,
        "optional_items": len(_CLOSING_CHECKLIST) - required_count,
        "instruction_en": (
            "All required gates must be verified before the contract is sent to the client. "
            "No exceptions."
        ),
        "instruction_ar": (
            "يجب التحقق من جميع البوابات المطلوبة قبل إرسال العقد للعميل. "
            "لا استثناءات."
        ),
        "checklist": _CLOSING_CHECKLIST,
    }
