"""
Islamic finance product guidance for Saudi B2B contracts.

Covers common Sharia-compliant structures: Murabaha (cost-plus sale),
Ijara (lease), Musharaka (partnership), and Istisna' (construction).
Payment calculators are illustrative — not a fatwa or binding quote.
No interest/riba-based calculations. All amounts in SAR.
"""
from __future__ import annotations

import math
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/islamic-finance", tags=["Saudi Market"])

# ---------------------------------------------------------------------------
# Product definitions
# ---------------------------------------------------------------------------

_STRUCTURES: list[dict[str, Any]] = [
    {
        "id": "murabaha",
        "name_ar": "المرابحة",
        "name_en": "Murabaha (Cost-Plus Sale)",
        "description_en": (
            "Bank purchases the asset at cost (C) and sells it to the client "
            "at cost + agreed profit margin. Client pays in installments. "
            "No interest — profit is fixed at contract inception."
        ),
        "description_ar": (
            "يشتري البنك الأصل بالتكلفة (C) ويبيعه للعميل بالتكلفة + هامش ربح متفق عليه. "
            "يدفع العميل أقساطاً. لا فوائد — الربح ثابت عند إبرام العقد."
        ),
        "typical_use_cases": [
            "Equipment purchase (IT hardware, machinery)",
            "Working capital financing",
            "Vehicle / fleet acquisition",
        ],
        "typical_profit_rate_pct": "3–6% per annum (indicative)",
        "typical_term_months": "12–60",
        "sharia_requirements": [
            "Asset must be tangible and Halal",
            "Bank must take ownership before selling",
            "Profit margin fixed — cannot increase after default",
        ],
        "saudi_banks_offering": [
            "Al Rajhi Bank", "Saudi National Bank (SNB)", "Riyad Bank",
            "Al Bilad Bank", "Bank Albilad", "Alinma Bank",
        ],
    },
    {
        "id": "ijara",
        "name_ar": "الإجارة",
        "name_en": "Ijara (Islamic Lease)",
        "description_en": (
            "Bank purchases and leases the asset to the client for a fixed period. "
            "Ownership remains with the bank. Optional purchase clause at lease end (Ijara wa-Iqtina)."
        ),
        "description_ar": (
            "يشتري البنك الأصل ويؤجره للعميل لفترة محددة. "
            "تبقى الملكية للبنك. بند شراء اختياري عند انتهاء الإجارة (إجارة وإقتناء)."
        ),
        "typical_use_cases": [
            "Office space financing",
            "Software/SaaS platform licensing (structured as usufruct lease)",
            "Vehicle / equipment leasing",
        ],
        "typical_profit_rate_pct": "4–7% per annum (indicative)",
        "typical_term_months": "12–84",
        "sharia_requirements": [
            "Asset must exist and be usable",
            "Lessor bears ownership risks (maintenance in major Ijara)",
            "Rental payments for usufruct only — not for ownership transfer",
        ],
        "saudi_banks_offering": [
            "Al Rajhi Bank", "Saudi Fransi", "SNB", "Riyad Bank",
        ],
    },
    {
        "id": "musharaka",
        "name_ar": "المشاركة",
        "name_en": "Musharaka (Partnership)",
        "description_en": (
            "Bank and client jointly invest in a venture. Profits shared "
            "per agreed ratio; losses per capital contribution. "
            "Diminishing Musharaka: client gradually buys out bank's share."
        ),
        "description_ar": (
            "يستثمر البنك والعميل معاً في مشروع. يُوزَّع الربح وفق نسبة متفق عليها؛ "
            "الخسارة بحسب حصة رأس المال. المشاركة المتناقصة: يشتري العميل تدريجياً حصة البنك."
        ),
        "typical_use_cases": [
            "Business expansion financing",
            "Joint venture projects",
            "Real estate development",
        ],
        "typical_profit_rate_pct": "Variable — based on actual project profit",
        "typical_term_months": "24–120",
        "sharia_requirements": [
            "Both parties contribute capital",
            "Profit ratio agreed at outset — not guaranteed",
            "Losses absorbed proportionally to capital",
            "No guaranteed fixed return to bank",
        ],
        "saudi_banks_offering": [
            "Al Rajhi Bank", "Alinma Bank", "Saudi Fransi",
        ],
    },
    {
        "id": "istisna",
        "name_ar": "الاستصناع",
        "name_en": "Istisna' (Manufacturing Contract)",
        "description_en": (
            "Contract for manufacture/construction of a specified asset. "
            "Buyer pays in advance; seller delivers upon completion. "
            "Common in construction and custom software development."
        ),
        "description_ar": (
            "عقد تصنيع/بناء أصل محدد. يدفع المشتري مقدماً؛ يسلّم البائع عند الانتهاء. "
            "شائع في البناء وتطوير البرمجيات المخصصة."
        ),
        "typical_use_cases": [
            "Custom software / AI platform development",
            "Construction projects",
            "Infrastructure build-outs",
        ],
        "typical_profit_rate_pct": "Fixed price negotiated at inception",
        "typical_term_months": "3–36",
        "sharia_requirements": [
            "Asset must be specifiable (type, quantity, quality)",
            "Price fixed at contract signing",
            "Delivery date and milestones defined",
        ],
        "saudi_banks_offering": ["SNB", "Riyad Bank", "SIDF"],
    },
]

