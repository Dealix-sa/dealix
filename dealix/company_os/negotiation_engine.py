"""Governed sales negotiation planning; no autonomous commercial commitments."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class NegotiationContext:
    account_name: str
    offer_id: str
    customer_problem: str
    customer_priorities: tuple[str, ...] = ()
    known_objections: tuple[str, ...] = ()
    list_price_sar: float | None = None
    approved_floor_sar: float | None = None
    max_discount_without_approval_pct: float = 0.0
    requested_discount_pct: float = 0.0
    non_standard_terms_requested: bool = False
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class NegotiationPlan:
    account_name: str
    offer_id: str
    evidence_refs: tuple[str, ...]
    discovery_questions_ar: tuple[str, ...]
    opening_posture_ar: str
    package_options: tuple[dict[str, Any], ...]
    concession_ladder: tuple[dict[str, Any], ...]
    red_lines: tuple[str, ...]
    objection_responses: tuple[dict[str, str], ...]
    missing_inputs: tuple[str, ...]
    approval_required: bool
    approval_question_ar: str | None
    external_commitment_made: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_negotiation_plan(context: NegotiationContext) -> NegotiationPlan:
    missing: list[str] = []
    if not context.evidence_refs:
        missing.append("customer_evidence")
    if context.list_price_sar is None:
        missing.append("approved_list_price")
    if context.approved_floor_sar is None:
        missing.append("approved_price_floor")
    approval_required = (
        context.requested_discount_pct > context.max_discount_without_approval_pct
        or context.non_standard_terms_requested
    )
    questions = (
        "ما النتيجة التشغيلية التي يجب أن تتحقق ليصبح الاستثمار منطقيًا؟",
        "كيف تقيسون المشكلة اليوم وما خط الأساس المتفق عليه؟",
        "من يملك القرار التجاري، ومن يراجع الأمن والبيانات والعقد؟",
        "ما الذي يمنع القرار الآن: القيمة، الميزانية، المخاطر، أم التوقيت؟",
        "إذا عالجنا العائق الرئيسي، ما الخطوة والموعد الواقعيان؟",
    )
    package_options: list[dict[str, Any]] = [
        {
            "option": "diagnostic",
            "positioning_ar": "تشخيص محدود لإثبات المشكلة وخط الأساس قبل الالتزام الأكبر.",
            "price_sar": None,
            "requires_approved_catalog_price": True,
        },
        {
            "option": "core_scope",
            "positioning_ar": "النطاق الأساسي بالمخرجات والقياس المتفق عليهما.",
            "price_sar": context.list_price_sar,
            "requires_approved_catalog_price": context.list_price_sar is None,
        },
        {
            "option": "phased_scope",
            "positioning_ar": "تقسيم التنفيذ إلى مراحل دون تخفيض سعر نفس النطاق.",
            "price_sar": None,
            "requires_scope_review": True,
        },
    ]
    concessions = (
        {
            "give": "مرونة في توقيت البدء",
            "get": "موعد قرار واضح وصاحب قرار حاضر",
            "changes_price_or_terms": False,
            "approval_required": False,
        },
        {
            "give": "توزيع النطاق على مراحل",
            "get": "اعتماد المرحلة الأولى وخط أساس موقع",
            "changes_price_or_terms": True,
            "approval_required": True,
        },
        {
            "give": "خصم أو شروط دفع مختلفة",
            "get": "خفض نطاق/التزام أطول/دفع مقدم حسب السياسة",
            "changes_price_or_terms": True,
            "approval_required": True,
        },
    )
    objection_responses = tuple(
        {
            "objection": objection,
            "response_ar": (
                "أتفهم الاعتراض. قبل تغيير النطاق أو السعر، نحتاج تحديد أثره "
                "على النتيجة والمخاطر ثم اختيار بديل قابل للقياس."
            ),
        }
        for objection in context.known_objections
    )
    approval_question = None
    if approval_required:
        approval_question = (
            "هل تعتمد الاستثناء التجاري المطلوب بعد مراجعة الحد الأدنى والنطاق "
            "والمقابل الذي سنحصل عليه؟"
        )
    return NegotiationPlan(
        account_name=context.account_name,
        offer_id=context.offer_id,
        evidence_refs=context.evidence_refs,
        discovery_questions_ar=questions,
        opening_posture_ar=(
            "ابدأ بنتيجة العميل وخط الأساس، ثم اربط النطاق بالقيمة. لا تبدأ بالخصم."
        ),
        package_options=tuple(package_options),
        concession_ladder=concessions,
        red_lines=(
            "لا ضمان لإيراد أو نتيجة غير مثبتة.",
            "لا تخفيض دون مقابل واضح أو صلاحية معتمدة.",
            "لا التزام قانوني أو أمني أو زمني خارج العرض والعقد.",
            "لا كشف للحد الأدنى أو معلومات Dealix الداخلية للعميل.",
        ),
        objection_responses=objection_responses,
        missing_inputs=tuple(missing),
        approval_required=approval_required,
        approval_question_ar=approval_question,
        external_commitment_made=False,
    )
