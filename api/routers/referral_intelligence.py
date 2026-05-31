"""Referral Intelligence API — referral tracking and program management.

Tracks referrals submitted by existing clients, their conversion status,
and incentive payouts. All outreach to referred companies requires explicit
founder approval before any contact is made (APPROVAL_FIRST doctrine).

Endpoints:
  GET  /api/v1/referral-intelligence/dashboard          — program overview
  GET  /api/v1/referral-intelligence/all                — all referrals (filterable)
  GET  /api/v1/referral-intelligence/by-referrer/{id}   — referrals from one client
  POST /api/v1/referral-intelligence/register           — register a new referral
  GET  /api/v1/referral-intelligence/program-terms      — bilingual program rules

All endpoints require admin auth (ADMIN-GATED).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/referral-intelligence",
    tags=["referral-intelligence"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


# ---------------------------------------------------------------------------
# Demo referral data — 10 referrals from 5 referrers
# ---------------------------------------------------------------------------

_REFERRALS: list[dict[str, Any]] = [
    {
        "referral_id": "REF-INTEL-001",
        "referrer_client_id": "CLT-001",
        "referred_company_ar": "شركة الأفق للتقنية",
        "referred_company_en": "Al Ufuq Technology Co",
        "sector": "technology",
        "city": "riyadh",
        "status": "converted",
        "referred_at": "2026-02-10T09:00:00Z",
        "converted_value_sar": 14_997,
        "incentive_sar": 1_500,
    },
    {
        "referral_id": "REF-INTEL-002",
        "referrer_client_id": "CLT-001",
        "referred_company_ar": "مجموعة الرياض للخدمات اللوجستية",
        "referred_company_en": "Riyadh Logistics Group",
        "sector": "logistics",
        "city": "riyadh",
        "status": "qualified",
        "referred_at": "2026-03-05T10:00:00Z",
        "converted_value_sar": 0,
        "incentive_sar": 0,
    },
    {
        "referral_id": "REF-INTEL-003",
        "referrer_client_id": "CLT-002",
        "referred_company_ar": "تقنيات البناء الحديث",
        "referred_company_en": "Modern Construction Technologies",
        "sector": "construction",
        "city": "jeddah",
        "status": "converted",
        "referred_at": "2026-02-20T11:00:00Z",
        "converted_value_sar": 5_997,
        "incentive_sar": 600,
    },
    {
        "referral_id": "REF-INTEL-004",
        "referrer_client_id": "CLT-002",
        "referred_company_ar": "صحة بلس للرعاية الطبية",
        "referred_company_en": "Health Plus Medical Care",
        "sector": "healthcare",
        "city": "jeddah",
        "status": "qualified",
        "referred_at": "2026-03-15T08:00:00Z",
        "converted_value_sar": 0,
        "incentive_sar": 0,
    },
    {
        "referral_id": "REF-INTEL-005",
        "referrer_client_id": "CLT-003",
        "referred_company_ar": "شركة التمويل الذكي",
        "referred_company_en": "Smart Finance Company",
        "sector": "financial_services",
        "city": "riyadh",
        "status": "converted",
        "referred_at": "2026-01-28T09:30:00Z",
        "converted_value_sar": 47_988,
        "incentive_sar": 4_799,
    },
    {
        "referral_id": "REF-INTEL-006",
        "referrer_client_id": "CLT-003",
        "referred_company_ar": "مصنع الطاقة المتجددة",
        "referred_company_en": "Renewable Energy Factory",
        "sector": "energy",
        "city": "dammam",
        "status": "pending",
        "referred_at": "2026-05-20T14:00:00Z",
        "converted_value_sar": 0,
        "incentive_sar": 0,
    },
    {
        "referral_id": "REF-INTEL-007",
        "referrer_client_id": "CLT-004",
        "referred_company_ar": "شركة التوزيع الغذائي المتحدة",
        "referred_company_en": "United Food Distribution Co",
        "sector": "food_and_beverage",
        "city": "jeddah",
        "status": "qualified",
        "referred_at": "2026-04-10T10:30:00Z",
        "converted_value_sar": 0,
        "incentive_sar": 0,
    },
    {
        "referral_id": "REF-INTEL-008",
        "referrer_client_id": "CLT-004",
        "referred_company_ar": "خدمات الأمن الرقمي",
        "referred_company_en": "Digital Security Services",
        "sector": "cybersecurity",
        "city": "riyadh",
        "status": "lost",
        "referred_at": "2026-03-01T09:00:00Z",
        "converted_value_sar": 0,
        "incentive_sar": 0,
    },
    {
        "referral_id": "REF-INTEL-009",
        "referrer_client_id": "CLT-005",
        "referred_company_ar": "مجموعة التعليم المتقدم",
        "referred_company_en": "Advanced Education Group",
        "sector": "education",
        "city": "khobar",
        "status": "qualified",
        "referred_at": "2026-04-25T13:00:00Z",
        "converted_value_sar": 0,
        "incentive_sar": 0,
    },
    {
        "referral_id": "REF-INTEL-010",
        "referrer_client_id": "CLT-005",
        "referred_company_ar": "شركة الاستشارات الهندسية",
        "referred_company_en": "Engineering Consulting Company",
        "sector": "professional_services",
        "city": "riyadh",
        "status": "pending",
        "referred_at": "2026-05-28T16:00:00Z",
        "converted_value_sar": 0,
        "incentive_sar": 0,
    },
]

_REQUIRED_REFERRAL_FIELDS: tuple[str, ...] = (
    "referral_id",
    "referrer_client_id",
    "referred_company_ar",
    "referred_company_en",
    "sector",
    "city",
    "status",
    "referred_at",
    "converted_value_sar",
    "incentive_sar",
)

_VALID_STATUSES: frozenset[str] = frozenset({"pending", "qualified", "converted", "lost"})

# ---------------------------------------------------------------------------
# Pure-function helpers
# ---------------------------------------------------------------------------


def _compute_conversion_rate(referrals: list[dict[str, Any]]) -> float:
    """Return the conversion rate as a float between 0.0 and 1.0."""
    if not referrals:
        return 0.0
    converted = sum(1 for r in referrals if r["status"] == "converted")
    return round(converted / len(referrals), 4)


def _compute_total_incentives(referrals: list[dict[str, Any]]) -> int:
    """Return the total incentives paid across all converted referrals."""
    return sum(r["incentive_sar"] for r in referrals)


def _find_best_referrer(referrals: list[dict[str, Any]]) -> str | None:
    """Return the referrer_client_id with the most converted referrals."""
    counts: dict[str, int] = {}
    for r in referrals:
        if r["status"] == "converted":
            counts[r["referrer_client_id"]] = counts.get(r["referrer_client_id"], 0) + 1
    if not counts:
        return None
    return max(counts, key=lambda k: counts[k])


def _sort_by_date_desc(referrals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return referrals sorted by referred_at descending."""
    return sorted(referrals, key=lambda r: r["referred_at"], reverse=True)


