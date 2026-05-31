"""Partner referral program framework for Dealix Saudi B2B.

Defines partner tiers, onboarding steps, commission rules, and earnings
calculator. All data is static; no LLM or external API calls are made.
All generated assessments carry a mandatory governance decision.

Prefix: /api/v1/partner-referral
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/partner-referral",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: partner tiers
# ---------------------------------------------------------------------------

_PARTNER_TIERS: list[dict[str, Any]] = [
    {
        "tier_id": "associate",
        "tier_name_en": "Associate Partner",
        "tier_name_ar": "شريك مساعد",
        "referral_fee_pct": 5.0,
        "requirements_en": [
            "Complete the Dealix partner onboarding programme.",
            "Submit at least one qualified lead per quarter.",
        ],
        "requirements_ar": [
            "إتمام برنامج تأهيل الشركاء لدى ديليكس.",
            "تقديم عميل محتمل مؤهل واحد على الأقل كل ربع سنة.",
        ],
        "annual_quota_sar": 50_000,
    },
    {
        "tier_id": "silver",
        "tier_name_en": "Silver Partner",
        "tier_name_ar": "شريك فضي",
        "referral_fee_pct": 10.0,
        "requirements_en": [
            "Maintain a minimum pipeline of SAR 50,000 annually.",
            "Complete advanced product certification within 60 days.",
        ],
        "requirements_ar": [
            "الحفاظ على حد أدنى من خط الأنابيب يبلغ 50,000 ريال سنوياً.",
            "إتمام شهادة المنتج المتقدمة خلال 60 يوماً.",
        ],
        "annual_quota_sar": 150_000,
    },
    {
        "tier_id": "gold",
        "tier_name_en": "Gold Partner",
        "tier_name_ar": "شريك ذهبي",
        "referral_fee_pct": 15.0,
        "requirements_en": [
            "Achieve annual referral revenue of SAR 150,000 or more.",
            "Assign a dedicated account manager for joint pipeline reviews.",
        ],
        "requirements_ar": [
            "تحقيق إيرادات إحالة سنوية بقيمة 150,000 ريال أو أكثر.",
            "تعيين مدير حساب مخصص لمراجعات خط الأنابيب المشترك.",
        ],
        "annual_quota_sar": 500_000,
    },
]

# ---------------------------------------------------------------------------
# Static data: partner onboarding steps
# ---------------------------------------------------------------------------

_PARTNER_ONBOARDING_STEPS: list[dict[str, Any]] = [
    {
        "order": 1,
        "step_en": "Application Review",
        "step_ar": "مراجعة الطلب",
        "duration_days": 3,
        "owner_en": "Partnerships Team",
    },
    {
        "order": 2,
        "step_en": "Agreement Signing",
        "step_ar": "توقيع الاتفاقية",
        "duration_days": 2,
        "owner_en": "Legal and Partnerships",
    },
    {
        "order": 3,
        "step_en": "Portal Access",
        "step_ar": "الوصول إلى البوابة",
        "duration_days": 1,
        "owner_en": "IT Operations",
    },
    {
        "order": 4,
        "step_en": "Training",
        "step_ar": "التدريب",
        "duration_days": 5,
        "owner_en": "Partner Enablement",
    },
    {
        "order": 5,
        "step_en": "First Referral Target",
        "step_ar": "هدف الإحالة الأولى",
        "duration_days": 30,
        "owner_en": "Partner Account Manager",
    },
]

# ---------------------------------------------------------------------------
# Static data: referral commission rules
# ---------------------------------------------------------------------------

_REFERRAL_COMMISSION_RULES: list[dict[str, Any]] = [
    {
        "rule_en": "Commission is paid only after the referred customer completes payment.",
        "rule_ar": "تُصرف العمولة فقط بعد إتمام العميل المُحال للدفع.",
    },
    {
        "rule_en": "Only net-new logos qualify; existing Dealix customers are excluded.",
        "rule_ar": "تؤهل الشعارات الجديدة فحسب؛ عملاء ديليكس الحاليون مستثنون.",
    },
    {
        "rule_en": "Double-counting is not permitted; a referral may be credited to one partner only.",
        "rule_ar": "لا يُسمح بالازدواجية؛ تُنسب الإحالة لشريك واحد فقط.",
    },
    {
        "rule_en": "All commission payments are denominated in Saudi Riyals (SAR).",
        "rule_ar": "جميع مدفوعات العمولات مقومة بالريال السعودي (SAR).",
    },
]

# ---------------------------------------------------------------------------
# Valid partner tiers lookup
# ---------------------------------------------------------------------------

_VALID_PARTNER_TIERS: set[str] = {"associate", "silver", "gold"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ReferralEarningsInput(BaseModel):
    partner_tier: str
    referrals_closed: int = Field(..., ge=0)
    avg_deal_value_sar: float = Field(..., ge=0)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _calculate_referral_earnings(inp: ReferralEarningsInput) -> dict[str, Any]:
    """Compute estimated referral earnings for a partner.

    Returns a structured dict with gross_revenue, commission rate, estimated
    commission, quota attainment, and upgrade eligibility.
    """
    if inp.partner_tier not in _VALID_PARTNER_TIERS:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid partner_tier '{inp.partner_tier}'. "
                f"Valid values: {sorted(_VALID_PARTNER_TIERS)}"
            ),
        )

    tier_data = next(t for t in _PARTNER_TIERS if t["tier_id"] == inp.partner_tier)

    gross_revenue_generated_sar: float = inp.referrals_closed * inp.avg_deal_value_sar
    commission_rate_pct: float = tier_data["referral_fee_pct"]
    estimated_commission_sar: float = gross_revenue_generated_sar * (commission_rate_pct / 100)

    quota = tier_data["annual_quota_sar"]
    quota_attainment_pct: float = (
        min(gross_revenue_generated_sar / quota * 100, 100.0) if quota > 0 else 0.0
    )

    next_tier_upgrade_eligible: bool = (
        quota_attainment_pct >= 100 and inp.partner_tier != "gold"
    )

    return {
        "partner_tier": inp.partner_tier,
        "gross_revenue_generated_sar": gross_revenue_generated_sar,
        "commission_rate_pct": commission_rate_pct,
        "estimated_commission_sar": estimated_commission_sar,
        "quota_attainment_pct": quota_attainment_pct,
        "next_tier_upgrade_eligible": next_tier_upgrade_eligible,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/tiers", summary="All 3 partner tiers with bilingual labels")
def get_tiers() -> dict[str, Any]:
    """Return all partner tiers with requirements and fee percentages."""
    return {
        "tiers": _PARTNER_TIERS,
        "total_tiers": len(_PARTNER_TIERS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/onboarding-steps", summary="All 5 partner onboarding steps")
def get_onboarding_steps() -> dict[str, Any]:
    """Return all partner onboarding steps with duration and owner."""
    return {
        "onboarding_steps": _PARTNER_ONBOARDING_STEPS,
        "total_steps": len(_PARTNER_ONBOARDING_STEPS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/commission-rules", summary="All 4 referral commission rules")
def get_commission_rules() -> dict[str, Any]:
    """Return all referral commission rules with bilingual descriptions."""
    return {
        "commission_rules": _REFERRAL_COMMISSION_RULES,
        "total_rules": len(_REFERRAL_COMMISSION_RULES),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/calculate-earnings", summary="Calculate estimated referral earnings")
def calculate_earnings(body: ReferralEarningsInput) -> dict[str, Any]:
    """Accept partner tier and referral data; return estimated commission.

    Governance decision: APPROVAL_FIRST.
    """
    return _calculate_referral_earnings(body)
