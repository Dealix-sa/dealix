"""
M&A Radar — evaluate acquisition targets and produce LOI proposals.

  POST /api/v1/m-and-a/evaluate
  GET  /api/v1/m-and-a/proposals
  GET  /api/v1/m-and-a/sectors
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.governance_os.runtime_decision import decide

router = APIRouter(prefix="/api/v1/m-and-a", tags=["m-and-a"])
log = logging.getLogger(__name__)

# In-memory store (same fallback pattern as autonomous.py)
_proposals: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# Multiplier reference table
# ---------------------------------------------------------------------------

SECTOR_MULTIPLIER_TABLE: dict[str, dict[str, Any]] = {
    "tech": {"base": 4.0, "sector_bonus": 1.0, "note": "software/SaaS premium"},
    "saas": {"base": 4.0, "sector_bonus": 1.0, "note": "recurring revenue premium"},
    "software": {"base": 4.0, "sector_bonus": 1.0, "note": "IP and scalability premium"},
    "logistics": {"base": 4.0, "sector_bonus": 0.0, "note": "asset-heavy; real estate bonus applies"},
    "retail": {"base": 4.0, "sector_bonus": 0.0, "note": "margin-sensitive sector"},
    "food": {"base": 4.0, "sector_bonus": 0.0, "note": "operations-intensive sector"},
    "healthcare": {"base": 4.0, "sector_bonus": 0.0, "note": "regulated sector"},
    "education": {"base": 4.0, "sector_bonus": 0.0, "note": "recurring cohort model"},
    "other": {"base": 4.0, "sector_bonus": 0.0, "note": "default base multiplier"},
}

_TECH_SECTORS = {"tech", "software", "saas"}


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class TargetCompany(BaseModel):
    name: str
    sector: str
    annual_revenue_sar: float
    net_profit_margin: float = Field(ge=0.0, le=1.0)
    num_employees: int
    years_in_business: int
    has_real_estate: bool = False
    has_ip: bool = False
    owner_willing_to_stay: bool = True
    city: str = "Riyadh"


class MAProposal(BaseModel):
    target_name: str
    ebitda_sar: float
    multiplier: float
    valuation_sar: float
    upfront_cash_sar: float
    earnout_sar: float
    earnout_months: int
    offer_tier: str
    loi_text_ar: str
    loi_text_en: str
    created_at: str


# ---------------------------------------------------------------------------
# Pure-function business logic
# ---------------------------------------------------------------------------


def _compute_multiplier(target: TargetCompany) -> float:
    """Return the EBITDA multiplier for a target company."""
    multiplier = 4.0

    if target.net_profit_margin > 0.20:
        multiplier += 1.0
    if target.has_real_estate or target.has_ip:
        multiplier += 1.0
    if target.owner_willing_to_stay:
        multiplier += 0.5
    if target.sector.lower() in _TECH_SECTORS:
        multiplier += 1.0
    if target.years_in_business < 2:
        multiplier -= 1.0

    return max(2.5, min(8.0, multiplier))


def _offer_tier(multiplier: float) -> str:
    if multiplier >= 7.0:
        return "aggressive"
    if multiplier >= 5.0:
        return "serious"
    return "exploratory"


def _loi_text_en(
    target: TargetCompany,
    valuation_sar: float,
    upfront_cash_sar: float,
    earnout_sar: float,
    earnout_months: int,
) -> str:
    return (
        f"Letter of Intent — {target.name}\n\n"
        f"This Letter of Intent ('LOI') sets out the key terms under which the "
        f"acquirer proposes to acquire {target.name}, a company operating in the "
        f"{target.sector} sector, headquartered in {target.city}.\n\n"
        f"Proposed Valuation: SAR {valuation_sar:,.0f}\n"
        f"Upfront Cash (60%): SAR {upfront_cash_sar:,.0f} payable at closing.\n"
        f"Earnout (40%): SAR {earnout_sar:,.0f} payable over {earnout_months} months "
        f"subject to agreed performance milestones.\n\n"
        f"This LOI is non-binding and subject to satisfactory due diligence, "
        f"definitive agreement, and regulatory approvals. All figures in Saudi Riyals."
    )


def _loi_text_ar(
    target: TargetCompany,
    valuation_sar: float,
    upfront_cash_sar: float,
    earnout_sar: float,
    earnout_months: int,
) -> str:
    return (
        f"خطاب النوايا — {target.name}\n\n"
        f"يُحدد هذا الخطاب الشروط الأساسية التي بموجبها يعرض المستحوذ الاستحواذ على "
        f"شركة {target.name} العاملة في قطاع {target.sector} ومقرها {target.city}.\n\n"
        f"التقييم المقترح: {valuation_sar:,.0f} ريال سعودي\n"
        f"النقد الفوري (60%): {upfront_cash_sar:,.0f} ريال سعودي يُسدَّد عند الإغلاق.\n"
        f"الدفعة المرتبطة بالأداء (40%): {earnout_sar:,.0f} ريال سعودي تُسدَّد على "
        f"{earnout_months} شهرًا وفق مؤشرات الأداء المتفق عليها.\n\n"
        f"هذا الخطاب غير ملزم ويخضع لإتمام العناية الواجبة وتوقيع الاتفاقية النهائية "
        f"والحصول على الموافقات التنظيمية اللازمة. جميع الأرقام بالريال السعودي."
    )


def build_proposal(target: TargetCompany, earnout_months: int = 18) -> MAProposal:
    """Compute valuation and build a full MAProposal from a TargetCompany."""
    ebitda = target.annual_revenue_sar * target.net_profit_margin
    multiplier = _compute_multiplier(target)
    valuation = round(ebitda * multiplier, 2)
    upfront = round(valuation * 0.60, 2)
    earnout = round(valuation * 0.40, 2)
    tier = _offer_tier(multiplier)

    return MAProposal(
        target_name=target.name,
        ebitda_sar=round(ebitda, 2),
        multiplier=multiplier,
        valuation_sar=valuation,
        upfront_cash_sar=upfront,
        earnout_sar=earnout,
        earnout_months=earnout_months,
        offer_tier=tier,
        loi_text_en=_loi_text_en(target, valuation, upfront, earnout, earnout_months),
        loi_text_ar=_loi_text_ar(target, valuation, upfront, earnout, earnout_months),
        created_at=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/evaluate")
async def evaluate_target(target: TargetCompany) -> dict[str, Any]:
    """Evaluate an acquisition target and return an MAProposal."""
    gov = decide(action_type="m_and_a_evaluate", context={"sector": target.sector})
    proposal = build_proposal(target)
    record = proposal.model_dump()
    record["id"] = f"ma_{uuid.uuid4().hex[:12]}"
    _proposals.append(record)
    log.info("m_and_a_proposal_created target=%s valuation=%s", target.name, proposal.valuation_sar)
    return {"governance_decision": gov.decision, "proposal": record}


@router.get("/proposals")
async def list_proposals() -> dict[str, Any]:
    """Return all generated M&A proposals (in-memory)."""
    gov = decide(action_type="m_and_a_list", context={})
    return {
        "governance_decision": gov.decision,
        "count": len(_proposals),
        "proposals": _proposals,
    }


@router.get("/sectors")
async def sector_multiplier_reference() -> dict[str, Any]:
    """Return the multiplier reference table by sector."""
    gov = decide(action_type="m_and_a_sectors", context={})
    return {
        "governance_decision": gov.decision,
        "multiplier_adjustments": {
            "base_all_sectors": 4.0,
            "margin_above_20pct": "+1.0",
            "has_real_estate_or_ip": "+1.0",
            "owner_willing_to_stay": "+0.5",
            "tech_software_saas_sector": "+1.0",
            "years_in_business_lt_2": "-1.0",
            "cap": 8.0,
            "floor": 2.5,
        },
        "sectors": SECTOR_MULTIPLIER_TABLE,
    }