def _generate_referral_id() -> str:
    """Generate a sequential referral ID for new registrations."""
    return f"REF-INTEL-{len(_REFERRALS) + 1:03d}"


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------


class RegisterReferralBody(BaseModel):
    referrer_client_id: str = Field(min_length=3, max_length=50)
    referred_company_ar: str = Field(min_length=2, max_length=100)
    referred_company_en: str = Field(min_length=2, max_length=100)
    sector: str = Field(min_length=2, max_length=50)
    city: str = Field(min_length=2, max_length=50)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/dashboard")
async def get_dashboard() -> dict[str, Any]:
    """Referral program overview: conversion rate, incentives, best referrer.

    Aggregates all referral activity into a single summary view for the
    founder. Governance gate: ALLOW_WITH_REVIEW.
    """
    conversion_rate = _compute_conversion_rate(_REFERRALS)
    total_incentives = _compute_total_incentives(_REFERRALS)
    best_referrer = _find_best_referrer(_REFERRALS)

    converted = [r for r in _REFERRALS if r["status"] == "converted"]
    qualified = [r for r in _REFERRALS if r["status"] == "qualified"]
    pending = [r for r in _REFERRALS if r["status"] == "pending"]
    lost = [r for r in _REFERRALS if r["status"] == "lost"]

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "total_referrals": len(_REFERRALS),
        "conversion_rate": conversion_rate,
        "conversion_rate_pct": round(conversion_rate * 100, 1),
        "converted_count": len(converted),
        "qualified_count": len(qualified),
        "pending_count": len(pending),
        "lost_count": len(lost),
        "total_incentives_earned_sar": total_incentives,
        "total_converted_value_sar": sum(r["converted_value_sar"] for r in converted),
        "best_referrer": best_referrer,
        "unique_referrers": len({r["referrer_client_id"] for r in _REFERRALS}),
        "note_ar": "لا يتم التواصل مع أي شركة مُحالة دون موافقة صريحة من المؤسس",
        "note_en": "No outreach is made to any referred company without explicit founder approval",
    }


