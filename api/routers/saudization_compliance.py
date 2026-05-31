"""
Saudi Nitaqat (Saudization) compliance checker.

Nitaqat is the Saudi Arabization / Saudization program enforced by
the Ministry of Human Resources and Social Development (MHRSD).
Companies are banded by industry and size; non-compliance restricts
ability to issue visas, renew business licenses, and access contracts.

Data based on publicly available MHRSD Nitaqat documentation.
Always verify against the official Nitaqat portal (nitaqat.gov.sa).
"""
from __future__ import annotations

import math
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator

router = APIRouter(prefix="/api/v1/saudization", tags=["Saudi Market"])

# ---------------------------------------------------------------------------
# Nitaqat band definitions
# ---------------------------------------------------------------------------

_BANDS: list[dict[str, Any]] = [
    {
        "band": "platinum",
        "label_ar": "البلاتيني",
        "label_en": "Platinum",
        "color": "#E5E4E2",
        "description_en": "Highest Saudization — significant incentives and expedited services.",
        "description_ar": "أعلى نسبة توطين — حوافز كبيرة وخدمات متسارعة.",
        "benefits": [
            "Priority visa processing",
            "Access to government incentive programs",
            "Preferred vendor status on government tenders",
            "Recognition on Monsha'at high-performance list",
        ],
        "restrictions": [],
    },
    {
        "band": "high_green",
        "label_ar": "الأخضر المرتفع",
        "label_en": "High Green",
        "color": "#228B22",
        "description_en": "Above target Saudization — full operating privileges.",
        "description_ar": "توطين فوق الهدف — امتيازات تشغيلية كاملة.",
        "benefits": [
            "Full visa issuance",
            "Can transfer visas from Yellow/Red companies",
            "Access to Kafalah and SME programs",
        ],
        "restrictions": [],
    },
    {
        "band": "medium_green",
        "label_ar": "الأخضر المتوسط",
        "label_en": "Medium Green",
        "color": "#32CD32",
        "description_en": "Meets Saudization target — standard operating status.",
        "description_ar": "يحقق هدف التوطين — وضع تشغيلي قياسي.",
        "benefits": [
            "Standard visa issuance",
            "Can hire from government employment portals",
        ],
        "restrictions": ["Cannot transfer visas to/from Yellow/Red companies"],
    },
    {
        "band": "low_green",
        "label_ar": "الأخضر المنخفض",
        "label_en": "Low Green",
        "color": "#90EE90",
        "description_en": "Marginally compliant — reduced visa privileges.",
        "description_ar": "ممتثل هامشياً — امتيازات تأشيرة مخفضة.",
        "benefits": ["Limited visa processing"],
        "restrictions": [
            "Reduced new visa allocations",
            "Cannot transfer visas from other companies",
        ],
    },
    {
        "band": "yellow",
        "label_ar": "الأصفر",
        "label_en": "Yellow",
        "color": "#FFD700",
        "description_en": "Below Saudization target — significant restrictions apply.",
        "description_ar": "أقل من هدف التوطين — قيود جوهرية سارية.",
        "benefits": [],
        "restrictions": [
            "No new work visa issuance",
            "Expat employees can transfer to Green/Platinum companies",
            "Cannot bid on many government contracts",
            "Restricted access to SME programs",
        ],
    },
    {
        "band": "red",
        "label_ar": "الأحمر",
        "label_en": "Red",
        "color": "#DC143C",
        "description_en": "Severely non-compliant — heavy restrictions, potential fines.",
        "description_ar": "غير ممتثل بشكل حاد — قيود صارمة وغرامات محتملة.",
        "benefits": [],
        "restrictions": [
            "All visa services suspended",
            "Cannot renew iqamas for existing expat employees",
            "Expat employees may transfer out freely",
            "Cannot renew Commercial Registration",
            "Subject to MHRSD inspection and fines",
        ],
    },
]

_BAND_ORDER = ["platinum", "high_green", "medium_green", "low_green", "yellow", "red"]

# ---------------------------------------------------------------------------
# Sector Nitaqat thresholds (% Saudi employees)
# Based on 2023 MHRSD published Nitaqat tables — small companies (5–49 emp)
# Actual thresholds vary by company size category and sub-sector.
# ---------------------------------------------------------------------------

