"""Proposal pack builder for the Dealix launch OS.

Generates structured bilingual proposal packs from discovery notes and
renders them as Arabic-primary markdown documents ready for client delivery.

The ``ProposalPack`` aligns with ``schemas/launch/proposal_pack.schema.json``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class ProposalPack:
    """Structured proposal ready for client delivery.

    Attributes:
        id:                  UUID-based proposal identifier.
        account_name:        Client company name.
        offer_id:            Canonical offer identifier.
        offer_name_ar:       Arabic offer name.
        value_prop_ar:       One-sentence Arabic value proposition.
        scope_items:         List of in-scope deliverable strings.
        timeline_weeks:      Estimated delivery timeline in weeks.
        investment_sar:      Investment amount in SAR (0 = TBD / pending approval).
        roi_narrative_ar:    Arabic ROI story based on discovery.
        proof_references:    List of proof reference strings.
        next_step_ar:        Arabic next-step instruction.
        problem_ar:          Arabic problem statement.
        out_of_scope:        List of explicitly excluded items.
        pricing_status:      Pricing approval state.
        approval_required:   Whether founder approval is needed.
        evidence_level:      Claim evidence level L0–L5.
        created_at_iso:      ISO timestamp.

    Examples:
        >>> p = ProposalPack(
        ...     id="prop_001",
        ...     account_name="Acme Motors",
        ...     offer_id="REVENUE_LEAK_AUDIT",
        ...     offer_name_ar="تشخيص تسرب الإيرادات",
        ...     value_prop_ar="نساعدك على اكتشاف الإيرادات الضائعة.",
        ...     scope_items=["تشخيص منظومة المبيعات"],
        ...     timeline_weeks=4,
        ...     investment_sar=15000,
        ...     roi_narrative_ar="تسرب محتمل.",
        ...     proof_references=["حالة عميل مماثل"],
        ...     next_step_ar="توقيع الاتفاقية",
        ... )
        >>> p.offer_id
        'REVENUE_LEAK_AUDIT'
    """

    id: str
    account_name: str
    offer_id: str
    offer_name_ar: str
    value_prop_ar: str
    scope_items: list[str]
    timeline_weeks: int
    investment_sar: int
    roi_narrative_ar: str
    proof_references: list[str]
    next_step_ar: str
    problem_ar: str = ""
    out_of_scope: list[str] = field(default_factory=list)
    pricing_status: str = "draft_only"
    approval_required: bool = True
    evidence_level: str = "L2"
    created_at_iso: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "account_name": self.account_name,
            "offer_id": self.offer_id,
            "offer_name_ar": self.offer_name_ar,
            "value_prop_ar": self.value_prop_ar,
            "scope_items": self.scope_items,
            "timeline_weeks": self.timeline_weeks,
            "investment_sar": self.investment_sar,
            "roi_narrative_ar": self.roi_narrative_ar,
            "proof_references": self.proof_references,
            "next_step_ar": self.next_step_ar,
            "problem_ar": self.problem_ar,
            "out_of_scope": self.out_of_scope,
            "pricing_status": self.pricing_status,
            "approval_required": self.approval_required,
            "evidence_level": self.evidence_level,
            "created_at_iso": self.created_at_iso,
        }


# ---------------------------------------------------------------------------
# Offer catalogue
# ---------------------------------------------------------------------------

_OFFER_CATALOGUE: dict[str, dict[str, Any]] = {
    "REVENUE_LEAK_AUDIT": {
        "name_ar": "تشخيص تسرب الإيرادات",
        "value_prop_ar": "نكشف أين تضيع إيراداتك ونضع خارطة طريق لاسترداد ما يمكن استرداده.",
        "problem_ar": "معظم الشركات لا تعرف بدقة أين تتسرب إيراداتها — في متابعة العملاء، في التسعير، أم في ضياع الصفقات.",
        "scope_items": [
            "مقابلة اكتشافية مع الفريق المعني (2 ساعة)",
            "تحليل قمع المبيعات الحالي",
            "خارطة الفجوات والمخاطر",
            "تقرير نقاط الضعف الرئيسية",
            "خارطة طريق 90 يوماً بخطوات قابلة للتنفيذ",
        ],
        "out_of_scope": [
            "تنفيذ الحلول التقنية",
            "ضمان نتائج مالية محددة",
        ],
        "timeline_weeks": 2,
        "investment_sar": 12_000,
        "proof_references": [],
    },
    "WHATSAPP_FOLLOWUP_OS": {
        "name_ar": "منظومة متابعة واتساب",
        "value_prop_ar": "أتمتة متابعة العملاء المحتملين عبر واتساب بعد الموافقة الصريحة.",
        "problem_ar": "العملاء المحتملون يُفقدون بسبب غياب نظام متابعة منتظم وسريع.",
        "scope_items": [
            "تصميم تسلسل الرسائل (3 خطوات)",
            "إعداد قواعد الموافقة والإذن",
            "تدريب الفريق على الأداة",
            "قياس معدل الاستجابة لمدة 30 يوماً",
        ],
        "out_of_scope": [
            "أتمتة المبيعات الكاملة",
            "تكامل CRM من الدرجة الأولى",
        ],
        "timeline_weeks": 3,
        "investment_sar": 18_000,
        "proof_references": [],
    },
    "SALES_COMMAND_CENTER": {
        "name_ar": "مركز قيادة المبيعات",
        "value_prop_ar": "لوحة تحكم مركزية تعطي المدير رؤية كاملة على خط أنابيب المبيعات يومياً.",
        "problem_ar": "القيادة لا ترى بشكل واضح أين توقفت الصفقات أو ما الخطوة التالية لكل فرصة.",
        "scope_items": [
            "تصميم لوحة تحكم المبيعات",
            "تكامل مع الأدوات الحالية",
            "إجراءات التشغيل اليومية",
            "تقارير أسبوعية تلقائية",
        ],
        "out_of_scope": [
            "تطوير تطبيقات مخصصة",
            "برمجة CRM من الصفر",
        ],
        "timeline_weeks": 4,
        "investment_sar": 25_000,
        "proof_references": [],
    },
    "PROPOSAL_PROOF_PACK_OS": {
        "name_ar": "منظومة العروض والإثبات",
        "value_prop_ar": "عروض أسعار احترافية وحزم إثبات موثقة تُغلق الصفقات بثقة.",
        "problem_ar": "العروض الحالية ضعيفة الإقناع ولا تحمل أدلة كافية على القيمة المقدمة.",
        "scope_items": [
            "قوالب عروض الأسعار الموحدة",
            "حزمة الإثبات لأول 3 عملاء",
            "مكتبة الأسئلة الشائعة والردود",
            "تدريب الفريق على تقديم العرض",
        ],
        "out_of_scope": [
            "أدوات توقيع إلكتروني",
            "إدارة العقود القانونية",
        ],
        "timeline_weeks": 3,
        "investment_sar": 20_000,
        "proof_references": [],
    },
    "AI_OPERATING_SYSTEM_FOR_SMB": {
        "name_ar": "نظام التشغيل بالذكاء الاصطناعي للشركات الصغيرة والمتوسطة",
        "value_prop_ar": "منظومة تشغيلية متكاملة بالذكاء الاصطناعي تحول الإجراءات اليدوية إلى آلية ذكية.",
        "problem_ar": "الشركات الصغيرة تصرف جهداً بشرياً كبيراً على مهام يمكن أتمتتها، مما يُبطئ النمو.",
        "scope_items": [
            "تشخيص شامل للعمليات القابلة للأتمتة",
            "تصميم أول 3 تدفقات عمل آلية",
            "التدريب والتسليم",
            "دعم 60 يوماً بعد التسليم",
        ],
        "out_of_scope": [
            "برمجة مخصصة خارج نطاق الأدوات الحالية",
            "تكاملات مع بائعي ERP",
        ],
        "timeline_weeks": 8,
        "investment_sar": 45_000,
        "proof_references": [],
    },
    "CUSTOM_ENTERPRISE_OS": {
        "name_ar": "نظام تشغيل مؤسسي مخصص",
        "value_prop_ar": "نظام تشغيل مؤسسي بالكامل يُصمم وفق احتياجات مؤسستك.",
        "problem_ar": "المؤسسات الكبيرة تحتاج منظومة تشغيلية متكاملة تعكس تعقيدها التنظيمي وأهدافها الاستراتيجية.",
        "scope_items": [
            "تحليل الوضع الراهن (4 أسابيع)",
            "تصميم المنظومة المستقبلية",
            "خارطة التحول التدريجي",
            "تنفيذ المرحلة الأولى",
            "قياس الأثر ومراجعة ربع سنوية",
        ],
        "out_of_scope": [
            "تطوير برمجيات مخصصة من الصفر",
            "بنية تحتية سحابية",
        ],
        "timeline_weeks": 16,
        "investment_sar": 120_000,
        "proof_references": [],
    },
}

# Public set of valid offer IDs for callers.
VALID_OFFER_IDS: frozenset[str] = frozenset(_OFFER_CATALOGUE)


def build_proposal(
    account: dict[str, Any],
    offer_id: str,
    discovery_notes: dict[str, Any] | None = None,
    *,
    pricing_status: str = "draft_only",
    approval_required: bool = True,
    evidence_level: str = "L2",
) -> ProposalPack:
    """Build a :class:`ProposalPack` from account data and discovery notes.

    Unknown ``offer_id`` values are handled gracefully — the pack is created
    with empty catalogue fields and the ``offer_id`` preserved.

    Args:
        account:          Account dict with at least ``account_id`` and
                          optionally ``account_name``, ``sector``.
        offer_id:         Canonical offer identifier from ``_OFFER_CATALOGUE``.
        discovery_notes:  Free-form dict from discovery call; keys ``pain_ar``,
                          ``leakage_sar``, ``timeline_note``, ``proof_ref``
                          are recognised if present.
        pricing_status:   Pricing approval state.
        approval_required: Whether founder must approve before sending.
        evidence_level:   Claim evidence level.

    Returns:
        Populated :class:`ProposalPack`.

    Examples:
        >>> pack = build_proposal(
        ...     {"account_id": "acme_001", "account_name": "Acme Motors", "sector": "automotive"},
        ...     "REVENUE_LEAK_AUDIT",
        ...     {"pain_ar": "فقدان العملاء المحتملين بعد الزيارة", "leakage_sar": 150000},
        ... )
        >>> pack.offer_id
        'REVENUE_LEAK_AUDIT'
        >>> pack.timeline_weeks
        2

        >>> unknown = build_proposal({"account_id": "x"}, "NONEXISTENT_OFFER", {})
        >>> unknown.offer_id
        'NONEXISTENT_OFFER'
    """
    notes = discovery_notes or {}
    catalogue = _OFFER_CATALOGUE.get(offer_id, {})
    account_name = str(account.get("account_name", account.get("account_id", "")))

    # Derive ROI narrative from discovery notes.
    leakage = notes.get("leakage_sar", 0)
    pain_ar = notes.get("pain_ar", catalogue.get("problem_ar", ""))
    timeline_note = str(notes.get("timeline_note", ""))
    extra_proof = str(notes.get("proof_ref", ""))

    if leakage and int(leakage) > 0:
        roi_narrative_ar = (
            f"فرضية كمية أدخلت في الاكتشاف: {int(leakage):,} ريال سنوياً. "
            "لا تُعامل كحقيقة أو عائد متوقع قبل ربطها بمرجع وخط أساس يتحقق منه العميل."
        )
    else:
        roi_narrative_ar = "سيتم تحديد قيمة العائد بدقة بعد مرحلة التشخيص."

    if timeline_note:
        roi_narrative_ar += f" {timeline_note}"

    proof_refs = list(catalogue.get("proof_references", []))
    if extra_proof:
        proof_refs.insert(0, extra_proof)

    return ProposalPack(
        id=f"prop_{uuid.uuid4().hex[:10]}",
        account_name=account_name,
        offer_id=offer_id,
        offer_name_ar=catalogue.get("name_ar", offer_id),
        value_prop_ar=catalogue.get("value_prop_ar", ""),
        scope_items=list(catalogue.get("scope_items", [])),
        timeline_weeks=int(catalogue.get("timeline_weeks", 4)),
        investment_sar=(
            int(catalogue.get("investment_sar", 0)) if pricing_status == "founder_approved" else 0
        ),
        roi_narrative_ar=roi_narrative_ar,
        proof_references=proof_refs,
        next_step_ar=(
            "مراجعة النطاق والدليل والسعر مع أصحاب القرار، ثم طلب موافقة المؤسس "
            "قبل التوقيع أو تحديد موعد ملزم."
        ),
        problem_ar=pain_ar,
        out_of_scope=list(catalogue.get("out_of_scope", [])),
        pricing_status=pricing_status,
        approval_required=approval_required,
        evidence_level=evidence_level,
        created_at_iso=datetime.now(UTC).isoformat(),
    )


def render_markdown(pack: ProposalPack) -> str:
    """Render a :class:`ProposalPack` as Arabic-primary markdown.

    Args:
        pack: Populated proposal pack.

    Returns:
        Markdown string ready for sending or printing.

    Examples:
        >>> pack = build_proposal(
        ...     {"account_id": "t1", "account_name": "Test Co"},
        ...     "REVENUE_LEAK_AUDIT",
        ...     {},
        ... )
        >>> md = render_markdown(pack)
        >>> "# " in md
        True
        >>> "Test Co" in md
        True
        >>> "REVENUE_LEAK_AUDIT" in md
        True
        >>> "ريال" in md
        True
        >>> "نطاق" in md
        True
        >>> pack.roi_narrative_ar[:20] in md
        True
        >>> pack.next_step_ar in md
        True
    """
    scope_md = "\n".join(f"- {item}" for item in pack.scope_items)
    out_of_scope_md = (
        "\n".join(f"- {item}" for item in pack.out_of_scope)
        if pack.out_of_scope
        else "- لا يوجد استثناءات مدرجة"
    )
    proof_md = (
        "\n".join(f"- {ref}" for ref in pack.proof_references)
        if pack.proof_references
        else "- قيد الإضافة"
    )
    investment_text = (
        f"{pack.investment_sar:,} ريال سعودي"
        if pack.investment_sar > 0
        else "يُحدد بالريال السعودي بعد اعتماد النطاق والسعر من المؤسس"
    )

    return f"""# عرض خدمة: {pack.offer_name_ar}

