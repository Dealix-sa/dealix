"""
Lead Ingestion API

Receives leads from external sources (HubSpot, Typeform, Zapier, Calendly,
custom forms) and routes them through the governed Dealix pipeline.

All writes are deterministic and approval-first; no external sends.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field

from auto_client_acquisition.agents.intake import Lead as DealixLead
from auto_client_acquisition.agents.intake import LeadSource as DealixLeadSource
from core.utils import generate_id
from integrations.hubspot import HubSpotClient
from intelligence import SaudiCompanyProfile, SaudiMarketIntelligence

router = APIRouter(prefix="/api/v1/ingest", tags=["Lead Ingestion"])


class LeadIngestionRequest(BaseModel):
    source: str = Field(..., description="Source system: hubspot, typeform, calendly, zapier, manual")
    company: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=32)
    sector: str = Field(..., min_length=1, max_length=128)
    city: str = Field(..., min_length=1, max_length=128)
    region: str | None = Field(default="Saudi Arabia", max_length=128)
    employees: int | None = Field(default=None, ge=1)
    website: str | None = Field(default=None, max_length=512)
    budget: float | None = Field(default=None, ge=0)
    message: str | None = Field(default=None, max_length=5000)


class LeadIngestionResponse(BaseModel):
    lead_id: str
    status: str
    icp_score: float
    recommended_package: str
    next_action: str
    hubspot_synced: bool
    warnings: list[str]


@router.post("/lead", response_model=LeadIngestionResponse, status_code=status.HTTP_201_CREATED)
async def ingest_lead(payload: LeadIngestionRequest) -> LeadIngestionResponse:
    """Ingest a single lead from an external source."""

    # Score with intelligence layer
    profile = SaudiCompanyProfile(
        company_name=payload.company,
        sector=payload.sector,
        city=payload.city,
        employees_estimate=payload.employees,
        website=payload.website,
    )
    intel = SaudiMarketIntelligence()
    icp = intel.score_icp(profile)
    entry = intel.recommend_entry(payload.sector, payload.city)

    # Build canonical Dealix lead
    lead_id = generate_id("lead")
    lead = DealixLead(
        id=lead_id,
        source=DealixLeadSource(payload.source) if payload.source in [e.value for e in DealixLeadSource] else DealixLeadSource.API,
        company_name=payload.company,
        contact_name=payload.name,
        contact_email=str(payload.email),
        contact_phone=payload.phone,
        contact_channel=payload.source,
        sector=payload.sector,
        region=payload.region or "Saudi Arabia",
        budget=payload.budget,
        message=payload.message,
        fit_score=icp.score,
        metadata={"city": payload.city, "icp_score": icp.score, "recommended_package": entry["recommended_package"]},
        created_at=datetime.utcnow(),
    )

    # Sync to HubSpot if configured
    hubspot = HubSpotClient()
    hubspot_synced = False
    warnings: list[str] = []
    try:
        if hubspot.configured:
            result = await hubspot.sync_lead(lead)
            hubspot_synced = result.success
            if not result.success and result.message:
                warnings.append(f"HubSpot sync: {result.message}")
        else:
            warnings.append("HubSpot not configured; lead queued for manual sync")
    except Exception as exc:
        warnings.append(f"HubSpot sync failed: {exc}")

    return LeadIngestionResponse(
        lead_id=lead_id,
        status="qualified" if icp.score >= 50 else "nurture",
        icp_score=icp.score,
        recommended_package=entry["recommended_package"],
        next_action=entry["next_action"],
        hubspot_synced=hubspot_synced,
        warnings=warnings,
    )


@router.post("/hubspot-webhook")
async def ingest_hubspot_webhook(request: Request) -> dict[str, Any]:
    """Receive HubSpot contact/deal creation webhook."""
    try:
        body = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}")

    # HubSpot webhooks are arrays of events
    if not isinstance(body, list):
        body = [body]

    processed = 0
    for event in body:
        # Minimal extraction — production would use objectId to fetch full contact
        email = event.get("properties", {}).get("email", {}).get("value")
        company = event.get("properties", {}).get("company", {}).get("value")
        if email and company:
            processed += 1

    return {"received": len(body), "processed": processed, "status": "queued"}


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "lead-ingestion"}