_SECTOR_THRESHOLDS: dict[str, dict[str, Any]] = {
    "information_technology": {
        "name_ar": "تقنية المعلومات",
        "name_en": "Information Technology",
        "platinum_pct": 40,
        "high_green_pct": 30,
        "medium_green_pct": 22,
        "low_green_pct": 15,
        "yellow_pct": 8,
        "size_note": "Thresholds for 5–49 employees. Larger companies have higher thresholds.",
        "vision2030_note_en": "IT sector has Vision 2030 Saudization targets of 30% by 2025.",
        "vision2030_note_ar": "لقطاع تقنية المعلومات أهداف توطين رؤية 2030 بنسبة 30% بحلول 2025.",
    },
    "retail": {
        "name_ar": "تجارة التجزئة",
        "name_en": "Retail",
        "platinum_pct": 60,
        "high_green_pct": 50,
        "medium_green_pct": 40,
        "low_green_pct": 30,
        "yellow_pct": 20,
        "size_note": "Retail has high Saudization targets under the 2030 retail localization program.",
        "vision2030_note_en": "Retail is a priority Saudization sector under Vision 2030.",
        "vision2030_note_ar": "التجزئة قطاع توطين ذو أولوية في رؤية 2030.",
    },
    "construction": {
        "name_ar": "البناء والتشييد",
        "name_en": "Construction",
        "platinum_pct": 20,
        "high_green_pct": 14,
        "medium_green_pct": 10,
        "low_green_pct": 6,
        "yellow_pct": 3,
        "size_note": "Construction has lower thresholds due to skilled-labor scarcity.",
        "vision2030_note_en": "NEOM and giga-projects drive construction demand; Saudization targets rising.",
        "vision2030_note_ar": "نيوم والمشاريع العملاقة تدفع الطلب على البناء؛ أهداف التوطين ترتفع.",
    },
    "healthcare": {
        "name_ar": "الرعاية الصحية",
        "name_en": "Healthcare",
        "platinum_pct": 35,
        "high_green_pct": 25,
        "medium_green_pct": 18,
        "low_green_pct": 12,
        "yellow_pct": 6,
        "size_note": "Healthcare Saudization is prioritized under Vision 2030 privatization.",
        "vision2030_note_en": "Vision 2030 targets 35%+ Saudi healthcare workers by 2030.",
        "vision2030_note_ar": "تستهدف رؤية 2030 نسبة 35%+ من العاملين الصحيين السعوديين بحلول 2030.",
    },
    "financial_services": {
        "name_ar": "الخدمات المالية",
        "name_en": "Financial Services",
        "platinum_pct": 70,
        "high_green_pct": 60,
        "medium_green_pct": 50,
        "low_green_pct": 40,
        "yellow_pct": 30,
        "size_note": "Financial services has the highest Saudization targets in Saudi Arabia.",
        "vision2030_note_en": "SAMA targets near-100% Saudization in core banking roles.",
        "vision2030_note_ar": "تستهدف مؤسسة النقد توطيناً شبه كامل في الأدوار المصرفية الجوهرية.",
    },
    "hospitality": {
        "name_ar": "الضيافة والسياحة",
        "name_en": "Hospitality & Tourism",
        "platinum_pct": 30,
        "high_green_pct": 22,
        "medium_green_pct": 16,
        "low_green_pct": 10,
        "yellow_pct": 5,
        "size_note": "Emerging sector — thresholds expected to rise as Saudi Tourism Authority expands.",
        "vision2030_note_en": "Tourism is a high-priority Vision 2030 sector with growing Saudization targets.",
        "vision2030_note_ar": "السياحة قطاع ذو أولوية قصوى في رؤية 2030 مع أهداف توطين متنامية.",
    },
    "manufacturing": {
        "name_ar": "التصنيع",
        "name_en": "Manufacturing",
        "platinum_pct": 25,
        "high_green_pct": 18,
        "medium_green_pct": 12,
        "low_green_pct": 7,
        "yellow_pct": 4,
        "size_note": "Manufacturing thresholds account for technical skill availability.",
        "vision2030_note_en": "Vision 2030 targets manufacturing as 12% of GDP — driving Saudization pressure.",
        "vision2030_note_ar": "تستهدف رؤية 2030 التصنيع بنسبة 12% من الناتج المحلي — مما يضغط على التوطين.",
    },
    "engineering_consulting": {
        "name_ar": "الاستشارات الهندسية",
        "name_en": "Engineering & Consulting",
        "platinum_pct": 30,
        "high_green_pct": 22,
        "medium_green_pct": 16,
        "low_green_pct": 10,
        "yellow_pct": 5,
        "size_note": "Engineering sector Saudization varies by sub-discipline.",
        "vision2030_note_en": "Saudi Engineering Council drives localization in professional engineering roles.",
        "vision2030_note_ar": "هيئة المهندسين السعوديين تدفع توطين الأدوار الهندسية المهنية.",
    },
}