_STRUCTURE_BY_ID = {s["id"]: s for s in _STRUCTURES}

# ---------------------------------------------------------------------------
# Sharia compliance checklist
# ---------------------------------------------------------------------------

_COMPLIANCE_CHECKLIST: list[dict[str, str]] = [
    {
        "item": "No riba (interest)",
        "item_ar": "لا ربا",
        "check_en": "Contract must not include interest-based penalties or returns.",
        "check_ar": "يجب ألا يتضمن العقد غرامات أو عوائد مستندة إلى الفائدة.",
    },
    {
        "item": "Asset is Halal",
        "item_ar": "الأصل حلال",
        "check_en": "Financed goods/services must be permissible under Islamic law.",
        "check_ar": "يجب أن تكون السلع/الخدمات الممولة مباحة شرعاً.",
    },
    {
        "item": "No excessive gharar (uncertainty)",
        "item_ar": "لا غرر مفرط",
        "check_en": "Contract terms (price, delivery, quality) must be clearly specified.",
        "check_ar": "شروط العقد (السعر والتسليم والجودة) يجب أن تُحدَّد بوضوح.",
    },
    {
        "item": "Bank takes ownership risk",
        "item_ar": "البنك يتحمل مخاطر الملكية",
        "check_en": "For Murabaha/Ijara, bank must hold title between purchase and sale/lease.",
        "check_ar": "في المرابحة/الإجارة، يجب أن يمتلك البنك الأصل بين الشراء والبيع/الإيجار.",
    },
    {
        "item": "Sharia Supervisory Board (SSB) approval",
        "item_ar": "اعتماد هيئة الرقابة الشرعية",
        "check_en": "Verify the financing bank has an active SSB and the product is SSB-approved.",
        "check_ar": "تحقق من وجود هيئة رقابة شرعية نشطة في البنك وأن المنتج معتمد منها.",
    },
    {
        "item": "SAMA licensing",
        "item_ar": "ترخيص مؤسسة النقد",
        "check_en": "Financing institution must hold a valid SAMA license for the product type.",
        "check_ar": "يجب أن تحمل مؤسسة التمويل ترخيصاً سارياً من مؤسسة النقد للمنتج المعني.",
    },
    {
        "item": "Late payment terms",
        "item_ar": "شروط التأخر في السداد",
        "check_en": "Late payment charges (if any) must be donated to charity — not kept by bank.",
        "check_ar": "رسوم التأخر في السداد (إن وُجدت) يجب التبرع بها للجمعيات الخيرية — لا يحتفظ بها البنك.",
    },
]

# ---------------------------------------------------------------------------
# Murabaha calculator
# ---------------------------------------------------------------------------

class MurabahaInput(BaseModel):
    principal_sar: float = Field(..., gt=0, description="Asset cost in SAR")
    profit_rate_annual_pct: float = Field(
        ..., gt=0, le=30, description="Annual profit rate % (e.g. 5.0 for 5%)"
    )
    term_months: int = Field(..., ge=1, le=360, description="Financing term in months")


def _calculate_murabaha(inp: MurabahaInput) -> dict[str, Any]:
    total_profit = inp.principal_sar * (inp.profit_rate_annual_pct / 100) * (inp.term_months / 12)
    total_amount = inp.principal_sar + total_profit
    monthly_installment = total_amount / inp.term_months

    # Build amortisation table (first 3 and last 3 payments shown)
    schedule_sample = []
    remaining = total_amount
    per_payment_principal = inp.principal_sar / inp.term_months
    per_payment_profit = total_profit / inp.term_months

    for i in range(1, inp.term_months + 1):
        remaining -= monthly_installment
        if i <= 3 or i >= inp.term_months - 2:
            schedule_sample.append({
                "period": i,
                "installment_sar": round(monthly_installment, 2),
                "principal_component_sar": round(per_payment_principal, 2),
                "profit_component_sar": round(per_payment_profit, 2),
                "balance_sar": round(max(remaining, 0), 2),
            })
        elif i == 4:
            schedule_sample.append({"period": "...", "note": f"{inp.term_months - 6} periods omitted"})

    return {
        "structure": "murabaha",
        "principal_sar": round(inp.principal_sar, 2),
        "profit_rate_annual_pct": inp.profit_rate_annual_pct,
        "term_months": inp.term_months,
        "total_profit_sar": round(total_profit, 2),
        "total_amount_sar": round(total_amount, 2),
        "monthly_installment_sar": round(monthly_installment, 2),
        "effective_cost_pct": round(inp.profit_rate_annual_pct, 4),
        "schedule_sample": schedule_sample,
    }


