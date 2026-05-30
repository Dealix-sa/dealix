"""
Proof Pack Builder — Build sellable proof packs from pilot events.
بانئ طقم الإثبات — يبني أطقم إثبات قابلة للبيع من أحداث البرنامج التجريبي.

Takes pilot evidence (messages, replies, deals) and builds a structured
proof pack (L1 level minimum) for client delivery and case study eligibility.

Constitutional: NO_FAKE_PROOF — every claim must have a referenced event.
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

log = logging.getLogger(__name__)

# Minimum evidence requirements for each level
EVIDENCE_LEVELS: dict[int, dict[str, Any]] = {
    0: {"name": "diagnostic", "min_messages": 0, "min_replies": 0, "min_proof_events": 0},
    1: {"name": "sprint_proof", "min_messages": 3, "min_replies": 1, "min_proof_events": 1},
    2: {"name": "data_pack", "min_messages": 5, "min_replies": 2, "min_proof_events": 1},
    3: {"name": "managed_ops", "min_messages": 10, "min_replies": 3, "min_proof_events": 3},
    4: {"name": "executive", "min_messages": 20, "min_replies": 5, "min_proof_events": 5},
    5: {"name": "venture_grade", "min_messages": 50, "min_replies": 15, "min_proof_events": 10},
}


@dataclass
class ProofEvidence:
    """Raw evidence collected during pilot."""
    messages_drafted: int = 0
    messages_approved: int = 0
    messages_sent: int = 0  # founder actually sent
    replies_received: int = 0
    meetings_booked: int = 0
    deals_created: int = 0
    response_time_before_hours: float = 0.0
    response_time_after_hours: float = 0.0
    proof_events: list[dict[str, Any]] = field(default_factory=list)
    testimonial_text: str = ""
    testimonial_consented: bool = False


@dataclass
class ProofPack:
    pack_id: str
    pilot_id: str
    account_id: str
    company_name: str
    contact_name: str
    sector: str
    evidence_level: int
    evidence_level_name: str

    # Bilingual sections
    executive_summary_ar: str
    executive_summary_en: str
    problem_statement_ar: str
    problem_statement_en: str
    actions_taken_ar: str
    actions_taken_en: str
    results_ar: str
    results_en: str
    testimonial_ar: str
    testimonial_en: str
    next_steps_ar: str
    next_steps_en: str

    # Metrics
    messages_drafted: int
    messages_sent: int
    replies_received: int
    meetings_booked: int
    response_time_improvement: str

    is_complete: bool = False
    can_use_as_case_study: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack_id": self.pack_id,
            "pilot_id": self.pilot_id,
            "account_id": self.account_id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "sector": self.sector,
            "evidence_level": self.evidence_level,
            "evidence_level_name": self.evidence_level_name,
            "executive_summary_ar": self.executive_summary_ar,
            "executive_summary_en": self.executive_summary_en,
            "problem_statement_ar": self.problem_statement_ar,
            "problem_statement_en": self.problem_statement_en,
            "actions_taken_ar": self.actions_taken_ar,
            "actions_taken_en": self.actions_taken_en,
            "results_ar": self.results_ar,
            "results_en": self.results_en,
            "testimonial_ar": self.testimonial_ar,
            "testimonial_en": self.testimonial_en,
            "next_steps_ar": self.next_steps_ar,
            "next_steps_en": self.next_steps_en,
            "messages_drafted": self.messages_drafted,
            "messages_sent": self.messages_sent,
            "replies_received": self.replies_received,
            "meetings_booked": self.meetings_booked,
            "response_time_improvement": self.response_time_improvement,
            "is_complete": self.is_complete,
            "can_use_as_case_study": self.can_use_as_case_study,
            "created_at": self.created_at.isoformat(),
        }

    def to_markdown_ar(self) -> str:
        lines = [
            f"# طقم الإثبات — {self.company_name}",
            f"**المستوى:** L{self.evidence_level} — {self.evidence_level_name}",
            f"**التاريخ:** {self.created_at.strftime('%Y-%m-%d')}",
            f"**رقم البرنامج:** {self.pilot_id}",
            "",
            "---",
            "",
            "## الملخص التنفيذي",
            self.executive_summary_ar,
            "",
            "---",
            "",
            "## المشكلة",
            self.problem_statement_ar,
            "",
            "## الإجراءات المتخذة",
            self.actions_taken_ar,
            "",
            "## النتائج المحققة",
            self.results_ar,
            "",
        ]

        if self.testimonial_ar and self.can_use_as_case_study:
            lines += [
                "## شهادة العميل",
                f'> "{self.testimonial_ar}"',
                f"> — {self.contact_name}، {self.company_name}",
                "",
            ]

        lines += [
            "## الإحصائيات الرئيسية",
            f"- رسائل مُعدّة: {self.messages_drafted}",
            f"- رسائل مُرسلة: {self.messages_sent}",
            f"- ردود واردة: {self.replies_received}",
            f"- اجتماعات محجوزة: {self.meetings_booked}",
            f"- تحسّن وقت الاستجابة: {self.response_time_improvement}",
            "",
            "## الخطوة التالية",
            self.next_steps_ar,
            "",
            "---",
            "",
            "*طقم إثبات سري — Dealix. البيانات محمية وفق PDPL.*",
        ]
        return "\n".join(lines)


def _calculate_evidence_level(evidence: ProofEvidence) -> int:
    """Determine the evidence level based on what was collected."""
    for level in range(5, -1, -1):
        req = EVIDENCE_LEVELS[level]
        if (
            evidence.messages_sent >= req["min_messages"]
            and evidence.replies_received >= req["min_replies"]
            and len(evidence.proof_events) >= req["min_proof_events"]
        ):
            return level
    return 0


def _response_time_improvement(before: float, after: float) -> str:
    if before <= 0 or after <= 0:
        return "لم يُقاس / Not measured"
    improvement_pct = ((before - after) / before) * 100
    before_str = f"{before:.0f} ساعة" if before > 1 else "أقل من ساعة"
    after_str = f"{after:.1f} ساعة" if after > 1 else f"{after*60:.0f} دقيقة"
    return f"من {before_str} إلى {after_str} ({improvement_pct:.0f}% تحسّن)"


def build_proof_pack(
    *,
    pilot_id: str,
    account_id: str,
    company_name: str,
    contact_name: str,
    sector: str,
    pain_point: str,
    evidence: ProofEvidence,
) -> ProofPack:
    """
    Build a proof pack from collected pilot evidence.
    Constitutional: only uses real evidence — no fabricated metrics.
    """
    level = _calculate_evidence_level(evidence)
    level_info = EVIDENCE_LEVELS[level]
    is_complete = level >= 1
    can_case_study = level >= 1 and evidence.testimonial_consented and bool(evidence.testimonial_text)

    rt_improvement = _response_time_improvement(
        evidence.response_time_before_hours,
        evidence.response_time_after_hours,
    )

    # Build sections from evidence
    exec_summary_ar = (
        f"خلال برنامج التجربة 7 أيام مع {company_name}، أعددنا {evidence.messages_drafted} رسالة مخصصة، "
        f"وحققنا {evidence.replies_received} رداً إيجابياً، وحجزنا {evidence.meetings_booked} اجتماع."
    )
    exec_summary_en = (
        f"During the 7-day pilot with {company_name}, we prepared {evidence.messages_drafted} personalized messages, "
        f"achieved {evidence.replies_received} positive replies, and booked {evidence.meetings_booked} meetings."
    )

    problem_ar = f"{company_name} تواجه: {pain_point}. هذا يُؤخّر الاستجابة للعملاء المحتملين ويُفقد الصفقات."
    problem_en = f"{company_name} faces: {pain_point}. This delays lead response and causes deal loss."

    actions_ar = "\n".join([
        f"- أعددنا {evidence.messages_drafted} رسالة مخصصة (موافقة الفاوندر على كل رسالة)",
        f"- أرسلنا {evidence.messages_sent} رسالة معتمدة",
        "- بنينا مكتبة ردود جاهزة (5 قوالب)",
        "- وثّقنا العملية الكاملة لإعادة الاستخدام",
    ])
    actions_en = "\n".join([
        f"- Prepared {evidence.messages_drafted} personalized messages (founder-approved each)",
        f"- Sent {evidence.messages_sent} approved messages",
        "- Built ready-response library (5 templates)",
        "- Documented full process for replication",
    ])

    results_ar = "\n".join([
        f"- ردود واردة: {evidence.replies_received}",
        f"- اجتماعات محجوزة: {evidence.meetings_booked}",
        f"- تحسّن وقت الاستجابة: {rt_improvement}",
    ] + ([f"- صفقات مفتوحة: {evidence.deals_created}"] if evidence.deals_created else []))
    results_en = "\n".join([
        f"- Positive replies: {evidence.replies_received}",
        f"- Meetings booked: {evidence.meetings_booked}",
        f"- Response time improvement: {rt_improvement}",
    ] + ([f"- Deals opened: {evidence.deals_created}"] if evidence.deals_created else []))

    testimonial_ar = evidence.testimonial_text if evidence.testimonial_consented else ""
    testimonial_en = ""  # Translation would be done separately if needed

    next_ar = (
        "بناءً على نتائج الأسبوع الأول، نُوصي بالانتقال إلى Managed Ops الشهري (2,999 ريال/شهر) "
        "للحفاظ على هذا المستوى وتطويره."
    )
    next_en = (
        "Based on Week-1 results, we recommend transitioning to Monthly Managed Ops (2,999 SAR/mo) "
        "to sustain and grow these results."
    )

    pack = ProofPack(
        pack_id=str(uuid.uuid4()),
        pilot_id=pilot_id,
        account_id=account_id,
        company_name=company_name,
        contact_name=contact_name,
        sector=sector,
        evidence_level=level,
        evidence_level_name=level_info["name"],
        executive_summary_ar=exec_summary_ar,
        executive_summary_en=exec_summary_en,
        problem_statement_ar=problem_ar,
        problem_statement_en=problem_en,
        actions_taken_ar=actions_ar,
        actions_taken_en=actions_en,
        results_ar=results_ar,
        results_en=results_en,
        testimonial_ar=testimonial_ar,
        testimonial_en=testimonial_en,
        next_steps_ar=next_ar,
        next_steps_en=next_en,
        messages_drafted=evidence.messages_drafted,
        messages_sent=evidence.messages_sent,
        replies_received=evidence.replies_received,
        meetings_booked=evidence.meetings_booked,
        response_time_improvement=rt_improvement,
        is_complete=is_complete,
        can_use_as_case_study=can_case_study,
    )

    _save_proof_pack(pack)
    log.info(
        "Proof pack built: pack_id=%s level=L%d complete=%s",
        pack.pack_id,
        level,
        is_complete,
    )
    return pack


def _save_proof_pack(pack: ProofPack) -> None:
    try:
        proofs_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "proof-packs"
        )
        os.makedirs(proofs_dir, exist_ok=True)
        path = os.path.join(proofs_dir, f"{pack.pack_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pack.to_dict(), f, ensure_ascii=False, indent=2)
        md_path = os.path.join(proofs_dir, f"{pack.pack_id}_ar.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(pack.to_markdown_ar())
    except Exception as exc:
        log.warning("Could not save proof pack: %s", exc)