def _determine_band(saudi_pct: float, thresholds: dict[str, Any]) -> str:
    if saudi_pct >= thresholds["platinum_pct"]:
        return "platinum"
    if saudi_pct >= thresholds["high_green_pct"]:
        return "high_green"
    if saudi_pct >= thresholds["medium_green_pct"]:
        return "medium_green"
    if saudi_pct >= thresholds["low_green_pct"]:
        return "low_green"
    if saudi_pct >= thresholds["yellow_pct"]:
        return "yellow"
    return "red"


def _gap_to_next_band(saudi_pct: float, thresholds: dict[str, Any], total: int) -> dict[str, Any]:
    next_thresholds = {
        "red": thresholds["yellow_pct"],
        "yellow": thresholds["low_green_pct"],
        "low_green": thresholds["medium_green_pct"],
        "medium_green": thresholds["high_green_pct"],
        "high_green": thresholds["platinum_pct"],
        "platinum": None,
    }
    current = _determine_band(saudi_pct, thresholds)
    next_threshold = next_thresholds[current]
    if next_threshold is None:
        return {"next_band": None, "additional_saudi_hires_needed": 0, "note": "Already at Platinum."}
    gap_pct = next_threshold - saudi_pct
    additional_hires = math.ceil(gap_pct / 100 * total)
    next_band_name = _BAND_ORDER[_BAND_ORDER.index(current) - 1] if current != "platinum" else None
    return {
        "next_band": next_band_name,
        "next_band_threshold_pct": next_threshold,
        "gap_pct": round(gap_pct, 1),
        "additional_saudi_hires_needed": max(additional_hires, 1),
        "note_en": (
            f"Hire {max(additional_hires, 1)} more Saudi employee(s) to reach "
            f"{next_band_name} band ({next_threshold}%)."
        ),
        "note_ar": (
            f"وظّف {max(additional_hires, 1)} موظفاً سعودياً إضافياً للوصول إلى الفئة "
            f"{next_band_name} ({next_threshold}%)."
        ),
    }


# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------

class NitaqatCheckInput(BaseModel):
    sector: str = Field(..., description="Sector ID from GET /api/v1/saudization/sectors")
    total_employees: int = Field(..., ge=1, description="Total headcount (including expats)")
    saudi_employees: int = Field(..., ge=0, description="Number of Saudi national employees")

    @model_validator(mode="after")
    def saudi_cannot_exceed_total(self) -> "NitaqatCheckInput":
        if self.saudi_employees > self.total_employees:
            raise ValueError("saudi_employees cannot exceed total_employees")
        return self


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/bands", summary="Nitaqat compliance bands explained")
async def get_bands() -> dict[str, Any]:
    return {
        "bands": _BANDS,
        "order_note_en": "Platinum is highest; Red is non-compliant.",
        "order_note_ar": "البلاتيني أعلى مستوى؛ الأحمر غير ممتثل.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/sectors", summary="Sector Saudization thresholds")
