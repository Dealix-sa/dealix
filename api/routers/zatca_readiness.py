"""ZATCA Readiness Assessment API — Saudi e-invoicing compliance scoring.

Endpoints:
  POST /api/v1/zatca-readiness/assess        — score a company's ZATCA readiness
  GET  /api/v1/zatca-readiness/checklist     — full ZATCA Phase 2 compliance checklist
  GET  /api/v1/zatca-readiness/waves         — all ZATCA wave deadlines
  GET  /api/v1/zatca-readiness/penalties     — penalty structure for non-compliance
  POST /api/v1/zatca-readiness/invoice-check — validate a single invoice format

All endpoints:
  - Open (no admin auth — lead generation tool)
  - governance_decision: ALLOW_WITH_REVIEW
  - Bilingual ar/en
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from fastapi import APIRouter, Body
from pydantic import BaseModel, ConfigDict, Field

_NOW = datetime.now(UTC)

router = APIRouter(
    prefix="/api/v1/zatca-readiness",
    tags=["zatca-readiness"],
)

_GOV = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# ZATCA Wave data (Saudi Arabia 2022-2026)
# ---------------------------------------------------------------------------

ZATCA_WAVES: list[dict[str, Any]] = [
    {
        "wave": 1,
        "deadline": "2023-01-01",
        "companies_ar": "إيرادات +3 مليار SAR",
        "companies_en": "Companies with +SAR 3 billion revenue",
        "status": "completed",
        "phase": "Integration",
    },
    {
        "wave": 2,
        "deadline": "2023-07-01",
        "companies_ar": "إيرادات +500 مليون SAR",
        "companies_en": "Companies with +SAR 500 million revenue",
        "status": "completed",
        "phase": "Integration",
    },
    {
        "wave": 3,
        "deadline": "2023-10-01",
        "companies_ar": "إيرادات +250 مليون SAR",
        "companies_en": "Companies with +SAR 250 million revenue",
        "status": "completed",
        "phase": "Integration",
    },
    {
        "wave": 4,
        "deadline": "2024-11-01",
        "companies_ar": "إيرادات +150 مليون SAR",
        "companies_en": "Companies with +SAR 150 million revenue",
        "status": "completed",
        "phase": "Integration",
    },
    {
        "wave": 5,
        "deadline": "2025-01-01",
        "companies_ar": "إيرادات +40 مليون SAR",
        "companies_en": "Companies with +SAR 40 million revenue",
        "status": "completed",
        "phase": "Integration",
    },
    {
        "wave": 6,
        "deadline": "2025-04-01",
        "companies_ar": "إيرادات +7 مليون SAR",
        "companies_en": "Companies with +SAR 7 million revenue",
        "status": "completed",
        "phase": "Integration",
    },
    {
        "wave": 7,
        "deadline": "2025-10-01",
        "companies_ar": "إيرادات +3 مليون SAR",
        "companies_en": "Companies with +SAR 3 million revenue",
        "status": "active",
        "phase": "Integration",
    },
    {
        "wave": 8,
        "deadline": "2026-04-01",
        "companies_ar": "إيرادات +1 مليون SAR",
        "companies_en": "Companies with +SAR 1 million revenue",
        "status": "upcoming",
        "phase": "Integration",
    },
    {
        "wave": 9,
        "deadline": "2026-10-01",
        "companies_ar": "جميع الشركات الخاضعة لضريبة القيمة المضافة",
        "companies_en": "All VAT-registered companies",
        "status": "upcoming",
        "phase": "Integration",
    },
]

# ---------------------------------------------------------------------------
# Checklist items
# ---------------------------------------------------------------------------

CHECKLIST: list[dict[str, Any]] = [
    {
        "id": "CK-001",
        "category": "technical",
        "title_ar": "شهادة CSID مسجّلة لدى ZATCA",
        "title_en": "CSID certificate registered with ZATCA",
        "weight": 20,
        "critical": True,
    },
    {
        "id": "CK-002",
        "category": "technical",
        "title_ar": "نظام الفوترة يدعم XML بمعيار UBL 2.1",
        "title_en": "Billing system supports XML in UBL 2.1 standard",
        "weight": 15,
        "critical": True,
    },
    {
        "id": "CK-003",
        "category": "technical",
        "title_ar": "QR code مُضمَّن في كل فاتورة",
        "title_en": "QR code embedded in every invoice",
        "weight": 15,
        "critical": True,
    },
    {
        "id": "CK-004",
        "category": "technical",
        "title_ar": "ختم رقمي على الفواتير الإلكترونية",
        "title_en": "Digital stamp on e-invoices",
        "weight": 10,
        "critical": True,
    },
    {
        "id": "CK-005",
        "category": "process",
        "title_ar": "تكامل API مع بوابة ZATCA (Fatoora)",
        "title_en": "API integration with ZATCA portal (Fatoora)",
        "weight": 15,
        "critical": True,
    },
    {
        "id": "CK-006",
        "category": "process",
        "title_ar": "إرسال الفواتير في الوقت الفعلي أو خلال 24 ساعة",
        "title_en": "Invoice submission in real-time or within 24 hours",
        "weight": 10,
        "critical": False,
    },
    {
        "id": "CK-007",
        "category": "data",
        "title_ar": "رقم ضريبي (TRN) صحيح في كل فاتورة",
        "title_en": "Correct Tax Registration Number (TRN) on every invoice",
        "weight": 5,
        "critical": False,
    },
    {
        "id": "CK-008",
        "category": "data",
        "title_ar": "معلومات المورد والعميل كاملة",
        "title_en": "Complete supplier and buyer information",
        "weight": 5,
        "critical": False,
    },
    {
        "id": "CK-009",
        "category": "process",
        "title_ar": "إجراءات التعامل مع رفض ZATCA للفواتير",
        "title_en": "Process for handling ZATCA invoice rejections",
        "weight": 3,
        "critical": False,
    },
    {
        "id": "CK-010",
        "category": "training",
        "title_ar": "تدريب الفريق المالي على اشتراطات ZATCA",
        "title_en": "Finance team trained on ZATCA requirements",
        "weight": 2,
        "critical": False,
    },
]

# ---------------------------------------------------------------------------
# Penalty structure
# ---------------------------------------------------------------------------

PENALTIES: list[dict[str, Any]] = [
    {
        "violation_ar": "عدم إصدار فاتورة ضريبية",
        "violation_en": "Not issuing a tax invoice",
        "penalty_sar": 1_000,
        "per": "invoice",
        "max_sar": 50_000,
    },
    {
        "violation_ar": "عدم الامتثال للمرحلة الثانية (التكامل)",
        "violation_en": "Non-compliance with Phase 2 (Integration)",
        "penalty_sar": 5_000,
        "per": "month",
        "max_sar": 50_000,
    },
    {
        "violation_ar": "فاتورة بمعلومات غير صحيحة",
        "violation_en": "Invoice with incorrect information",
        "penalty_sar": 1_000,
        "per": "invoice",
        "max_sar": 20_000,
    },
    {
        "violation_ar": "عدم إرسال الفاتورة للعميل",
        "violation_en": "Failure to send invoice to buyer",
        "penalty_sar": 1_000,
        "per": "invoice",
        "max_sar": 50_000,
    },
    {
        "violation_ar": "الاحتفاظ بسجلات غير كافية",
        "violation_en": "Insufficient record-keeping",
        "penalty_sar": 10_000,
        "per": "audit",
        "max_sar": 50_000,
    },
]


# ---------------------------------------------------------------------------
# Request/Response models
# ---------------------------------------------------------------------------

class ZATCAAssessBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str | None = Field(default=None, max_length=200)
    annual_revenue_sar: float | None = Field(default=None, ge=0)
    current_billing_system: str | None = Field(default=None, max_length=100)
    # Checklist answers — True = compliant, False = not compliant
    has_csid: bool = False
    has_xml_ubl: bool = False
    has_qr_code: bool = False
    has_digital_stamp: bool = False
    has_fatoora_integration: bool = False
    has_realtime_submission: bool = False
    has_correct_trn: bool = True
    has_complete_data: bool = True
    has_rejection_process: bool = False
    has_team_training: bool = False


class InvoiceCheckBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    has_xml_format: bool = False
    has_qr_code: bool = False
    has_digital_signature: bool = False
    has_uuid: bool = False
    has_trn_supplier: bool = True
    has_trn_buyer: bool = False
    has_line_items: bool = True
    invoice_type: str = Field(default="standard", pattern="^(standard|simplified|credit|debit)$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _determine_applicable_wave(revenue_sar: float | None) -> dict[str, Any] | None:
    """Return the earliest wave (lowest wave number) that applied to this company.

    Companies with higher revenue were subject to earlier (lower-numbered) waves.
    """
    if revenue_sar is None:
        return None
    _THRESHOLDS: dict[int, float] = {
        1: 3_000_000_000,
        2: 500_000_000,
        3: 250_000_000,
        4: 150_000_000,
        5: 40_000_000,
        6: 7_000_000,
        7: 3_000_000,
        8: 1_000_000,
        9: 0,
    }
    # Find the earliest (lowest-numbered) wave whose threshold ≤ revenue_sar
    wave_lookup = {w["wave"]: w for w in ZATCA_WAVES}
    for wave_num in sorted(_THRESHOLDS.keys()):
        if revenue_sar >= _THRESHOLDS[wave_num]:
            return wave_lookup.get(wave_num)
    return wave_lookup.get(9)  # catch-all


def _score_assessment(body: ZATCAAssessBody) -> dict[str, Any]:
    answers = {
        "CK-001": body.has_csid,
        "CK-002": body.has_xml_ubl,
        "CK-003": body.has_qr_code,
        "CK-004": body.has_digital_stamp,
        "CK-005": body.has_fatoora_integration,
        "CK-006": body.has_realtime_submission,
        "CK-007": body.has_correct_trn,
        "CK-008": body.has_complete_data,
        "CK-009": body.has_rejection_process,
        "CK-010": body.has_team_training,
    }
    total_weight = sum(item["weight"] for item in CHECKLIST)
    earned = sum(item["weight"] for item in CHECKLIST if answers.get(item["id"], False))
    score = round(earned / total_weight * 100)

    gaps = [
        {
            "id": item["id"],
            "title_ar": item["title_ar"],
            "title_en": item["title_en"],
            "critical": item["critical"],
            "weight": item["weight"],
        }
        for item in CHECKLIST
        if not answers.get(item["id"], False)
    ]
    critical_gaps = [g for g in gaps if g["critical"]]

    if score >= 85:
        tier = "compliant"
        tier_ar = "ممتثل"
        risk = "low"
    elif score >= 60:
        tier = "partial"
        tier_ar = "ممتثل جزئياً"
        risk = "medium"
    elif score >= 35:
        tier = "at_risk"
        tier_ar = "في خطر"
        risk = "high"
    else:
        tier = "non_compliant"
        tier_ar = "غير ممتثل"
        risk = "critical"

    return {
        "score": score,
        "tier": tier,
        "tier_ar": tier_ar,
        "risk_level": risk,
        "gaps": gaps,
        "critical_gaps": critical_gaps,
        "critical_gap_count": len(critical_gaps),
        "earned_weight": earned,
        "total_weight": total_weight,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/assess")
async def assess_zatca_readiness(body: ZATCAAssessBody = Body(...)) -> dict[str, Any]:
    """Score a company's ZATCA Phase 2 readiness (0-100)."""
    result = _score_assessment(body)
    applicable_wave = _determine_applicable_wave(body.annual_revenue_sar)

    recommendation = (
        "الشركة ممتثلة بالكامل — استمر في المراقبة الشهرية."
        if result["tier"] == "compliant"
        else (
            f"تم تحديد {result['critical_gap_count']} ثغرات حرجة — Sprint Dealix يُعالجها خلال 7 أيام."
            if result["critical_gap_count"] > 0
            else "ثغرات غير حرجة — يمكن معالجتها خلال 30 يوماً."
        )
    )

    recommendation_en = (
        "Company is fully compliant — continue monthly monitoring."
        if result["tier"] == "compliant"
        else (
            f"{result['critical_gap_count']} critical gaps identified — Dealix Sprint resolves them in 7 days."
            if result["critical_gap_count"] > 0
            else "Non-critical gaps — can be addressed within 30 days."
        )
    )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "company": body.company_name,
        "readiness_score": result["score"],
        "readiness_tier": {"id": result["tier"], "ar": result["tier_ar"]},
        "risk_level": result["risk_level"],
        "critical_gaps": result["critical_gaps"],
        "all_gaps": result["gaps"],
        "applicable_wave": applicable_wave,
        "recommendation": {"ar": recommendation, "en": recommendation_en},
        "next_step": {
            "offer_ar": "Sprint الامتثال ZATCA — 499 SAR / 7 أيام",
            "offer_en": "ZATCA Compliance Sprint — 499 SAR / 7 days",
            "cta": "/dealix-diagnostic",
        },
        "estimated_penalty_exposure_sar": (
            sum(p["penalty_sar"] for p in PENALTIES) * max(1, result["critical_gap_count"])
            if result["critical_gap_count"] > 0
            else 0
        ),
        "disclaimer_ar": "التقييم أداة توجيهية فقط — احصل على مراجعة رسمية من محاسب قانوني معتمد.",
        "disclaimer_en": "Assessment is a guidance tool only — obtain formal review from a certified accountant.",
    }


