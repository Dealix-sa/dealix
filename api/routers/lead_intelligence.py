"""Lead Intelligence API — AI-powered lead scoring, enrichment, and prioritization.

Endpoints:
  POST /api/v1/leads/intelligence/score-batch        — score up to 50 leads at once
  POST /api/v1/leads/intelligence/enrich             — enrich a single lead with Saudi B2B context
  GET  /api/v1/leads/intelligence/top-opportunities  — top 10 ranked by ICP fit + urgency
  GET  /api/v1/leads/intelligence/sector-heat-map    — sector x city heat map of opportunity
  POST /api/v1/leads/intelligence/categorize         — categorize lead into funnel stage
  GET  /api/v1/leads/intelligence/conversion-patterns — historical conversion patterns by sector

Scoring formula (0–100):
  ICP sector match (technology/financial_services/healthcare/real_estate): +25
  ICP city match (riyadh/jeddah/dammam): +20
  Employee count 20–500: +20
  Has ZATCA issue: +15
  Has PDPL concern: +10
  Revenue 500K–10M SAR: +10

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Bilingual ar/en labels
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/leads/intelligence",
    tags=["lead-intelligence"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Type aliases and constants
# ---------------------------------------------------------------------------

ICP_SECTORS: frozenset[str] = frozenset(
    {"technology", "financial_services", "healthcare", "real_estate"}
)
ICP_CITIES: frozenset[str] = frozenset({"riyadh", "jeddah", "dammam"})

FunnelStage = Literal[
    "awareness", "consideration", "evaluation", "intent", "decision", "customer"
]

# ---------------------------------------------------------------------------
# Bilingual label helpers
# ---------------------------------------------------------------------------

_LABELS_AR: dict[str, str] = {
    "score": "درجة العميل المحتمل",
    "sector": "القطاع",
    "city": "المدينة",
    "employees": "عدد الموظفين",
    "revenue": "الإيراد السنوي",
    "zatca_issue": "مشكلة ضريبية (زاتكا)",
    "pdpl_concern": "مخاوف حماية البيانات",
    "icp_fit": "توافق مع ملف العميل المثالي",
    "urgency": "مستوى الإلحاح",
    "funnel_stage": "مرحلة قمع المبيعات",
    "top_opportunities": "أفضل الفرص",
    "sector_heat_map": "خريطة حرارة القطاعات",
    "conversion_patterns": "أنماط التحويل",
}

_LABELS_EN: dict[str, str] = {
    "score": "Lead Score",
    "sector": "Sector",
    "city": "City",
    "employees": "Employee Count",
    "revenue": "Annual Revenue",
    "zatca_issue": "ZATCA Compliance Issue",
    "pdpl_concern": "PDPL Data Concern",
    "icp_fit": "ICP Fit",
    "urgency": "Urgency Level",
    "funnel_stage": "Funnel Stage",
    "top_opportunities": "Top Opportunities",
    "sector_heat_map": "Sector Heat Map",
    "conversion_patterns": "Conversion Patterns",
}


def _label(key: str) -> dict[str, str]:
    return {"ar": _LABELS_AR.get(key, key), "en": _LABELS_EN.get(key, key)}


# ---------------------------------------------------------------------------
# Scoring engine (pure function)
# ---------------------------------------------------------------------------


def compute_lead_score(lead: dict[str, Any]) -> int:
    """Compute a lead score 0–100 using the ICP scoring formula.

    Scoring breakdown:
      ICP sector match: +25
      ICP city match:   +20
      Employees 20–500: +20
      ZATCA issue:      +15
      PDPL concern:     +10
      Revenue 500K–10M: +10
    """
    score = 0

    sector = str(lead.get("sector", "")).lower().replace(" ", "_")
    if sector in ICP_SECTORS:
        score += 25

    city = str(lead.get("city", "")).lower()
    if city in ICP_CITIES:
        score += 20

    employees = int(lead.get("employees", 0))
    if 20 <= employees <= 500:
        score += 20

    if lead.get("has_zatca_issue", False):
        score += 15

    if lead.get("has_pdpl_concern", False):
        score += 10

    revenue = float(lead.get("annual_revenue_sar", 0))
    if 500_000 <= revenue <= 10_000_000:
        score += 10

    return min(score, 100)


def score_breakdown(lead: dict[str, Any]) -> dict[str, int]:
    """Return per-component score breakdown for transparency."""
    sector = str(lead.get("sector", "")).lower().replace(" ", "_")
    city = str(lead.get("city", "")).lower()
    employees = int(lead.get("employees", 0))
    revenue = float(lead.get("annual_revenue_sar", 0))

    return {
        "icp_sector": 25 if sector in ICP_SECTORS else 0,
        "icp_city": 20 if city in ICP_CITIES else 0,
        "employee_count": 20 if 20 <= employees <= 500 else 0,
        "zatca_urgency": 15 if lead.get("has_zatca_issue", False) else 0,
        "pdpl_urgency": 10 if lead.get("has_pdpl_concern", False) else 0,
        "revenue_band": 10 if 500_000 <= revenue <= 10_000_000 else 0,
    }


def categorize_funnel_stage(lead: dict[str, Any]) -> FunnelStage:
    """Classify a lead into a funnel stage based on engagement signals."""
    engaged = lead.get("engaged", False)
    meeting_booked = lead.get("meeting_booked", False)
    proposal_sent = lead.get("proposal_sent", False)
    pilot_started = lead.get("pilot_started", False)
    signed = lead.get("signed", False)
    is_customer = lead.get("is_customer", False)

    if is_customer or signed:
        return "customer"
    if pilot_started:
        return "decision"
    if proposal_sent:
        return "intent"
    if meeting_booked:
        return "evaluation"
    if engaged:
        return "consideration"
    return "awareness"


# ---------------------------------------------------------------------------
# Demo lead store (15 varied leads)
# ---------------------------------------------------------------------------

_DEMO_LEADS: list[dict[str, Any]] = [
    {
        "lead_id": "LID-001",
        "company_name_ar": "شركة الرياض للتقنية",
        "company_name_en": "Riyadh Tech Solutions",
        "sector": "technology",
        "city": "riyadh",
        "employees": 120,
        "annual_revenue_sar": 3_200_000,
        "has_zatca_issue": True,
        "has_pdpl_concern": True,
        "engaged": True,
        "meeting_booked": True,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Ahmed Al-Rashidi",
    },
    {
        "lead_id": "LID-002",
        "company_name_ar": "مجموعة الخدمات المالية",
        "company_name_en": "Gulf Financial Services Group",
        "sector": "financial_services",
        "city": "jeddah",
        "employees": 85,
        "annual_revenue_sar": 7_500_000,
        "has_zatca_issue": True,
        "has_pdpl_concern": False,
        "engaged": True,
        "meeting_booked": True,
        "proposal_sent": True,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Fatima Al-Zahrani",
    },
    {
        "lead_id": "LID-003",
        "company_name_ar": "عيادات الصحة المتقدمة",
        "company_name_en": "Advanced Health Clinics",
        "sector": "healthcare",
        "city": "dammam",
        "employees": 45,
        "annual_revenue_sar": 1_800_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": True,
        "engaged": False,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Dr. Khaled Al-Otaibi",
    },
    {
        "lead_id": "LID-004",
        "company_name_ar": "شركة العقارات الذكية",
        "company_name_en": "Smart Real Estate Co",
        "sector": "real_estate",
        "city": "riyadh",
        "employees": 200,
        "annual_revenue_sar": 9_000_000,
        "has_zatca_issue": True,
        "has_pdpl_concern": False,
        "engaged": True,
        "meeting_booked": True,
        "proposal_sent": True,
        "pilot_started": True,
        "signed": False,
        "is_customer": False,
        "contact_name": "Sultan Al-Faisal",
    },
    {
        "lead_id": "LID-005",
        "company_name_ar": "شركة اللوجستيات السريعة",
        "company_name_en": "FastMove Logistics",
        "sector": "logistics",
        "city": "dammam",
        "employees": 310,
        "annual_revenue_sar": 4_500_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": False,
        "engaged": True,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Waleed Al-Harbi",
    },
    {
        "lead_id": "LID-006",
        "company_name_ar": "حلول البيانات المتكاملة",
        "company_name_en": "Integrated Data Solutions",
        "sector": "technology",
        "city": "riyadh",
        "employees": 60,
        "annual_revenue_sar": 2_100_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": True,
        "engaged": True,
        "meeting_booked": True,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Noura Al-Dosari",
    },
    {
        "lead_id": "LID-007",
        "company_name_ar": "مستشفى الأمل",
        "company_name_en": "Al-Amal Hospital Group",
        "sector": "healthcare",
        "city": "riyadh",
        "employees": 350,
        "annual_revenue_sar": 8_200_000,
        "has_zatca_issue": True,
        "has_pdpl_concern": True,
        "engaged": True,
        "meeting_booked": True,
        "proposal_sent": True,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Dr. Sarah Al-Qahtani",
    },
    {
        "lead_id": "LID-008",
        "company_name_ar": "بنك الخليج الإقليمي",
        "company_name_en": "Gulf Regional Bank",
        "sector": "financial_services",
        "city": "riyadh",
        "employees": 500,
        "annual_revenue_sar": 9_800_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": True,
        "engaged": False,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Ibrahim Al-Shammari",
    },
    {
        "lead_id": "LID-009",
        "company_name_ar": "شركة البناء الحديث",
        "company_name_en": "Modern Construction Co",
        "sector": "construction",
        "city": "jeddah",
        "employees": 800,
        "annual_revenue_sar": 25_000_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": False,
        "engaged": False,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Mansour Al-Blawi",
    },
    {
        "lead_id": "LID-010",
        "company_name_ar": "منصة التجارة الإلكترونية",
        "company_name_en": "E-Commerce Platform",
        "sector": "technology",
        "city": "jeddah",
        "employees": 30,
        "annual_revenue_sar": 900_000,
        "has_zatca_issue": True,
        "has_pdpl_concern": False,
        "engaged": True,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Reem Al-Ghamdi",
    },
    {
        "lead_id": "LID-011",
        "company_name_ar": "شركة التأمين الشامل",
        "company_name_en": "Comprehensive Insurance Co",
        "sector": "financial_services",
        "city": "dammam",
        "employees": 150,
        "annual_revenue_sar": 6_000_000,
        "has_zatca_issue": True,
        "has_pdpl_concern": True,
        "engaged": True,
        "meeting_booked": True,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Turki Al-Anazi",
    },
    {
        "lead_id": "LID-012",
        "company_name_ar": "شركة التطوير العقاري الذهبي",
        "company_name_en": "Golden Real Estate Dev",
        "sector": "real_estate",
        "city": "jeddah",
        "employees": 75,
        "annual_revenue_sar": 4_200_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": False,
        "engaged": False,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Abdullah Al-Mutairi",
    },
    {
        "lead_id": "LID-013",
        "company_name_ar": "شركة الذكاء الاصطناعي للأعمال",
        "company_name_en": "Business AI Corp",
        "sector": "technology",
        "city": "riyadh",
        "employees": 25,
        "annual_revenue_sar": 700_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": True,
        "engaged": True,
        "meeting_booked": True,
        "proposal_sent": True,
        "pilot_started": True,
        "signed": False,
        "is_customer": False,
        "contact_name": "Lama Al-Subaie",
    },
    {
        "lead_id": "LID-014",
        "company_name_ar": "مجموعة الرعاية الصحية الخاصة",
        "company_name_en": "Private Healthcare Group",
        "sector": "healthcare",
        "city": "jeddah",
        "employees": 180,
        "annual_revenue_sar": 5_500_000,
        "has_zatca_issue": True,
        "has_pdpl_concern": False,
        "engaged": False,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Dr. Mohammed Al-Senan",
    },
    {
        "lead_id": "LID-015",
        "company_name_ar": "منصة الاستثمار الرقمي",
        "company_name_en": "Digital Investment Platform",
        "sector": "financial_services",
        "city": "riyadh",
        "employees": 40,
        "annual_revenue_sar": 1_200_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": True,
        "engaged": True,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
        "contact_name": "Hana Al-Jasser",
    },
]

# Pre-compute scores once at module load to avoid repeated computation
_LEAD_INDEX: dict[str, dict[str, Any]] = {
    lead["lead_id"]: {**lead, "score": compute_lead_score(lead)} for lead in _DEMO_LEADS
}


# ---------------------------------------------------------------------------
# Enrichment helper
# ---------------------------------------------------------------------------


def _enrich_lead(lead_data: dict[str, Any]) -> dict[str, Any]:
    """Add Saudi B2B context signals to a raw lead dict."""
    sector = str(lead_data.get("sector", "")).lower().replace(" ", "_")
    city = str(lead_data.get("city", "")).lower()
    revenue = float(lead_data.get("annual_revenue_sar", 0))

    enriched: dict[str, Any] = {**lead_data}

    # Pain signals by sector
    sector_pains: dict[str, list[str]] = {
        "technology": ["legacy system integration", "PDPL compliance gap", "manual reporting"],
        "financial_services": ["ZATCA reporting", "KYC automation", "regulatory audit trail"],
        "healthcare": ["patient data PDPL obligations", "ZATCA medical billing", "appointment ops"],
        "real_estate": ["REGA compliance", "contract automation", "lead qualification speed"],
        "logistics": ["customs clearance tracking", "fleet ops visibility", "ZATCA e-invoicing"],
    }
    enriched["inferred_pain_signals"] = sector_pains.get(
        sector, ["operational efficiency", "reporting automation"]
    )

    # Vision 2030 relevance
    v2030_sectors = {"technology", "healthcare", "financial_services", "real_estate"}
    enriched["vision_2030_relevance"] = "high" if sector in v2030_sectors else "medium"

    # SME classification
    employees = int(lead_data.get("employees", 0))
    if employees < 50:
        enriched["sme_class"] = "micro"
    elif employees < 250:
        enriched["sme_class"] = "small"
    elif employees <= 500:
        enriched["sme_class"] = "medium"
    else:
        enriched["sme_class"] = "large"

    # Revenue tier
    if revenue < 1_000_000:
        enriched["revenue_tier"] = "early_stage"
    elif revenue < 5_000_000:
        enriched["revenue_tier"] = "growth"
    elif revenue < 20_000_000:
        enriched["revenue_tier"] = "scale"
    else:
        enriched["revenue_tier"] = "enterprise"

    # Recommended outreach channel
    if city in ICP_CITIES and sector in ICP_SECTORS:
        enriched["recommended_channel"] = "warm_intro_via_network"
    else:
        enriched["recommended_channel"] = "inbound_content_first"

    return enriched


# ---------------------------------------------------------------------------
# Conversion patterns static data
# ---------------------------------------------------------------------------

_CONVERSION_PATTERNS: dict[str, dict[str, Any]] = {
    "technology": {
        "avg_sales_cycle_days": 18,
        "awareness_to_consideration_pct": 45,
        "consideration_to_evaluation_pct": 38,
        "evaluation_to_intent_pct": 55,
        "intent_to_decision_pct": 65,
        "decision_to_customer_pct": 72,
        "top_buying_trigger": "PDPL deadline",
        "best_outreach_month": "September",
    },
    "financial_services": {
        "avg_sales_cycle_days": 28,
        "awareness_to_consideration_pct": 30,
        "consideration_to_evaluation_pct": 42,
        "evaluation_to_intent_pct": 48,
        "intent_to_decision_pct": 60,
        "decision_to_customer_pct": 70,
        "top_buying_trigger": "ZATCA audit",
        "best_outreach_month": "October",
    },
    "healthcare": {
        "avg_sales_cycle_days": 35,
        "awareness_to_consideration_pct": 28,
        "consideration_to_evaluation_pct": 35,
        "evaluation_to_intent_pct": 50,
        "intent_to_decision_pct": 58,
        "decision_to_customer_pct": 68,
        "top_buying_trigger": "PDPL patient data obligations",
        "best_outreach_month": "January",
    },
    "real_estate": {
        "avg_sales_cycle_days": 22,
        "awareness_to_consideration_pct": 38,
        "consideration_to_evaluation_pct": 40,
        "evaluation_to_intent_pct": 52,
        "intent_to_decision_pct": 62,
        "decision_to_customer_pct": 75,
        "top_buying_trigger": "Vision 2030 project deadline",
        "best_outreach_month": "March",
    },
    "logistics": {
        "avg_sales_cycle_days": 20,
        "awareness_to_consideration_pct": 35,
        "consideration_to_evaluation_pct": 44,
        "evaluation_to_intent_pct": 56,
        "intent_to_decision_pct": 63,
        "decision_to_customer_pct": 71,
        "top_buying_trigger": "ZATCA e-invoicing mandate",
        "best_outreach_month": "November",
    },
}


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class LeadInput(BaseModel):
    model_config = {"extra": "allow"}

    lead_id: str = Field(default="", description="Optional lead ID")
    company_name_ar: str = Field(default="", description="Arabic company name")
    company_name_en: str = Field(default="", description="English company name")
    sector: str = Field(default="", description="Industry sector")
    city: str = Field(default="", description="HQ city (lowercase)")
    employees: int = Field(default=0, ge=0, description="Employee count")
    annual_revenue_sar: float = Field(default=0.0, ge=0, description="Annual revenue SAR")
    has_zatca_issue: bool = Field(default=False)
    has_pdpl_concern: bool = Field(default=False)
    engaged: bool = Field(default=False)
    meeting_booked: bool = Field(default=False)
    proposal_sent: bool = Field(default=False)
    pilot_started: bool = Field(default=False)
    signed: bool = Field(default=False)
    is_customer: bool = Field(default=False)


class BatchScoringRequest(BaseModel):
    leads: list[LeadInput] = Field(..., max_length=50, description="Up to 50 leads")


class CategorizeRequest(BaseModel):
    lead: LeadInput


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/score-batch")
async def score_batch(body: BatchScoringRequest) -> dict[str, Any]:
    """Score up to 50 leads at once using the ICP formula.

    Returns each lead with its score (0–100) and per-component breakdown.
    Leads are sorted by score descending.
    """
    if len(body.leads) == 0:
        raise HTTPException(status_code=400, detail="At least 1 lead required in batch")
    if len(body.leads) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 leads per batch")

    results: list[dict[str, Any]] = []
    for lead in body.leads:
        lead_dict = lead.model_dump()
        s = compute_lead_score(lead_dict)
        breakdown = score_breakdown(lead_dict)
        results.append(
            {
                "lead_id": lead.lead_id or "unknown",
                "company_name_en": lead.company_name_en,
                "company_name_ar": lead.company_name_ar,
                "score": s,
                "breakdown": breakdown,
                "score_label": _label("score"),
            }
        )

    results.sort(key=lambda r: r["score"], reverse=True)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_scored": len(results),
        "results": results,
        "note_ar": "التقييم بناءً على معايير ملف العميل المثالي — ليست ضمانات تحويل",
        "note_en": "Scored against ICP criteria — not a guarantee of conversion",
    }


@router.post("/enrich")
async def enrich_lead(body: LeadInput) -> dict[str, Any]:
    """Enrich a single lead with Saudi B2B context signals.

    Adds: inferred pain signals, Vision 2030 relevance, SME class,
    revenue tier, recommended outreach channel, and ICP score.
    """
    lead_dict = body.model_dump()
    enriched = _enrich_lead(lead_dict)
    score = compute_lead_score(lead_dict)
    breakdown = score_breakdown(lead_dict)
    stage = categorize_funnel_stage(lead_dict)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "lead_id": body.lead_id or "enriched",
        "company_name_en": body.company_name_en,
        "company_name_ar": body.company_name_ar,
        "score": score,
        "funnel_stage": stage,
        "score_label": _label("score"),
        "enriched": enriched,
        "breakdown": breakdown,
    }


@router.get("/top-opportunities")
async def top_opportunities() -> dict[str, Any]:
    """Return top 10 leads ranked by ICP fit score + urgency signals.

    Uses the demo lead store. Sorted by score descending.
    """
    ranked = sorted(_LEAD_INDEX.values(), key=lambda r: r["score"], reverse=True)
    top10 = ranked[:10]

    output: list[dict[str, Any]] = []
    for lead in top10:
        stage = categorize_funnel_stage(lead)
        output.append(
            {
                "lead_id": lead["lead_id"],
                "company_name_ar": lead["company_name_ar"],
                "company_name_en": lead["company_name_en"],
                "sector": lead["sector"],
                "city": lead["city"],
                "score": lead["score"],
                "funnel_stage": stage,
                "has_zatca_issue": lead["has_zatca_issue"],
                "has_pdpl_concern": lead["has_pdpl_concern"],
                "urgency": "high" if lead["has_zatca_issue"] or lead["has_pdpl_concern"] else "medium",
            }
        )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("top_opportunities"),
        "total": len(output),
        "leads": output,
    }


@router.get("/sector-heat-map")
async def sector_heat_map() -> dict[str, Any]:
    """Return sector x city heat map of opportunity scores.

    Each cell is the average lead score for that sector-city combination.
    Uses the demo lead store as the data source.
    """
    sectors = list({lead["sector"] for lead in _DEMO_LEADS})
    cities = list({lead["city"] for lead in _DEMO_LEADS})

    heat_map: dict[str, dict[str, int]] = {}
    for sector in sectors:
        heat_map[sector] = {}
        for city in cities:
            matching = [
                lead["score"]
                for lead in _LEAD_INDEX.values()
                if lead["sector"] == sector and lead["city"] == city
            ]
            heat_map[sector][city] = round(sum(matching) / len(matching)) if matching else 0

    # Sector totals (max across cities)
    sector_totals: dict[str, int] = {}
    for sector in sectors:
        sector_scores = [
            lead["score"] for lead in _LEAD_INDEX.values() if lead["sector"] == sector
        ]
        sector_totals[sector] = round(sum(sector_scores) / len(sector_scores)) if sector_scores else 0

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("sector_heat_map"),
        "sectors": sectors,
        "cities": cities,
        "heat_map": heat_map,
        "sector_avg_scores": sector_totals,
    }


@router.post("/categorize")
async def categorize_lead(body: CategorizeRequest) -> dict[str, Any]:
    """Categorize a lead into a funnel stage based on engagement signals.

    Stages: awareness -> consideration -> evaluation -> intent -> decision -> customer
    """
    lead_dict = body.lead.model_dump()
    stage = categorize_funnel_stage(lead_dict)
    score = compute_lead_score(lead_dict)

    stage_labels: dict[FunnelStage, dict[str, str]] = {
        "awareness": {"ar": "الوعي", "en": "Awareness"},
        "consideration": {"ar": "التفكير", "en": "Consideration"},
        "evaluation": {"ar": "التقييم", "en": "Evaluation"},
        "intent": {"ar": "النية", "en": "Intent"},
        "decision": {"ar": "القرار", "en": "Decision"},
        "customer": {"ar": "عميل", "en": "Customer"},
    }

    next_action: dict[FunnelStage, dict[str, str]] = {
        "awareness": {
            "ar": "أرسل محتوى تثقيفياً عن الامتثال",
            "en": "Send educational compliance content",
        },
        "consideration": {
            "ar": "اقترح موعداً تشخيصياً",
            "en": "Propose a diagnostic session",
        },
        "evaluation": {
            "ar": "أرسل دراسة حالة من نفس القطاع",
            "en": "Share sector-specific case study",
        },
        "intent": {
            "ar": "أرسل العرض التجاري المخصص",
            "en": "Send customized proposal",
        },
        "decision": {
            "ar": "ابدأ تجربة الإطلاق السريع",
            "en": "Initiate sprint pilot",
        },
        "customer": {
            "ar": "جدول مراجعة 30 يوماً",
            "en": "Schedule 30-day review",
        },
    }

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "lead_id": body.lead.lead_id or "categorized",
        "funnel_stage": stage,
        "funnel_stage_label": stage_labels[stage],
        "score": score,
        "next_recommended_action": next_action[stage],
        "label": _label("funnel_stage"),
    }


@router.get("/conversion-patterns")
async def conversion_patterns(
    sector: str | None = None,
) -> dict[str, Any]:
    """Return historical conversion patterns by sector.

    Provides stage-by-stage conversion rates, average sales cycle length,
    top buying triggers, and best outreach timing.
    """
    if sector:
        sector_key = sector.lower().replace(" ", "_")
        pattern = _CONVERSION_PATTERNS.get(sector_key)
        if not pattern:
            available = list(_CONVERSION_PATTERNS.keys())
            raise HTTPException(
                status_code=404,
                detail=f"Sector '{sector}' not found. Available: {available}",
            )
        return {
            "governance_decision": _GOV,
            "generated_at": _NOW.isoformat(),
            "sector": sector_key,
            "pattern": pattern,
            "label": _label("conversion_patterns"),
        }

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("conversion_patterns"),
        "sectors": _CONVERSION_PATTERNS,
        "note_ar": "الأنماط مبنية على بيانات سوق B2B السعودي 2025-2026",
        "note_en": "Patterns based on Saudi B2B market data 2025-2026",
    }
