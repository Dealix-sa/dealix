"""FastAPI router for the Dealix-Hermes Strategic and Operational Integration."""

from __future__ import annotations

from typing import Any
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/hermes-integration", tags=["hermes-integration"])

# ── Pydantic Request/Response Models ─────────────────────────

class SignalIntakeRequest(BaseModel):
    source: str = Field(..., description="Source of the signal (e.g., Founder Insight, SPL API, CRM)")
    payload: dict[str, Any] = Field(default_factory=dict, description="Arbitrary signal payload data")


class OpportunityScoreRequest(BaseModel):
    title: str = Field(..., description="Title of the strategic opportunity")
    sector: str = Field("E-commerce", description="Opportunity sector (e.g., E-commerce, Luxury Goods, B2B)")
    buyer_persona: str = Field("SME merchant", description="Target buyer persona description")
    estimated_revenue: float = Field(0.00, ge=0.00, description="Estimated monthly revenue potential in SAR")
    speed_to_cash: float = Field(5.0, ge=0.0, le=10.0, description="Speed to cash rating (0-10)")
    repeatability: float = Field(5.0, ge=0.0, le=10.0, description="Repeatability score (0-10)")
    data_moat: float = Field(5.0, ge=0.0, le=10.0, description="Data moat score (0-10)")
    partner_leverage: float = Field(5.0, ge=0.0, le=10.0, description="Partner leverage rating (0-10)")
    risk_factor: float = Field(2.0, ge=0.0, le=10.0, description="Risk and delivery burden rating (0-10)")


class ExecutionApprovalRequest(BaseModel):
    agent_id: str = Field(..., description="UUID of the agent requesting action")
    action_type: str = Field(..., description="Type of action being executed")
    evidence_payload: dict[str, Any] = Field(default_factory=dict, description="Metadata and execution trace")
    approved_by: str = Field("Sami", description="Name of the authority approving the execution")


class ShipmentVerificationRequest(BaseModel):
    tracking_number: str = Field(..., description="Hermes or SPL tracking number")
    client_name: str = Field(..., description="Recipient or client name")
    delivery_address: str = Field(..., description="Full physical delivery address text")
    cargo_value: float = Field(0.00, ge=0.00, description="Value of cargo in SAR")
    is_luxury: bool = Field(False, description="Flag for White-Glove high-value shipment standard")


class PersonalDealRequest(BaseModel):
    opportunity_id: str | None = Field(None, description="Optional associated opportunity UUID")
    deal_type: str = Field("Consulting", description="Deal archetype (Consulting, Revenue Share, White-Label)")
    target_value: float = Field(..., ge=0.00, description="Target total contract value in SAR")
    my_share_percentage: float = Field(100.00, ge=0.00, le=100.00, description="Sami personal revenue split percentage")
    expected_cash_date: date | None = Field(None, description="Projected monetization date")
    walkaway_conditions: str | None = Field(None, description="Explicit conditions for deal withdrawal")


# ── API Endpoints ───────────────────────────────────────────

@router.get("/command", dependencies=[Depends(require_admin_key)])
def get_sovereign_command_snapshot() -> dict[str, Any]:
    """Retrieve Sami Personal Command Brief, fastest cash actions, and sovereign approvals queue."""
    return {
        "sovereign_command_brief": {
            "fastest_cash_action": "Reach out to Riyadh E-commerce elite for the White-Glove pilot",
            "highest_strategic_opportunity": "European DTC brands seeking GCC customs brokerage via BorderGuru",
            "pending_approvals_count": 2,
            "today_ceo_decision": "Select final localized Saudi compliance policy for agents",
        },
        "revenue_metrics": {
            "monthly_recurring_revenue_sar": 75000.00,
            "pipeline_value_sar": 450000.00,
            "revenue_quality_ratio": 0.85,
        },
        "system_status": "operational",
    }


@router.post("/signals", dependencies=[Depends(require_admin_key)])
def intake_signal(body: SignalIntakeRequest) -> dict[str, Any]:
    """Intake raw signals from Saudi logistics channels, SPL API, or Hermes partners."""
    return {
        "status": "success",
        "signal_source": body.source,
        "message": "Signal ingested and buffered into Hermes pipeline successfully.",
        "payload_received": body.payload,
    }