@router.get("/checklist")
async def get_zatca_checklist() -> dict[str, Any]:
    """Full ZATCA Phase 2 compliance checklist with weights."""
    by_category: dict[str, list[dict[str, Any]]] = {}
    for item in CHECKLIST:
        cat = item["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_items": len(CHECKLIST),
        "critical_items": sum(1 for i in CHECKLIST if i["critical"]),
        "checklist_by_category": by_category,
        "note_ar": "هذه القائمة تعكس متطلبات المرحلة الثانية من ZATCA (التكامل).",
        "note_en": "This checklist reflects Phase 2 ZATCA requirements (Integration phase).",
    }


@router.get("/waves")
async def get_zatca_waves() -> dict[str, Any]:
    """All ZATCA rollout waves with deadlines and applicability."""
    completed = [w for w in ZATCA_WAVES if w["status"] == "completed"]
    active = [w for w in ZATCA_WAVES if w["status"] == "active"]
    upcoming = [w for w in ZATCA_WAVES if w["status"] == "upcoming"]

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_waves": len(ZATCA_WAVES),
        "completed_count": len(completed),
        "active_count": len(active),
        "upcoming_count": len(upcoming),
        "waves": ZATCA_WAVES,
        "note_ar": "المواعيد النهائية للتكامل الإلزامي حسب حجم الإيرادات.",
        "note_en": "Mandatory integration deadlines by revenue size.",
    }