**المرجع:** {pack.id}
**العرض:** {pack.offer_id}
**العميل:** {pack.account_name}
**تاريخ الإعداد:** {pack.created_at_iso[:10]}

---

## المشكلة

{pack.problem_ar}

---

## القيمة المقترحة

{pack.value_prop_ar}

---

## نطاق العمل

{scope_md}

---

## خارج النطاق

{out_of_scope_md}

---

## الجدول الزمني

المدة المقدرة: **{pack.timeline_weeks} أسبوع**

---

## الاستثمار

{investment_text}

> ملاحظة: السعر النهائي خاضع للموافقة ({pack.pricing_status})

---

## عائد الاستثمار

{pack.roi_narrative_ar}

---

## مراجع الإثبات

{proof_md}

---

## الخطوة التالية

{pack.next_step_ar}

---

*معرّف العرض: {pack.offer_id} — مستوى الدليل: {pack.evidence_level}*
"""


if __name__ == "__main__":
    import doctest

    results = doctest.testmod(verbose=False)
    print(f"Proposal engine doctests: {results.attempted} run, {results.failed} failed")

    pack = build_proposal(
        {"account_id": "smoke_co", "account_name": "Smoke Contracting", "sector": "contracting"},
        "SALES_COMMAND_CENTER",
        {"pain_ar": "لا يوجد لوحة تحكم مركزية للمبيعات", "leakage_sar": 200_000},
    )
    md = render_markdown(pack)
    print(f"Proposal {pack.id} rendered ({len(md)} chars)")
    print(md[:400])