async def get_sectors() -> dict[str, Any]:
    return {
        "sectors": [
            {"id": k, **v}
            for k, v in _SECTOR_THRESHOLDS.items()
        ],
        "disclaimer_en": (
            "Thresholds are approximate for 5–49 employee companies. "
            "Actual thresholds vary by company size category and MHRSD classification. "
            "Always verify at nitaqat.hrsd.gov.sa."
        ),
        "disclaimer_ar": (
            "الحدود تقريبية لشركات 5–49 موظفاً. "
            "تتفاوت الحدود الفعلية حسب فئة حجم الشركة وتصنيف وزارة الموارد البشرية. "
            "تحقق دائماً على نطاقات.hrsd.gov.sa."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/check", summary="Check current Nitaqat band and path to upgrade")
async def check_nitaqat(body: NitaqatCheckInput) -> dict[str, Any]:
    if body.saudi_employees > body.total_employees:
        raise HTTPException(
            status_code=422,
            detail="saudi_employees cannot exceed total_employees.",
        )

    thresholds = _SECTOR_THRESHOLDS.get(body.sector)
    if not thresholds:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{body.sector}' not found. Use GET /api/v1/saudization/sectors.",
        )

    saudi_pct = body.saudi_employees / body.total_employees * 100
    current_band = _determine_band(saudi_pct, thresholds)
    band_meta = next(b for b in _BANDS if b["band"] == current_band)
    upgrade_path = _gap_to_next_band(saudi_pct, thresholds, body.total_employees)

    return {
        "sector": body.sector,
        "sector_name_ar": thresholds["name_ar"],
        "sector_name_en": thresholds["name_en"],
        "total_employees": body.total_employees,
        "saudi_employees": body.saudi_employees,
        "saudi_pct": round(saudi_pct, 1),
        "current_band": current_band,
        "band_label_ar": band_meta["label_ar"],
        "band_label_en": band_meta["label_en"],
        "band_color": band_meta["color"],
        "active_restrictions": band_meta["restrictions"],
        "active_benefits": band_meta["benefits"],
        "upgrade_path": upgrade_path,
        "disclaimer_en": (
            "Indicative assessment only. Actual Nitaqat band is determined by MHRSD "
            "based on registered employee data. Verify at nitaqat.hrsd.gov.sa."
        ),
        "disclaimer_ar": (
            "تقييم استرشادي فقط. تحدد وزارة الموارد البشرية الفئة الفعلية "
            "بناءً على بيانات الموظفين المسجلين. تحقق على نطاقات.hrsd.gov.sa."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/calculator-guide", summary="How Nitaqat is calculated — guide for employers")
async def calculator_guide() -> dict[str, Any]:
    return {
        "title_ar": "كيف تُحسَب نسبة التوطين (نطاقات)",
        "title_en": "How Saudization / Nitaqat is Calculated",
        "steps_en": [
            "1. Count all registered employees in the company (Saudis + expats).",
            "2. Divide Saudi employees by total employees × 100 = Saudization %.",
            "3. Look up the % against your sector/size band table from MHRSD.",
            "4. Compare to determine your Nitaqat band (Platinum/Green/Yellow/Red).",
            "5. Part-time Saudi employees may count as 0.5 FTE — verify MHRSD rules.",
            "6. Employees on unpaid leave, disability, or maternity may have special treatment.",
        ],
        "steps_ar": [
            "١. احصب جميع الموظفين المسجلين في الشركة (سعوديون + وافدون).",
            "٢. اقسم الموظفين السعوديين على إجمالي الموظفين × 100 = نسبة التوطين.",
            "٣. قارن النسبة بجدول الفئة/الحجم الخاص بقطاعك من وزارة الموارد البشرية.",
            "٤. حدّد فئة نطاقاتك (بلاتيني/أخضر/أصفر/أحمر).",
            "٥. قد يُحتسب الموظف السعودي بدوام جزئي كـ 0.5 — تحقق من قواعد وزارة الموارد البشرية.",
            "٦. الموظفون في إجازة بدون راتب أو إعاقة أو أمومة قد يحظون بمعاملة خاصة.",
        ],
        "important_notes_en": [
            "Nitaqat is recalculated quarterly based on GOSI (General Organization for Social Insurance) data.",
            "Companies with 1–4 employees are exempt from Nitaqat.",
            "Violations can lead to CR suspension and inability to renew work permits.",
            "MHRSD offers a grace period for Yellow companies to improve before Red designation.",
        ],
        "important_notes_ar": [
            "يُعاد حساب نطاقات كل ربع سنة بناءً على بيانات التأمينات الاجتماعية (GOSI).",
            "الشركات التي لديها 1–4 موظفين معفاة من نطاقات.",
            "قد تؤدي الانتهاكات إلى تعليق السجل التجاري وعدم القدرة على تجديد تصاريح العمل.",
            "تمنح وزارة الموارد البشرية مهلة للشركات الصفراء لتحسين وضعها قبل الفئة الحمراء.",
        ],
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