class IjaraInput(BaseModel):
    asset_value_sar: float = Field(..., gt=0, description="Asset market value in SAR")
    rental_rate_annual_pct: float = Field(
        ..., gt=0, le=30, description="Annual rental rate % of asset value"
    )
    term_months: int = Field(..., ge=1, le=360)
    purchase_option: bool = Field(
        False, description="Include end-of-lease purchase option (Ijara wa-Iqtina)"
    )
    residual_value_pct: float = Field(
        10.0, ge=0, le=100, description="Asset residual value % at lease end"
    )


def _calculate_ijara(inp: IjaraInput) -> dict[str, Any]:
    monthly_rental = inp.asset_value_sar * (inp.rental_rate_annual_pct / 100) / 12
    total_rentals = monthly_rental * inp.term_months
    purchase_price = inp.asset_value_sar * (inp.residual_value_pct / 100) if inp.purchase_option else None

    return {
        "structure": "ijara",
        "asset_value_sar": round(inp.asset_value_sar, 2),
        "rental_rate_annual_pct": inp.rental_rate_annual_pct,
        "term_months": inp.term_months,
        "monthly_rental_sar": round(monthly_rental, 2),
        "total_rentals_sar": round(total_rentals, 2),
        "purchase_option": inp.purchase_option,
        "purchase_price_at_end_sar": round(purchase_price, 2) if purchase_price is not None else None,
        "total_cost_if_purchased_sar": (
            round(total_rentals + purchase_price, 2) if purchase_price is not None else None
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/structures", summary="Islamic finance structures available in Saudi Arabia")
async def list_structures() -> dict[str, Any]:
    return {
        "structures": _STRUCTURES,
        "disclaimer_en": (
            "Informational only. Not a fatwa or financial advice. "
            "Consult a SAMA-licensed Islamic finance institution and Sharia advisor."
        ),
        "disclaimer_ar": (
            "معلومات فقط. ليست فتوى ولا استشارة مالية. "
            "استشر مؤسسة تمويل إسلامية مرخصة من مؤسسة النقد ومستشاراً شرعياً."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/structures/{structure_id}", summary="Detail for a specific Islamic finance structure")
async def get_structure(structure_id: str) -> dict[str, Any]:
    structure = _STRUCTURE_BY_ID.get(structure_id)
    if not structure:
        raise HTTPException(
            status_code=404,
            detail=f"Structure '{structure_id}' not found. Valid: {list(_STRUCTURE_BY_ID.keys())}",
        )
    return {
        "structure": structure,
        "disclaimer_en": "Informational only — not a fatwa or binding offer.",
        "disclaimer_ar": "معلومات فقط — ليست فتوى ولا عرضاً ملزماً.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/compliance-checklist", summary="Sharia compliance checklist for B2B contracts")
async def get_compliance_checklist() -> dict[str, Any]:
    return {
        "checklist": _COMPLIANCE_CHECKLIST,
        "note_en": (
            "This checklist is a practical guide based on commonly applied AAOIFI standards. "
            "Final Sharia compliance must be certified by a qualified scholar."
        ),
        "note_ar": (
            "هذه القائمة دليل عملي مستند إلى معايير هيئة المحاسبة والمراجعة للمؤسسات المالية الإسلامية (AAOIFI). "
            "يجب أن تُصادق على الامتثال الشرعي النهائي من قِبَل عالم مؤهّل."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/calculate/murabaha", summary="Murabaha payment calculator")
async def calculate_murabaha(body: MurabahaInput) -> dict[str, Any]:
    result = _calculate_murabaha(body)
    return {
        **result,
        "disclaimer_en": (
            "Indicative calculation only. Actual terms set by the financing institution. "
            "Not interest — this is a fixed profit margin agreed at contract signing."
        ),
        "disclaimer_ar": (
            "حساب استرشادي فقط. الشروط الفعلية تحددها مؤسسة التمويل. "
            "ليست فائدة — هذا هامش ربح ثابت متفق عليه عند إبرام العقد."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/calculate/ijara", summary="Ijara (Islamic lease) payment calculator")
async def calculate_ijara(body: IjaraInput) -> dict[str, Any]:
    result = _calculate_ijara(body)
    return {
        **result,
        "disclaimer_en": (
            "Indicative calculation only. Actual rental rates set by the financing institution."
        ),
        "disclaimer_ar": "حساب استرشادي فقط. الأسعار الفعلية تحددها مؤسسة التمويل.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
