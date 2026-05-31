"""Contract intelligence and compliance review for Dealix Saudi B2B.

Provides standard clause library, Saudi contract requirements, risk matrix,
and a compliance review function. All data is static; no LLM or external
API calls are made.

Prefix: /api/v1/contract-intelligence
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/contract-intelligence",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: contract clauses
# ---------------------------------------------------------------------------

_CONTRACT_CLAUSES: list[dict[str, Any]] = [
    {
        "clause_id": "payment_terms",
        "clause_name_en": "Payment Terms",
        "clause_name_ar": "شروط الدفع",
        "risk_level": "medium",
        "negotiable": True,
        "dealix_standard_en": "Net-30 payment terms from invoice date.",
        "dealix_standard_ar": "شروط دفع صافي 30 يوماً من تاريخ الفاتورة.",
    },
    {
        "clause_id": "liability_cap",
        "clause_name_en": "Liability Cap",
        "clause_name_ar": "سقف المسؤولية",
        "risk_level": "high",
        "negotiable": True,
        "dealix_standard_en": "Total liability capped at 12 months of contract value.",
        "dealix_standard_ar": "الحد الأقصى للمسؤولية الإجمالية يعادل 12 شهراً من قيمة العقد.",
    },
    {
        "clause_id": "auto_renewal",
        "clause_name_en": "Auto-Renewal",
        "clause_name_ar": "التجديد التلقائي",
        "risk_level": "medium",
        "negotiable": True,
        "dealix_standard_en": "Contract auto-renews for 12 months unless cancelled 30 days before expiry.",
        "dealix_standard_ar": "يتجدد العقد تلقائياً لمدة 12 شهراً ما لم يتم إلغاؤه قبل 30 يوماً من انتهائه.",
    },
    {
        "clause_id": "data_ownership",
        "clause_name_en": "Data Ownership",
        "clause_name_ar": "ملكية البيانات",
        "risk_level": "high",
        "negotiable": False,
        "dealix_standard_en": "Client retains full ownership of all their data at all times.",
        "dealix_standard_ar": "يحتفظ العميل بالملكية الكاملة لجميع بياناته في جميع الأوقات.",
    },
    {
        "clause_id": "sla_uptime",
        "clause_name_en": "SLA Uptime Commitment",
        "clause_name_ar": "التزام وقت التشغيل في اتفاقية مستوى الخدمة",
        "risk_level": "medium",
        "negotiable": True,
        "dealix_standard_en": "99.5% monthly uptime guarantee with service credits for breaches.",
        "dealix_standard_ar": "ضمان وقت تشغيل شهري بنسبة 99.5% مع أرصدة خدمة عند الانتهاك.",
    },
    {
        "clause_id": "governing_law",
        "clause_name_en": "Governing Law",
        "clause_name_ar": "القانون الحاكم",
        "risk_level": "low",
        "negotiable": False,
        "dealix_standard_en": "Contract governed by the laws of the Kingdom of Saudi Arabia.",
        "dealix_standard_ar": "يخضع العقد لأنظمة المملكة العربية السعودية.",
    },
]

# ---------------------------------------------------------------------------
# Static data: Saudi contract requirements
# ---------------------------------------------------------------------------

_SAUDI_CONTRACT_REQUIREMENTS: list[dict[str, Any]] = [
    {
        "requirement_en": "An Arabic version of the contract is required.",
        "requirement_ar": "يجب توفير نسخة عربية من العقد.",
        "mandatory": True,
        "_flag_field": "includes_arabic_version",
    },
    {
        "requirement_en": "Contract must be governed by Saudi Arabian law.",
        "requirement_ar": "يجب أن يخضع العقد للقانون السعودي.",
        "mandatory": True,
        "_flag_field": None,
    },
    {
        "requirement_en": "A PDPL-compliant personal data protection clause is required.",
        "requirement_ar": "يجب تضمين بند حماية البيانات الشخصية المتوافق مع نظام حماية البيانات الشخصية.",
        "mandatory": True,
        "_flag_field": "has_pdpl_clause",
    },
    {
        "requirement_en": "A ZATCA compliance clause covering e-invoicing obligations is required.",
        "requirement_ar": "يجب تضمين بند الامتثال لهيئة الزكاة والضريبة والجمارك يغطي التزامات الفواتير الإلكترونية.",
        "mandatory": True,
        "_flag_field": "has_zatca_clause",
    },
    {
        "requirement_en": "A Vision 2030 alignment statement is recommended.",
        "requirement_ar": "يُوصى بتضمين بيان توافق مع رؤية 2030.",
        "mandatory": False,
        "_flag_field": None,
    },
]

# ---------------------------------------------------------------------------
# Static data: contract risk matrix
# ---------------------------------------------------------------------------

_CONTRACT_RISK_MATRIX: dict[str, Any] = {
    "high": {
        "risk_label_en": "High Risk",
        "risk_label_ar": "مخاطرة عالية",
        "mitigation_strategy_en": "Escalate to legal counsel for review before signature.",
        "mitigation_strategy_ar": "رفع الأمر إلى المستشار القانوني للمراجعة قبل التوقيع.",
    },
    "medium": {
        "risk_label_en": "Medium Risk",
        "risk_label_ar": "مخاطرة متوسطة",
        "mitigation_strategy_en": "Review with account manager and propose standard Dealix terms.",
        "mitigation_strategy_ar": "مراجعة مع مدير الحساب واقتراح شروط ديليكس القياسية.",
    },
    "low": {
        "risk_label_en": "Low Risk",
        "risk_label_ar": "مخاطرة منخفضة",
        "mitigation_strategy_en": "Accept as-is or apply minor editorial adjustments.",
        "mitigation_strategy_ar": "القبول كما هو أو إجراء تعديلات تحريرية طفيفة.",
    },
}

# ---------------------------------------------------------------------------
# Valid contract stages
# ---------------------------------------------------------------------------

_VALID_CONTRACT_STAGES: set[str] = {"draft", "review", "negotiation", "signed"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ContractReviewInput(BaseModel):
    contract_stage: str
    deal_value_sar: float = Field(..., ge=0)
    includes_arabic_version: bool = False
    has_pdpl_clause: bool = False
    has_zatca_clause: bool = False
    payment_terms_days: int = Field(default=30, ge=1)
    auto_renewal_included: bool = False


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _review_contract(inp: ContractReviewInput) -> dict[str, Any]:
    """Review a contract for Saudi compliance and flag risk areas.

    Returns compliance score (0-100), label, missing requirements, high-risk
    clauses, negotiable clauses, and a governance decision of APPROVAL_FIRST.
    """
    if inp.contract_stage not in _VALID_CONTRACT_STAGES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid contract_stage '{inp.contract_stage}'. "
                f"Valid values: {sorted(_VALID_CONTRACT_STAGES)}"
            ),
        )

    compliance_score = 0
    if inp.includes_arabic_version:
        compliance_score += 30
    if inp.has_pdpl_clause:
        compliance_score += 30
    if inp.has_zatca_clause:
        compliance_score += 30
    if inp.payment_terms_days <= 30:
        compliance_score += 10

    if compliance_score >= 90:
        compliance_label = "compliant"
    elif compliance_score >= 50:
        compliance_label = "partial"
    else:
        compliance_label = "non_compliant"

    missing_requirements: list[str] = []
    flag_map = {
        "includes_arabic_version": inp.includes_arabic_version,
        "has_pdpl_clause": inp.has_pdpl_clause,
        "has_zatca_clause": inp.has_zatca_clause,
    }
    for req in _SAUDI_CONTRACT_REQUIREMENTS:
        if not req["mandatory"]:
            continue
        flag_field = req.get("_flag_field")
        if flag_field is not None and not flag_map.get(flag_field, True):
            missing_requirements.append(req["requirement_en"])

    high_risk_clauses = [c for c in _CONTRACT_CLAUSES if c["risk_level"] == "high"]
    negotiable_clauses = [c for c in _CONTRACT_CLAUSES if c["negotiable"]]

    return {
        "contract_stage": inp.contract_stage,
        "deal_value_sar": inp.deal_value_sar,
        "compliance_score": compliance_score,
        "compliance_label": compliance_label,
        "missing_requirements": missing_requirements,
        "high_risk_clauses": high_risk_clauses,
        "negotiable_clauses": negotiable_clauses,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/clauses", summary="All 6 standard contract clauses")
def get_clauses() -> dict[str, Any]:
    """Return all contract clauses with risk level and negotiability."""
    return {
        "clauses": _CONTRACT_CLAUSES,
        "total_clauses": len(_CONTRACT_CLAUSES),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/saudi-requirements", summary="All 5 Saudi contract requirements")
def get_saudi_requirements() -> dict[str, Any]:
    """Return all Saudi-specific contract requirements with mandatory flags."""
    public_reqs = [
        {k: v for k, v in req.items() if k != "_flag_field"}
        for req in _SAUDI_CONTRACT_REQUIREMENTS
    ]
    return {
        "saudi_requirements": public_reqs,
        "total_requirements": len(public_reqs),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/review", summary="Review a contract for Saudi compliance")
def review_contract(body: ContractReviewInput) -> dict[str, Any]:
    """Accept contract metadata and return a compliance review.

    Governance decision: APPROVAL_FIRST.
    """
    return _review_contract(body)