@router.get("/all")
async def get_all_referrals(
    status: str | None = Query(default=None, description="Filter by status: pending|qualified|converted|lost"),
) -> dict[str, Any]:
    """All referrals sorted by date descending, optionally filtered by status.

    Accepts an optional ?status= query parameter. Returns referrals sorted
    newest first. Governance gate: ALLOW_WITH_REVIEW.
    """
    referrals = list(_REFERRALS)

    if status is not None:
        if status not in _VALID_STATUSES:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status '{status}'. Must be one of: {sorted(_VALID_STATUSES)}",
            )
        referrals = [r for r in referrals if r["status"] == status]

    sorted_referrals = _sort_by_date_desc(referrals)

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "total": len(sorted_referrals),
        "filter_status": status,
        "referrals": sorted_referrals,
    }


@router.get("/by-referrer/{referrer_client_id}")
async def get_by_referrer(referrer_client_id: str) -> dict[str, Any]:
    """All referrals submitted by a specific client.

    Returns 404 if no referrals are found for the given referrer_client_id.
    Governance gate: ALLOW_WITH_REVIEW.
    """
    referrals = [r for r in _REFERRALS if r["referrer_client_id"] == referrer_client_id]

    if not referrals:
        raise HTTPException(
            status_code=404,
            detail=f"No referrals found for referrer {referrer_client_id}",
        )

    sorted_referrals = _sort_by_date_desc(referrals)
    converted = [r for r in referrals if r["status"] == "converted"]
    total_incentives = _compute_total_incentives(referrals)

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "referrer_client_id": referrer_client_id,
        "total_referrals": len(referrals),
        "converted_count": len(converted),
        "conversion_rate": _compute_conversion_rate(referrals),
        "total_incentives_earned_sar": total_incentives,
        "referrals": sorted_referrals,
    }


@router.post("/register")
async def register_referral(body: RegisterReferralBody = Body(...)) -> dict[str, Any]:
    """Register a new referral from an existing client.

    The referred company will NOT be contacted until the founder explicitly
    approves the referral. This enforces the NO_COLD_WHATSAPP and
    APPROVAL_FIRST doctrine — no automated or cold outreach will be sent.

    Governance decision: APPROVAL_FIRST.
    """
    new_referral: dict[str, Any] = {
        "referral_id": _generate_referral_id(),
        "referrer_client_id": body.referrer_client_id,
        "referred_company_ar": body.referred_company_ar,
        "referred_company_en": body.referred_company_en,
        "sector": body.sector,
        "city": body.city,
        "status": "pending",
        "referred_at": _now_iso(),
        "converted_value_sar": 0,
        "incentive_sar": 0,
    }
    _REFERRALS.append(new_referral)

    _log.info(
        "referral_registered",
        referral_id=new_referral["referral_id"],
        referrer=body.referrer_client_id,
        company_en=body.referred_company_en,
    )

    return {
        "governance_decision": "APPROVAL_FIRST",
        "generated_at": _now_iso(),
        "referral_id": new_referral["referral_id"],
        "status": "pending",
        "status_ar": "قيد الانتظار — يتطلب موافقة المؤسس قبل أي تواصل",
        "status_en": "Pending — awaiting founder approval before any outreach",
        "no_cold_outreach_note_ar": (
            "لن يتم التواصل مع الشركة المُحالة بأي شكل — واتساب أو بريد إلكتروني أو غيره "
            "— حتى يوافق المؤسس صراحةً على هذا الإحالة."
        ),
        "no_cold_outreach_note_en": (
            "NO outreach will be made to the referred company via any channel "
            "— WhatsApp, email, or otherwise — until the founder explicitly approves "
            "this referral. Cold contact is prohibited."
        ),
        "next_step_ar": "على المؤسس مراجعة هذا الإحالة والموافقة عليها قبل البدء بأي تواصل",
        "next_step_en": "Founder must review and approve this referral before any contact is initiated",
        "referred_company_en": body.referred_company_en,
        "referred_company_ar": body.referred_company_ar,
        "referrer_client_id": body.referrer_client_id,
    }


