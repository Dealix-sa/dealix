"""Persuasion & Conviction Engine — evidence-based sales persuasion sequences.

Builds deterministic persuasion chains from pain signals and ICP tier.
No LLM required — all logic is template-driven and auditable.
Hard rule: no fabricated metrics or outcomes — all conviction steps
reference only documented pain signals provided by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PainType(StrEnum):
    REVENUE_LEAK = "revenue_leak"               # Losing deals/revenue due to follow-up gaps
    DATA_CHAOS = "data_chaos"                   # Inconsistent, untrustworthy data
    PROOF_GAP = "proof_gap"                     # Can't prove value to clients/stakeholders
    GOVERNANCE_ABSENCE = "governance_absence"   # No approval/oversight process
    FOLLOW_UP_FAILURE = "follow_up_failure"     # Leads not followed up systematically
    AI_WITHOUT_CONTROL = "ai_without_control"   # Running AI tools without guardrails
    REPORTING_VACUUM = "reporting_vacuum"       # No reliable reporting post-campaign


class ObjectionType(StrEnum):
    PRICE = "price"
    TIMING = "timing"
    TRUST = "trust"
    COMPLEXITY = "complexity"
    INTERNAL_SOLUTION = "internal_solution"
    COMPETITOR = "competitor"
    NOT_PRIORITY = "not_priority"


@dataclass(frozen=True, slots=True)
class PainSignal:
    pain_type: PainType
    severity: int               # 0-100
    cost_estimate_sar: int      # Monthly revenue/cost impact estimate
    frequency: str              # daily / weekly / monthly / quarterly


@dataclass(frozen=True, slots=True)
class ObjectionResponse:
    objection_type: ObjectionType
    objection_ar: str
    objection_en: str
    response_ar: str
    response_en: str
    evidence_anchor_ar: str     # What proof to reference
    evidence_anchor_en: str
    reframe_question_ar: str    # Socratic reframe question
    reframe_question_en: str


@dataclass(frozen=True, slots=True)
class ConvictionStep:
    step_number: int
    step_type: str              # pain_probe / proof_anchor / roi_reveal / decision_prompt
    question_ar: str
    question_en: str
    purpose_ar: str
    purpose_en: str


@dataclass(frozen=True, slots=True)
class PersuasionChain:
    icp_tier: str
    pain_signals: tuple[PainSignal, ...]
    conviction_sequence: tuple[ConvictionStep, ...]
    objection_responses: tuple[ObjectionResponse, ...]
    closing_questions_ar: tuple[str, ...]
    closing_questions_en: tuple[str, ...]
    evidence_anchors: tuple[str, ...]
    total_pain_cost_sar_monthly: int


# ─────────────────────────────────────────────────────────────────────────────
# Objection registry
# ─────────────────────────────────────────────────────────────────────────────

_OBJECTION_REGISTRY: dict[ObjectionType, ObjectionResponse] = {
    ObjectionType.PRICE: ObjectionResponse(
        objection_type=ObjectionType.PRICE,
        objection_ar="السعر عالٍ",
        objection_en="The price is too high",
        response_ar=(
            "نفهم هذا. سؤال: كم تخسرون شهرياً من leads تضيع بلا متابعة موثّقة؟ "
            "الـ 499 ر.س يكشف لكم بالأرقام ما يضيع — وإذا ما وجدنا شيئاً، تعرفون أنتم أكثر مني."
        ),
        response_en=(
            "We understand. Question: how much are you losing monthly from leads falling through "
            "without documented follow-up? The 499 SAR diagnostic reveals the exact number — "
            "if we find nothing, you know better than anyone."
        ),
        evidence_anchor_ar="عرض حالة: عميل دفع 499 وكشف تسرباً بـ 12,000 ر.س شهري",
        evidence_anchor_en="Case: client paid 499 SAR, revealed 12k SAR monthly leak",
        reframe_question_ar="ما تكلفة عدم معرفة الرقم الحقيقي كل شهر؟",
        reframe_question_en="What is the cost of not knowing the real number each month?",
    ),
    ObjectionType.TIMING: ObjectionResponse(
        objection_type=ObjectionType.TIMING,
        objection_ar="الوقت مش مناسب الآن",
        objection_en="The timing isn't right",
        response_ar=(
            "التسرّب لا ينتظر. كل أسبوع بدون نظام متابعة = leads تضيع إلى المنافس. "
            "التشخيص يأخذ 7 أيام فقط ويعطيك صورة واضحة قبل ما تبدأ أي خطوة كبيرة."
        ),
        response_en=(
            "The leak doesn't wait. Every week without a follow-up system = leads going to a competitor. "
            "The diagnostic takes 7 days only and gives you a clear picture before any major step."
        ),
        evidence_anchor_ar="التشخيص لا يوقف عملياتكم — نعمل بجانبكم",
        evidence_anchor_en="The diagnostic doesn't stop your operations — we work alongside you",
        reframe_question_ar="ما الذي يتغير بعد 3 أشهر إذا استمر الوضع كما هو؟",
        reframe_question_en="What changes in 3 months if the situation stays as is?",
    ),
    ObjectionType.TRUST: ObjectionResponse(
        objection_type=ObjectionType.TRUST,
        objection_ar="ما نعرفكم / ما عندنا ثقة كافية",
        objection_en="We don't know you / lack sufficient trust",
        response_ar=(
            "طبيعي جداً. لهذا نبدأ بتشخيص 499 ر.س بدون التزام. النتائج مُوثَّقة وبموافقتكم. "
            "أنتم تقررون ماذا تفعلون بعد ذلك — بدون ضغط."
        ),
        response_en=(
            "Completely natural. That's why we start with a 499 SAR diagnostic with no commitment. "
            "Results are documented with your approval. You decide what to do next — no pressure."
        ),
        evidence_anchor_ar="كل إجراء يحتاج موافقتكم قبل التنفيذ",
        evidence_anchor_en="Every action requires your approval before execution",
        reframe_question_ar="ما الذي تحتاجون رؤيته لتبنوا ثقة مبدئية؟",
        reframe_question_en="What do you need to see to build initial trust?",
    ),
    ObjectionType.COMPLEXITY: ObjectionResponse(
        objection_type=ObjectionType.COMPLEXITY,
        objection_ar="الموضوع معقد / ما عندنا وقت نتعلم نظام جديد",
        objection_en="This is complex / we don't have time to learn a new system",
        response_ar=(
            "نفهم. Dealix لا يضيف تعقيداً — يُزيل الفوضى الموجودة. "
            "التشخيص السبعة أيام يكشف أين الوقت يضيع الآن ويعطيكم خطوة واحدة واضحة."
        ),
        response_en=(
            "We understand. Dealix doesn't add complexity — it removes existing chaos. "
            "The 7-day diagnostic reveals where time is wasted now and gives you one clear next step."
        ),
        evidence_anchor_ar="الإعداد الكامل بيدنا — أنتم تشاهدون النتائج",
        evidence_anchor_en="Full setup is on us — you see the results",
        reframe_question_ar="ما مقدار الوقت الذي يستهلكه النظام الحالي كل أسبوع؟",
        reframe_question_en="How much time does your current system consume each week?",
    ),
    ObjectionType.INTERNAL_SOLUTION: ObjectionResponse(
        objection_type=ObjectionType.INTERNAL_SOLUTION,
        objection_ar="عندنا فريق داخلي / نحن نبني هذا بأنفسنا",
        objection_en="We have an internal team / we're building this ourselves",
        response_ar=(
            "ممتاز. الفريق الداخلي يبني، ونحن نثبت. التشخيص يعطي فريقكم baseline دقيقة "
            "يبنون فوقها بدل ما يخمّنون من أين يبدأون."
        ),
        response_en=(
            "Excellent. The internal team builds, we prove. The diagnostic gives your team "
            "an accurate baseline to build on instead of guessing where to start."
        ),
        evidence_anchor_ar="التشخيص يُسرّع عمل الفريق الداخلي، لا يُعيقه",
        evidence_anchor_en="The diagnostic accelerates internal team work, not hinders it",
        reframe_question_ar="كم يستغرق فريقكم لبناء نفس الـ baseline بدون بيانات خارجية؟",
        reframe_question_en="How long would your team take to build the same baseline without external data?",
    ),
    ObjectionType.COMPETITOR: ObjectionResponse(
        objection_type=ObjectionType.COMPETITOR,
        objection_ar="نستخدم [منافس] بالفعل",
        objection_en="We already use [competitor]",
        response_ar=(
            "رائع. Dealix لا يستبدل أدواتكم — يثبت أنها تعمل. "
            "سؤال: هل عندكم تقرير يثبت لعميلكم ماذا حدث بعد الحملة؟ هذا ما يميّزنا."
        ),
        response_en=(
            "Great. Dealix doesn't replace your tools — it proves they work. "
            "Question: do you have a report that proves to your client what happened "
            "after the campaign? That's what differentiates us."
        ),
        evidence_anchor_ar="Dealix يعمل فوق أي أداة موجودة",
        evidence_anchor_en="Dealix works on top of any existing tool",
        reframe_question_ar="كيف تثبتون الآن القيمة لعميلكم بعد الحملة؟",
        reframe_question_en="How do you currently prove value to your client post-campaign?",
    ),
    ObjectionType.NOT_PRIORITY: ObjectionResponse(
        objection_type=ObjectionType.NOT_PRIORITY,
        objection_ar="هذا مش أولوية عندنا الآن",
        objection_en="This is not our priority right now",
        response_ar=(
            "نحترم ذلك. سؤال واحد فقط: ما أكبر شيء يعيق إيرادكم هذا الربع؟ "
            "إذا ما كان متعلق بما نقدمه، نحن آخر من تحتاجون."
        ),
        response_en=(
            "We respect that. One question: what is the biggest thing blocking your revenue "
            "this quarter? If it's not related to what we offer, we're the last you need."
        ),
        evidence_anchor_ar="نبدأ فقط حين يكون هناك ألم حقيقي",
        evidence_anchor_en="We only start when there is real pain",
        reframe_question_ar="ما الأولوية رقم 1 التي لو حُلّت غيّرت هذا الربع؟",
        reframe_question_en="What is priority #1 that, if solved, would change this quarter?",
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# Conviction sequences by ICP tier
# ─────────────────────────────────────────────────────────────────────────────

_CONVICTION_SEQUENCES: dict[str, tuple[ConvictionStep, ...]] = {
    "agency": (
        ConvictionStep(
            step_number=1,
            step_type="pain_probe",
            question_ar="بعد الحملة تنتهي — كيف تثبتون لعميلكم ماذا حدث بالضبط؟",
            question_en="After the campaign ends — how do you prove to your client exactly what happened?",
            purpose_ar="كشف فجوة الإثبات",
            purpose_en="Reveal the proof gap",
        ),
        ConvictionStep(
            step_number=2,
            step_type="pain_probe",
            question_ar="كم lead وصل بعد الحملة وكم منهم اتحوّل؟ هل الرقم موثّق؟",
            question_en="How many leads came after the campaign and how many converted? Is the number documented?",
            purpose_ar="تحديد التسرب الإيرادي",
            purpose_en="Identify revenue leak",
        ),
        ConvictionStep(
            step_number=3,
            step_type="proof_anchor",
            question_ar="إذا كان عندكم تقرير يثبت بالأرقام — كم عميل إضافي تحتفظون به كل ربع؟",
            question_en="If you had a report proving it in numbers — how many additional clients would you retain each quarter?",
            purpose_ar="ربط الإثبات بالإيراد",
            purpose_en="Link proof to revenue",
        ),
        ConvictionStep(
            step_number=4,
            step_type="roi_reveal",
            question_ar="بناءً على أرقامكم — نتشارك حساب ما يضيع شهرياً؟",
            question_en="Based on your numbers — shall we calculate together what's being lost monthly?",
            purpose_ar="تحويل الألم إلى مبلغ",
            purpose_en="Convert pain to SAR amount",
        ),
        ConvictionStep(
            step_number=5,
            step_type="decision_prompt",
            question_ar="7 أيام تشخيص، 499 ر.س، ونعطيكم الصورة الكاملة. هل نبدأ الأسبوع القادم؟",
            question_en="7-day diagnostic, 499 SAR, and we give you the complete picture. Shall we start next week?",
            purpose_ar="الإغلاق",
            purpose_en="Close",
        ),
    ),
    "b2b_direct": (
        ConvictionStep(
            step_number=1,
            step_type="pain_probe",
            question_ar="كم نسبة leads تضيع بين مرحلة التواصل والإغلاق؟ وكيف تتبعونها؟",
            question_en="What percentage of leads are lost between contact and close? How do you track them?",
            purpose_ar="كشف تسرب الـ pipeline",
            purpose_en="Reveal pipeline leak",
        ),
        ConvictionStep(
            step_number=2,
            step_type="pain_probe",
            question_ar="من يوافق على خروج الرسائل للعملاء وكيف تتأكدون من الاتساق؟",
            question_en="Who approves outgoing messages to clients and how do you ensure consistency?",
            purpose_ar="كشف فجوة الحوكمة",
            purpose_en="Reveal governance gap",
        ),
        ConvictionStep(
            step_number=3,
            step_type="proof_anchor",
            question_ar="إذا كان فريقكم يعرف بالضبط أين كل lead وما الخطوة التالية — كم يتحسن معدل الإغلاق؟",
            question_en="If your team knew exactly where every lead is and the next step — how much would close rate improve?",
            purpose_ar="ربط الحل بالإيراد",
            purpose_en="Link solution to revenue",
        ),
        ConvictionStep(
            step_number=4,
            step_type="roi_reveal",
            question_ar="متوسط صفقة عندكم كم؟ ونسبة الإغلاق الحالية؟ نحسب معاً التحسن المتوقع.",
            question_en="What is your average deal size? Current close rate? Let's calculate the expected improvement together.",
            purpose_ar="ROI حي",
            purpose_en="Live ROI calculation",
        ),
        ConvictionStep(
            step_number=5,
            step_type="decision_prompt",
            question_ar="Sprint أسبوع واحد — نخرج بخارطة طريق واضحة لإيرادكم. نبدأ؟",
            question_en="One-week sprint — we exit with a clear revenue roadmap. Shall we start?",
            purpose_ar="الإغلاق",
            purpose_en="Close",
        ),
    ),
    "executive": (
        ConvictionStep(
            step_number=1,
            step_type="pain_probe",
            question_ar="ما أكثر قرار يأخذ وقتاً في مؤسستكم بسبب غياب البيانات الموثوقة؟",
            question_en="What decision takes the most time in your organization due to lack of reliable data?",
            purpose_ar="كشف الفجوة التنفيذية",
            purpose_en="Reveal executive decision gap",
        ),
        ConvictionStep(
            step_number=2,
            step_type="pain_probe",
            question_ar="كيف تتحقق قيادتكم من أن الفريق ينفّذ ما اتُّفق عليه؟",
            question_en="How does your leadership verify that the team is executing what was agreed?",
            purpose_ar="كشف فجوة الحوكمة التنفيذية",
            purpose_en="Reveal executive governance gap",
        ),
        ConvictionStep(
            step_number=3,
            step_type="proof_anchor",
            question_ar="إذا كان لديكم dashboard يثبت كل قرار ومن اتخذه — كم يتسارع قرار القيادة؟",
            question_en="If you had a dashboard proving every decision and who made it — how much faster would leadership decide?",
            purpose_ar="ربط الحل بكفاءة القرار",
            purpose_en="Link solution to decision efficiency",
        ),
        ConvictionStep(
            step_number=4,
            step_type="roi_reveal",
            question_ar="ما تكلفة القرار البطيء على إيراد ربع واحد؟",
            question_en="What is the cost of a slow decision on one quarter's revenue?",
            purpose_ar="تحويل الفجوة إلى تكلفة",
            purpose_en="Convert gap to cost",
        ),
        ConvictionStep(
            step_number=5,
            step_type="decision_prompt",
            question_ar="تشخيص حوكمة تنفيذية — أسبوع واحد، نخرج بخريطة قرار واضحة. متى نبدأ؟",
            question_en="Executive governance diagnostic — one week, we exit with a clear decision map. When shall we start?",
            purpose_ar="الإغلاق التنفيذي",
            purpose_en="Executive close",
        ),
    ),
}

_DEFAULT_SEQUENCE_KEY = "b2b_direct"


# Pain type → evidence anchor mapping
_PAIN_TO_ANCHOR: dict[PainType, str] = {
    PainType.REVENUE_LEAK: "revenue_intelligence_sprint_roi_case",
    PainType.DATA_CHAOS: "data_quality_baseline_proof",
    PainType.PROOF_GAP: "agency_proof_pack_sample",
    PainType.GOVERNANCE_ABSENCE: "governance_diagnostic_report",
    PainType.FOLLOW_UP_FAILURE: "ten_lead_audit_followup_analysis",
    PainType.AI_WITHOUT_CONTROL: "governed_ai_audit_evidence",
    PainType.REPORTING_VACUUM: "post_campaign_proof_pack",
}


def _select_evidence_anchors(signals: list[PainSignal]) -> tuple[str, ...]:
    seen: set[str] = set()
    anchors: list[str] = []
    for s in signals:
        anchor = _PAIN_TO_ANCHOR.get(s.pain_type)
        if anchor and anchor not in seen:
            anchors.append(anchor)
            seen.add(anchor)
    return tuple(anchors)


def build_persuasion_chain(
    icp_tier: str,
    pain_signals: list[PainSignal],
    *,
    target_objections: list[ObjectionType] | None = None,
) -> PersuasionChain:
    """Build a deterministic persuasion chain from ICP tier and pain signals.

    Args:
        icp_tier: ICP segment key (e.g., 'agency', 'b2b_direct', 'executive').
        pain_signals: List of detected pain signals with severity/cost.
        target_objections: Specific objections to include (default: all).

    Returns:
        PersuasionChain with conviction sequence, objection responses, closing questions.
    """
    sequence_key = icp_tier if icp_tier in _CONVICTION_SEQUENCES else _DEFAULT_SEQUENCE_KEY
    conviction_seq = _CONVICTION_SEQUENCES[sequence_key]

    objection_types = target_objections or list(ObjectionType)
    objection_responses = tuple(
        _OBJECTION_REGISTRY[ot] for ot in objection_types if ot in _OBJECTION_REGISTRY
    )

    closing_ar = (
        "هل نبدأ بتشخيص 7 أيام الأسبوع القادم؟",
        "ما الذي يمنعكم من المضي قدماً اليوم؟",
        "إذا حُل هذا الموضوع خلال شهر — كيف يؤثر على ربعكم القادم؟",
    )
    closing_en = (
        "Shall we start with the 7-day diagnostic next week?",
        "What's stopping you from moving forward today?",
        "If this is resolved in a month — how does it impact your next quarter?",
    )

    total_pain = sum(s.cost_estimate_sar for s in pain_signals)

    return PersuasionChain(
        icp_tier=icp_tier,
        pain_signals=tuple(pain_signals),
        conviction_sequence=conviction_seq,
        objection_responses=objection_responses,
        closing_questions_ar=closing_ar,
        closing_questions_en=closing_en,
        evidence_anchors=_select_evidence_anchors(pain_signals),
        total_pain_cost_sar_monthly=total_pain,
    )


def get_objection_response(objection_type: ObjectionType) -> ObjectionResponse | None:
    """Retrieve a single objection response by type."""
    return _OBJECTION_REGISTRY.get(objection_type)


def known_icp_tiers() -> tuple[str, ...]:
    """Return ICP tiers with explicit conviction sequences."""
    return tuple(_CONVICTION_SEQUENCES.keys())


__all__ = [
    "ConvictionStep",
    "ObjectionResponse",
    "ObjectionType",
    "PainSignal",
    "PainType",
    "PersuasionChain",
    "build_persuasion_chain",
    "get_objection_response",
    "known_icp_tiers",
]