@router.get("/penalties")
async def get_zatca_penalties() -> dict[str, Any]:
    """ZATCA penalty structure for non-compliance."""
    total_max_exposure = sum(p["max_sar"] for p in PENALTIES)
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_penalty_items": len(PENALTIES),
        "max_total_exposure_sar": total_max_exposure,
        "penalties": PENALTIES,
        "note_ar": "الغرامات وفقاً للوائح هيئة الزكاة والضريبة والجمارك. قد تتغير.",
        "note_en": "Penalties per ZATCA regulations. Subject to change.",
        "disclaimer_ar": "استشر محاسباً قانونياً للحصول على تقييم دقيق لالتزاماتك.",
        "disclaimer_en": "Consult a certified accountant for accurate assessment of your obligations.",
    }


@router.post("/invoice-check")
async def check_invoice_compliance(body: InvoiceCheckBody = Body(...)) -> dict[str, Any]:
    """Validate a single invoice's compliance with ZATCA Phase 2 requirements."""
    checks = [
        ("xml_format", body.has_xml_format, "تنسيق XML (UBL 2.1)", "XML format (UBL 2.1)", True),
        ("qr_code", body.has_qr_code, "QR code مُضمَّن", "QR code embedded", True),
        ("digital_sig", body.has_digital_signature, "توقيع رقمي", "Digital signature", True),
        ("uuid", body.has_uuid, "UUID فريد", "Unique UUID", True),
        ("trn_supplier", body.has_trn_supplier, "TRN المورد", "Supplier TRN", True),
        ("trn_buyer", body.has_trn_buyer, "TRN المشتري", "Buyer TRN", body.invoice_type == "standard"),
        ("line_items", body.has_line_items, "بنود تفصيلية", "Line items", False),
    ]

    results = []
    passed = 0
    failed_critical = 0
    for check_id, value, ar_label, en_label, is_critical in checks:
        status = "pass" if value else "fail"
        if value:
            passed += 1
        elif is_critical:
            failed_critical += 1
        results.append({
            "check": check_id,
            "label_ar": ar_label,
            "label_en": en_label,
            "critical": is_critical,
            "status": status,
        })

    compliant = failed_critical == 0
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "invoice_type": body.invoice_type,
        "compliant": compliant,
        "checks_passed": passed,
        "checks_total": len(results),
        "critical_failures": failed_critical,
        "checks": results,
        "verdict_ar": "الفاتورة ممتثلة" if compliant else f"الفاتورة غير ممتثلة — {failed_critical} مشكلة حرجة",
        "verdict_en": "Invoice is compliant" if compliant else f"Invoice non-compliant — {failed_critical} critical issue(s)",
    }
