"""
Customer Onboarding API

Governs the first 30 days for a new Dealix customer:
- Diagnostic scheduling
- Kick-off checklist
- Success milestones
- Health tracking
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/onboarding", tags=["Customer Onboarding"])


class OnboardingStage(str, Enum):
    KICKOFF = "kickoff"
    DIAGNOSTIC = "diagnostic"
    PILOT_SETUP = "pilot_setup"
    PILOT_DELIVERY = "pilot_delivery"
    REVIEW = "review"
    CONTRACT = "contract"
    ACTIVE = "active"


class CustomerOnboardingRequest(BaseModel):
    company_name: str = Field(min_length=1, max_length=255)
    package: str = Field(min_length=1, max_length=128)
    start_date: datetime | None = None
    primary_contact_name: str = Field(min_length=1, max_length=255)
    primary_contact_email: str = Field(min_length=1, max_length=255)


class Milestone(BaseModel):
    name: str
    due_days_from_start: int
    completed: bool = False


class CustomerOnboardingResponse(BaseModel):
    customer_id: str
    company_name: str
    package: str
    current_stage: OnboardingStage
    start_date: str
    milestones: list[Milestone]
    next_action: str


DEFAULT_MILESTONES: dict[str, list[Milestone]] = {
    "Revenue Diagnostic": [
        Milestone(name="Kick-off call scheduled", due_days_from_start=1),
        Milestone(name="Data access + NDAs signed", due_days_from_start=2),
        Milestone(name="Diagnostic completed", due_days_from_start=5),
        Milestone(name="CEO brief delivered", due_days_from_start=6),
        Milestone(name="Next-step proposal sent", due_days_from_start=7),
    ],
    "Lead Sprint": [
        Milestone(name="Kick-off call scheduled", due_days_from_start=1),
        Milestone(name="ICP definition approved", due_days_from_start=2),
        Milestone(name="Prospect pack delivered", due_days_from_start=5),
        Milestone(name="Outreach drafts approved", due_days_from_start=6),
        Milestone(name="Handoff to sales", due_days_from_start=7),
    ],
    "Pilot Service Pack": [
        Milestone(name="Kick-off call scheduled", due_days_from_start=1),
        Milestone(name="Scope + success metrics signed", due_days_from_start=3),
        Milestone(name="Service delivery started", due_days_from_start=5),
        Milestone(name="Mid-pilot check-in", due_days_from_start=10),
        Milestone(name="Proof pack delivered", due_days_from_start=14),
        Milestone(name="Contract decision", due_days_from_start=21),
    ],
}

CUSTOMERS: dict[str, CustomerOnboardingResponse] = {}


@router.post("/start", response_model=CustomerOnboardingResponse, status_code=201)
async def start_onboarding(payload: CustomerOnboardingRequest) -> CustomerOnboardingResponse:
    """Start a new customer onboarding journey."""
    from core.utils import generate_id

    customer_id = generate_id("cust")
    start = payload.start_date or datetime.utcnow()
    milestones = DEFAULT_MILESTONES.get(payload.package, DEFAULT_MILESTONES["Revenue Diagnostic"])

    onboarding = CustomerOnboardingResponse(
        customer_id=customer_id,
        company_name=payload.company_name,
        package=payload.package,
        current_stage=OnboardingStage.KICKOFF,
        start_date=start.isoformat(),
        milestones=milestones,
        next_action="Schedule kick-off call within 24 hours",
    )
    CUSTOMERS[customer_id] = onboarding
    return onboarding


@router.get("/{customer_id}", response_model=CustomerOnboardingResponse)
async def get_onboarding(customer_id: str) -> CustomerOnboardingResponse:
    """Get onboarding status for a customer."""
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer onboarding not found")
    return CUSTOMERS[customer_id]


@router.post("/{customer_id}/complete-milestone/{milestone_name}")
async def complete_milestone(customer_id: str, milestone_name: str) -> dict[str, Any]:
    """Mark a milestone as completed and advance stage if appropriate."""
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer onboarding not found")

    onboarding = CUSTOMERS[customer_id]
    for m in onboarding.milestones:
        if m.name == milestone_name:
            m.completed = True
            break
    else:
        raise HTTPException(status_code=404, detail="Milestone not found")

    # Simple stage advancement
    completed_count = sum(1 for m in onboarding.milestones if m.completed)
    total = len(onboarding.milestones)
    if completed_count >= total:
        onboarding.current_stage = OnboardingStage.ACTIVE
        onboarding.next_action = "Move to active customer success"
    elif completed_count >= total * 0.6:
        onboarding.current_stage = OnboardingStage.PILOT_DELIVERY
        onboarding.next_action = "Deliver pilot and collect proof"
    elif completed_count >= total * 0.3:
        onboarding.current_stage = OnboardingStage.PILOT_SETUP
        onboarding.next_action = "Prepare delivery environment"

    return {
        "customer_id": customer_id,
        "current_stage": onboarding.current_stage.value,
        "next_action": onboarding.next_action,
        "progress": f"{completed_count}/{total}",
    }


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "customer-onboarding"}
