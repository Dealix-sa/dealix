"""Proposal Factory — governed proposal drafts from qualified prospects.

Reuses ``sales_os.build_proposal_skeleton`` (which prefills the two
non-negotiable statements: no-sales-guarantee + governance-boundaries) and
fills the remaining sections deterministically from the prospect. Output is a
draft for human review — never a binding commitment.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.distribution_os.models import Prospect, ProspectStatus
from auto_client_acquisition.sales_os import build_proposal_skeleton

DEFAULT_SPRINT = "Revenue Intelligence Sprint"
DEFAULT_PRICE_RANGE = "499–4,999 SAR حسب النطاق (Diagnostic → Sprint → Managed Ops)"

#: Prospect stages that are proposal-ready.
PROPOSAL_READY_STATUSES: frozenset[str] = frozenset(
    {ProspectStatus.DISCOVERY_BOOKED.value, ProspectStatus.QUALIFIED.value}
)


@dataclass(frozen=True)
class ProposalDraft:
    prospect_id: str
    company: str
    sector: str
    sections: dict[str, str]
    evidence_level: str = "L1"
    approval_required: bool = True


def build_proposal(
    prospect: Prospect,
    *,
    sprint_name: str = DEFAULT_SPRINT,
    price_range: str = DEFAULT_PRICE_RANGE,
) -> ProposalDraft:
    sk = build_proposal_skeleton(client_label=prospect.company, sprint_name=sprint_name)
    sk["problem"] = prospect.pain_hypothesis or sk["problem"]
    sk["current_maturity"] = "يُحدّد خلال التشخيص بناءً على مصادر العملاء الحالية."
    sk["scope"] = (
        "مراجعة مصادر العملاء، تنظيم workflow المتابعات، رؤية إيراد يومية، "
        "توليد مسودات محكومة، تقرير أسبوعي، وProof Pack أساسي."
    )
    sk["inputs_needed"] = "صلاحية اطّلاع على مصادر العملاء الحالية + جهة تواصل واحدة للقرار."
    sk["deliverables"] = (
        "workflow متابعة محكوم، لوحة رؤية يومية، حزمة مسودات أولى، تقرير أسبوعي، Proof Pack."
    )
    sk["proof_metrics"] = "قياس قبل/بعد على تنظيم المتابعات وزمنها (مرتبط بمستوى دليل واضح)."
    sk["timeline"] = "7–14 يوماً لأول workflow تشغيلي."
    sk["price"] = price_range
    sk["retainer_path"] = "إمكانية الانتقال إلى Managed Ops شهري بعد إثبات القيمة."
    sk["exclusions"] = (
        "لا إرسال خارجي تلقائي، ولا نطاق مفتوح، ولا التزام قانوني بدون مراجعة، "
        "ولا أرقام نتائج بدون دليل."
    )
    return ProposalDraft(
        prospect_id=prospect.id,
        company=prospect.company,
        sector=prospect.sector,
        sections=sk,
    )


_SECTION_TITLES_AR: dict[str, str] = {
    "problem": "المشكلة",
    "current_maturity": "النضج الحالي",
    "recommended_sprint": "الباقة المقترحة",
    "scope": "نطاق العمل",
    "inputs_needed": "المدخلات المطلوبة",
    "deliverables": "المخرجات",
    "governance_boundaries": "حدود الحوكمة",
    "proof_metrics": "مؤشرات الإثبات",
    "timeline": "الجدول الزمني",
    "price": "السعر / النطاق السعري",
    "retainer_path": "مسار الاستمرار",
    "exclusions": "ما لا يشمله العرض",
    "no_sales_guarantee_statement": "إفصاح: لا ضمان مبيعات",
}


def render_proposal_markdown(proposal: ProposalDraft) -> str:
    lines = [
        f"# عرض Dealix — مسودة للمراجعة — {proposal.company}",
        "",
        f"- **القطاع:** {proposal.sector}",
        f"- **مستوى الدليل:** {proposal.evidence_level}",
        "- **الحالة:** مسودة تتطلب موافقة (لا التزام نهائي)",
        "",
    ]
    for key, title in _SECTION_TITLES_AR.items():
        value = proposal.sections.get(key, "").strip()
        if not value:
            continue
        lines.append(f"## {title}")
        lines.append(value)
        lines.append("")
    lines.append("## الخطوة التالية")
    lines.append("اعتماد جلسة تشخيص أو الموافقة على البدء — ثم يُرسل رابط الدفع الرسمي يدوياً.")
    lines.append("")
    return "\n".join(lines)


def generate_proposals(prospects: list[Prospect]) -> list[ProposalDraft]:
    """Build proposal drafts for all proposal-ready prospects."""
    return [build_proposal(p) for p in prospects if p.status in PROPOSAL_READY_STATUSES]


__all__ = [
    "DEFAULT_PRICE_RANGE",
    "DEFAULT_SPRINT",
    "PROPOSAL_READY_STATUSES",
    "ProposalDraft",
    "build_proposal",
    "generate_proposals",
    "render_proposal_markdown",
]
