"""Proof Stack Builder — multi-type proof assembly and gap analysis.

Builds comprehensive proof stacks from recorded events, scores completeness,
and identifies gaps for sales conversations and case-study publication.
Hard rule: only events explicitly provided are reflected — no fabrication.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from auto_client_acquisition.proof_engine.evidence import EvidenceLevel


class ProofType(StrEnum):
    PAYMENT = "payment"             # Payment confirmation — strongest trust signal
    METRIC = "metric"               # Quantified before/after metrics
    DELIVERY = "delivery"           # Documented deliverable completion
    ROI = "roi"                     # Return on investment proof
    BEFORE_AFTER = "before_after"   # Before/after state comparison
    SOCIAL = "social"               # Client testimonials / quotes
    PROCESS = "process"             # Documented process proof (how we work)
    AUTHORITY = "authority"         # Third-party validation / awards


@dataclass(frozen=True, slots=True)
class ProofAsset:
    """A single proof asset in the stack."""

    proof_type: ProofType
    label_ar: str
    label_en: str
    evidence_level: int         # EvidenceLevel int value
    is_available: bool
    is_publishable: bool        # Meets L4+ publish gate
    gap_detail_ar: str          # What's missing when not available
    gap_detail_en: str
    weight: int                 # Contribution to completeness score


@dataclass
class ProofStack:
    """Complete proof stack for an account."""

    account_id: str
    assets: tuple[ProofAsset, ...]
    completeness_score: int         # 0-100 overall
    publishable_score: int          # 0-100 for public use
    private_sales_score: int        # 0-100 for L3+ private sales use
    gaps_ar: tuple[str, ...]
    gaps_en: tuple[str, ...]
    recommended_next_event_ar: str
    recommended_next_event_en: str
    is_ready_for_case_study: bool   # publishable_score >= 60
    is_ready_for_private_sales: bool  # private_sales_score >= 40


# Weights must sum to 100
_PROOF_WEIGHTS: dict[ProofType, int] = {
    ProofType.PAYMENT: 25,
    ProofType.METRIC: 20,
    ProofType.DELIVERY: 15,
    ProofType.ROI: 15,
    ProofType.BEFORE_AFTER: 10,
    ProofType.SOCIAL: 8,
    ProofType.PROCESS: 4,
    ProofType.AUTHORITY: 3,
}

assert sum(_PROOF_WEIGHTS.values()) == 100, "Proof weights must sum to 100"

# Event type → ProofType mapping
_EVENT_TO_PROOF_TYPE: dict[str, ProofType] = {
    "payment_confirmed": ProofType.PAYMENT,
    "deliverable_completed": ProofType.DELIVERY,
    "diagnostic_delivered": ProofType.DELIVERY,
    "proof_pack_assembled": ProofType.METRIC,
    "expansion_offered": ProofType.ROI,
    "demo_booked": ProofType.PROCESS,
}

# Gap descriptions by proof type
_GAP_TO_NEXT_EVENT: dict[ProofType, tuple[str, str]] = {
    ProofType.PAYMENT: (
        "أكمل خطوة الدفع أو سجّل تأكيد الفاتورة",
        "Complete payment step or log invoice confirmation",
    ),
    ProofType.METRIC: (
        "سجّل حدث قياس نتيجة مع قيم قبل/بعد",
        "Log a result measurement event with before/after values",
    ),
    ProofType.DELIVERY: (
        "سجّل تسليم المخرج وأرسله للعميل",
        "Log deliverable completion and send to client",
    ),
    ProofType.ROI: (
        "احسب ROI مع العميل وسجّل في جلسة قياس القيمة",
        "Calculate ROI with client and log in a value measurement session",
    ),
    ProofType.BEFORE_AFTER: (
        "اجمع baseline بداية المشروع ووثّق حالة ما قبل",
        "Collect project baseline and document pre-state",
    ),
    ProofType.SOCIAL: (
        "اطلب اقتباساً خاصاً من العميل بعد تسليم أول نتيجة",
        "Request a private quote from the client after first result delivery",
    ),
    ProofType.PROCESS: (
        "وثّق سير العمل الخاص بهذا العميل كدليل عملية",
        "Document the workflow for this client as a process proof",
    ),
    ProofType.AUTHORITY: (
        "اطلب من الشريك أو جهة ثالثة كتابة تقييم",
        "Request a partner or third party to write an assessment",
    ),
}


def _asset_from_event(event: dict[str, Any]) -> ProofAsset | None:
    event_type = str(event.get("event_type", ""))
    proof_type = _EVENT_TO_PROOF_TYPE.get(event_type)
    if proof_type is None:
        return None

    evidence_level = int(event.get("evidence_level", 0))
    consent = str(event.get("consent_status", "internal_only"))
    approval = str(event.get("approval_status", "pending"))

    is_publishable = (
        evidence_level >= EvidenceLevel.L4_PUBLIC_APPROVED
        and consent == "granted"
        and approval == "approved"
    )

    return ProofAsset(
        proof_type=proof_type,
        label_ar=f"حدث: {event_type}",
        label_en=f"Event: {event_type}",
        evidence_level=evidence_level,
        is_available=True,
        is_publishable=is_publishable,
        gap_detail_ar="",
        gap_detail_en="",
        weight=_PROOF_WEIGHTS[proof_type],
    )


def _missing_asset(proof_type: ProofType) -> ProofAsset:
    gap_ar, gap_en = _GAP_TO_NEXT_EVENT[proof_type]
    return ProofAsset(
        proof_type=proof_type,
        label_ar=f"مطلوب: {proof_type.value}",
        label_en=f"Missing: {proof_type.value}",
        evidence_level=0,
        is_available=False,
        is_publishable=False,
        gap_detail_ar=gap_ar,
        gap_detail_en=gap_en,
        weight=_PROOF_WEIGHTS[proof_type],
    )


def build_proof_stack(
    account_id: str,
    events: list[dict[str, Any]],
) -> ProofStack:
    """Build a complete proof stack from recorded proof events.

    Args:
        account_id: Account/tenant identifier.
        events: List of proof event dicts with event_type, evidence_level, etc.

    Returns:
        ProofStack with completeness scores and gap analysis.
    """
    available_assets: list[ProofAsset] = []
    available_types: set[ProofType] = set()

    for event in events:
        asset = _asset_from_event(event)
        if asset is not None and asset.proof_type not in available_types:
            available_assets.append(asset)
            available_types.add(asset.proof_type)

    missing_assets = [
        _missing_asset(pt) for pt in ProofType if pt not in available_types
    ]
    all_assets = tuple(available_assets + missing_assets)

    completeness = min(100, sum(a.weight for a in available_assets))
    publishable = min(100, sum(a.weight for a in available_assets if a.is_publishable))
    private_sales = min(
        100,
        sum(
            a.weight for a in available_assets
            if a.evidence_level >= EvidenceLevel.L3_CUSTOMER_APPROVED
        ),
    )

    gaps_ar = tuple(a.gap_detail_ar for a in missing_assets if a.gap_detail_ar)
    gaps_en = tuple(a.gap_detail_en for a in missing_assets if a.gap_detail_en)

    # Recommend biggest-weight missing gap
    if missing_assets:
        biggest_gap = max(missing_assets, key=lambda a: a.weight)
        next_ar, next_en = _GAP_TO_NEXT_EVENT[biggest_gap.proof_type]
    else:
        next_ar = "الـ Proof Stack مكتمل — جاهز للنشر"
        next_en = "Proof stack complete — ready to publish"

    return ProofStack(
        account_id=account_id,
        assets=all_assets,
        completeness_score=completeness,
        publishable_score=publishable,
        private_sales_score=private_sales,
        gaps_ar=gaps_ar,
        gaps_en=gaps_en,
        recommended_next_event_ar=next_ar,
        recommended_next_event_en=next_en,
        is_ready_for_case_study=publishable >= 60,
        is_ready_for_private_sales=private_sales >= 40,
    )


def score_proof_readiness(stack: ProofStack) -> dict[str, Any]:
    """Return a structured proof readiness report."""
    return {
        "account_id": stack.account_id,
        "completeness_score": stack.completeness_score,
        "publishable_score": stack.publishable_score,
        "private_sales_score": stack.private_sales_score,
        "is_ready_for_case_study": stack.is_ready_for_case_study,
        "is_ready_for_private_sales": stack.is_ready_for_private_sales,
        "total_available_assets": sum(1 for a in stack.assets if a.is_available),
        "total_missing_assets": sum(1 for a in stack.assets if not a.is_available),
        "recommended_next_event_ar": stack.recommended_next_event_ar,
        "recommended_next_event_en": stack.recommended_next_event_en,
        "gaps": list(stack.gaps_ar),
        "gaps_en": list(stack.gaps_en),
    }


__all__ = [
    "ProofAsset",
    "ProofStack",
    "ProofType",
    "build_proof_stack",
    "score_proof_readiness",
]