@router.get("/program-terms")
async def get_program_terms() -> dict[str, Any]:
    """Referral program rules: incentive structure, eligibility, payout timing.

    Returns bilingual (Arabic and English) program terms. Governance gate:
    ALLOW_WITH_REVIEW.
    """
    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "program_version": "2.0",
        "effective_date": "2026-01-01",
        "incentive_structure": {
            "incentive_structure_ar": "10% من قيمة أول صفقة مع الشركة المُحالة",
            "incentive_structure_en": "10% of the first deal value with the referred company",
            "calculation_basis_ar": "قيمة العقد الأول المدفوع فعلياً",
            "calculation_basis_en": "Actual paid value of the first contract",
            "minimum_deal_sar": 499,
            "maximum_incentive_sar": 10_000,
            "example_ar": "صفقة بقيمة 5,000 ريال = حافز 500 ريال",
            "example_en": "A 5,000 SAR deal yields a 500 SAR incentive",
        },
        "eligibility": {
            "eligibility_ar": "المؤهلية للبرنامج",
            "eligibility_en": "Program eligibility",
            "rules_ar": [
                "يجب أن يكون المُحيل عميلاً نشطاً حالياً لدى Dealix",
                "يجب أن تكون الشركة المُحالة شركة سعودية B2B غير مسجلة لدى Dealix",
                "الإحالات الذاتية غير مقبولة",
                "لا يُسمح بأكثر من 5 إحالات نشطة في نفس الوقت لكل عميل",
            ],
            "rules_en": [
                "Referrer must be a currently active Dealix client",
                "Referred company must be a Saudi B2B not already registered with Dealix",
                "Self-referrals are not accepted",
                "No more than 5 active referrals per client at any time",
            ],
        },
        "payout_timing": {
            "payout_timing_ar": "توقيت صرف الحوافز",
            "payout_timing_en": "Incentive payout timing",
            "trigger_ar": "بعد سداد الفاتورة الأولى من الشركة المُحالة",
            "trigger_en": "After the referred company pays their first invoice",
            "method_ar": "خصم من فاتورة الاشتراك القادمة للمُحيل",
            "method_en": "Deducted from the referrer's next subscription invoice",
            "processing_days": 7,
        },
        "approval_requirement": {
            "approval_requirement_ar": "شرط الموافقة المسبقة",
            "approval_requirement_en": "Prior approval requirement",
            "note_ar": (
                "يجب على المؤسس الموافقة على كل إحالة قبل أي تواصل مع الشركة المُحالة. "
                "لا يتم التواصل البارد بأي شكل."
            ),
            "note_en": (
                "The founder must approve each referral before any outreach to the referred company. "
                "No cold outreach is permitted under any circumstances."
            ),
        },
        "contact_ar": "للاستفسار عن حالة إحالتك، تواصل مع فريق Dealix عبر القناة المعتمدة",
        "contact_en": "For referral status inquiries, contact the Dealix team via the approved channel",
    }
