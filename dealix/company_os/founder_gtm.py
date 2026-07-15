"""Founder-first GTM packet generation for Dealix operating on itself."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from dealix.company_os.company_directory import DirectoryCandidate
from dealix.company_os.negotiation_engine import NegotiationContext, build_negotiation_plan
from dealix.company_os.service_catalog import match_services


@dataclass(frozen=True)
class FounderTarget:
    company_id: str
    company_name: str
    city: str
    activity: str
    research_score: float
    source_ref: str
    service_matches: tuple[dict[str, Any], ...]
    primary_offer_id: str
    why_dealix_ar: str
    objections_ar: tuple[str, ...]
    discovery_questions_ar: tuple[str, ...]
    draft_ar: str
    approval_status: str
    external_action_allowed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _objections(activity: str) -> tuple[str, ...]:
    baseline = (
        "لدينا CRM أو نظام قائم، فما الإضافة؟",
        "هل لديكم دليل أن المشكلة من العملية وليست من الموظفين؟",
        "كيف تحمون البيانات ومن يملك صلاحية القرار؟",
        "ما النتيجة القابلة للقياس قبل أن نلتزم؟",
    )
    value = activity.casefold()
    if any(token in value for token in ("مقاول", "مصنع", "نقل", "صيانة")):
        return baseline + ("هل يتكامل Dealix مع التشغيل الميداني ولا يضيف عبئًا جديدًا؟",)
    if any(token in value for token in ("عيادة", "طبي", "مستشفى")):
        return baseline + ("كيف تتعاملون مع الخصوصية والحالات الطبية الحساسة؟",)
    return baseline + ("لماذا لا نوظف شخصًا أو نستخدم أداة أرخص؟",)


def _why_dealix(candidate: DirectoryCandidate, matches: tuple[dict[str, Any], ...]) -> str:
    names = "، ".join(item["name_ar"] for item in matches[:3])
    return (
        f"لأن نشاط {candidate.company_name} ({candidate.activity or 'غير محدد'}) يمكن خدمته "
        f"بمسار متدرج يجمع {names}. Dealix لا يستبدل الأنظمة القائمة؛ يضيف طبقة "
        "بحث وقرار ومتابعة وموافقة وإثبات فوقها، ثم يوسع الأتمتة فقط بعد إثبات خط الأساس."
    )


def _draft(candidate: DirectoryCandidate, primary: dict[str, Any]) -> str:
    return (
        f"السلام عليكم، أعددنا فرضية بحثية أولية لشركة {candidate.company_name} بناءً على "
        f"نشاطها المعلن في {candidate.city or 'السعودية'}. أقرب نقطة بداية هي "
        f"{primary['name_ar']} لأنها تساعد على {primary['value_outcomes'][0]} دون تغيير "
        "الأنظمة الحالية أو أي التزام كبير. هذه مسودة داخلية؛ قبل التواصل نحتاج إثبات "
        "العلاقة والقناة وموافقة المؤسس."
    )


def build_founder_target(candidate: DirectoryCandidate) -> FounderTarget:
    matches = match_services(
        activity=candidate.activity,
        city=candidate.city,
        company_name=candidate.company_name,
        signals=(candidate.value_angle_ar,),
        limit=4,
    )
    primary = matches[0]
    objections = _objections(candidate.activity)
    negotiation = build_negotiation_plan(
        NegotiationContext(
            account_name=candidate.company_name,
            offer_id=str(primary["offer_id"]),
            customer_problem=candidate.value_angle_ar,
            known_objections=objections,
            evidence_refs=(f"{candidate.source_sheet}:{candidate.source_row_number}",),
        )
    )
    return FounderTarget(
        company_id=candidate.id,
        company_name=candidate.company_name,
        city=candidate.city,
        activity=candidate.activity,
        research_score=candidate.research_priority_score,
        source_ref=f"{candidate.source_sheet}:{candidate.source_row_number}",
        service_matches=matches,
        primary_offer_id=str(primary["offer_id"]),
        why_dealix_ar=_why_dealix(candidate, matches),
        objections_ar=objections,
        discovery_questions_ar=negotiation.discovery_questions_ar,
        draft_ar=_draft(candidate, primary),
        approval_status="blocked_research_only",
        external_action_allowed=False,
    )


def build_founder_gtm_packet(
    candidates: Iterable[DirectoryCandidate],
    *,
    limit: int = 50,
) -> dict[str, Any]:
    selected = sorted(
        candidates,
        key=lambda item: (-item.research_priority_score, item.company_name),
    )[: max(1, min(limit, 500))]
    targets = tuple(build_founder_target(candidate) for candidate in selected)
    departments = sorted(
        {
            match["department"]
            for target in targets
            for match in target.service_matches
        }
    )
    return {
        "mode": "founder_first_draft_only",
        "client": "dealix",
        "target_count": len(targets),
        "departments_covered": departments,
        "targets": [target.to_dict() for target in targets],
        "approval_queue": [
            {
                "company_id": target.company_id,
                "company_name": target.company_name,
                "action": "review_research_and_choose_allowed_channel",
                "status": target.approval_status,
                "external_action_allowed": False,
            }
            for target in targets
        ],
        "proof_ledger": [
            {
                "company_id": target.company_id,
                "source_ref": target.source_ref,
                "research_score": target.research_score,
                "offer_ids": [item["offer_id"] for item in target.service_matches],
            }
            for target in targets
        ],
        "global_rules": [
            "no_live_outbound",
            "no_cold_whatsapp",
            "no_mass_linkedin_automation",
            "no_consent_inference",
            "no_fake_proof",
            "no_guaranteed_outcomes",
            "founder_approval_required",
        ],
        "external_actions_performed": 0,
    }