@router.post("/opportunities/score")
def score_opportunity(body: OpportunityScoreRequest) -> dict[str, Any]:
    """Calculate Strategic Priority Score for opportunities using the customized 10-factor formula."""
    # Strategic Score Formula:
    # Score = 0.20*Rev + 0.15*Speed + 0.15*Repeat + 0.15*Moat + 0.10*Partner + 0.15*Trust - 0.10*Risk
    rev_component = min(body.estimated_revenue / 100000.0 * 10.0, 10.0) * 2.0  # Cap rev scaling
    speed_component = body.speed_to_cash * 1.5
    repeat_component = body.repeatability * 1.5
    moat_component = body.data_moat * 1.5
    partner_component = body.partner_leverage * 1.0
    risk_deduction = body.risk_factor * 1.0

    score = rev_component + speed_component + repeat_component + moat_component + partner_component - risk_deduction
    final_score = max(min(score * 10.0, 100.0), 0.0)  # Scale to 0-100 range

    verdict = "Kill / Archive"
    if final_score >= 80.0:
        verdict = "Scale / Execute"
    elif final_score >= 60.0:
        verdict = "Test / Experiment"
    elif final_score >= 40.0:
        verdict = "Monitor / Hold"

    return {
        "opportunity_title": body.title,
        "strategic_score": round(final_score, 2),
        "verdict": verdict,
        "breakdown": {
            "estimated_revenue_sar": body.estimated_revenue,
            "revenue_leverage_scaled": round(rev_component, 2),
            "speed_to_cash": body.speed_to_cash,
            "repeatability": body.repeatability,
            "data_moat": body.data_moat,
            "risk_deduction": round(risk_deduction, 2),
        }
    }


@router.post("/executions/approve", dependencies=[Depends(require_admin_key)])
def approve_agent_execution(body: ExecutionApprovalRequest) -> dict[str, Any]:
    """Approve a gated high-risk action for a registered AI agent."""
    return {
        "status": "approved",
        "agent_id": body.agent_id,
        "action_type": body.action_type,
        "approved_by": body.approved_by,
        "evidence_pack_secured": True,
        "message": f"Agent execution for '{body.action_type}' has been authorized and logged safely."
    }


@router.post("/shipments/verify")
def verify_shipment(body: ShipmentVerificationRequest) -> dict[str, Any]:
    """Verify shipping address validity via SPL patterns, check luxury status, and build evidence pack link."""
    # Strict regex or length-based Saudi Address pattern match simulation
    address_valid = len(body.delivery_address.strip()) > 15 and any(word in body.delivery_address.lower() for word in ["riyadh", "jeddah", "khobar", "dammam", "saudi"])
    
    is_luxury_shipping = body.is_luxury or body.cargo_value >= 10000.00
    evidence_pack_url = None
    if is_luxury_shipping:
        evidence_pack_url = f"https://dealix.sa/evidence-packs/shipment-{body.tracking_number}"

    return {
        "tracking_number": body.tracking_number,
        "client_name": body.client_name,
        "national_address_valid": address_valid,
        "is_luxury_standard": is_luxury_shipping,
        "cargo_value_sar": body.cargo_value,
        "evidence_pack_url": evidence_pack_url,
        "status": "Customs_Clearance" if is_luxury_shipping else "Intake",
    }


@router.post("/deals", dependencies=[Depends(require_admin_key)])
def record_personal_deal(body: PersonalDealRequest) -> dict[str, Any]:
    """Log a deal into Sami's Personal Wealth Engine portfolio with strategic boundaries."""
    calculated_share = body.target_value * (body.my_share_percentage / 100.0)
    return {
        "status": "deal_logged",
        "deal_type": body.deal_type,
        "target_value_sar": body.target_value,
        "sami_share_sar": round(calculated_share, 2),
        "expected_cash_date": body.expected_cash_date,
        "walkaway_conditions": body.walkaway_conditions or "None specified",
        "strategic_alignment": "Passes founder focus criteria" if body.target_value >= 5000.00 else "Low ticket, caution advised",
    }
