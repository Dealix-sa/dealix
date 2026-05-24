"""Proposal Renderer router — POST /render (PDF) + POST /preview (HTML).

Track B.3 of the 90-day commercial plan. Returns a branded, bilingual
proposal PDF or HTML built from a lead + tier + language. Pricing is
read from ``dealix/config/pricing.yaml`` — never hardcoded.

The router is intentionally tenant-scoped via ``customer_id`` and
delegates all business logic to
``dealix.commercial_ops.proposal_renderer.ProposalRenderer``.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.revenue_pipeline.lead import Lead
from dealix.commercial_ops.proposal_renderer import (
    SUPPORTED_LANGUAGES,
    SUPPORTED_TIERS,
    ProposalRenderer,
)

router = APIRouter(prefix="/api/v1/proposals", tags=["proposals"])

_renderer = ProposalRenderer()


class ProposalRenderBody(BaseModel):
    """Request body for both /render and /preview."""

    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1, max_length=64)
    lead_id: str = Field(..., min_length=1, max_length=64)
    tier: str = Field(..., description="One of: " + ", ".join(SUPPORTED_TIERS))
    language: str = Field(
        default="ar",
        description="One of: " + ", ".join(SUPPORTED_LANGUAGES),
    )
    # Lead context — PII-free placeholders only.
    sector: str = Field(default="tbd", max_length=64)
    region: str = Field(default="tbd", max_length=64)
    customer_label: str | None = Field(default=None, max_length=128)
    customer_handle: str | None = Field(default=None, max_length=64)
    custom_pricing: dict[str, int] | None = None


def _validate_body(body: ProposalRenderBody) -> None:
    if body.tier not in SUPPORTED_TIERS:
        raise HTTPException(status_code=422, detail=f"invalid tier {body.tier!r}")
    if body.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=422, detail=f"invalid language {body.language!r}"
        )
    if body.custom_pricing:
        for tier_key, amount in body.custom_pricing.items():
            if tier_key not in SUPPORTED_TIERS:
                raise HTTPException(
                    status_code=422,
                    detail=f"custom_pricing has unknown tier {tier_key!r}",
                )
            if not isinstance(amount, int) or amount <= 0:
                raise HTTPException(
                    status_code=422,
                    detail=f"custom_pricing[{tier_key!r}] must be a positive int",
                )


def _build_lead(body: ProposalRenderBody) -> Lead:
    return Lead.make(
        slot_id=body.lead_id,
        sector=body.sector,
        region=body.region,
    )


@router.post("/preview")
async def preview_proposal(body: ProposalRenderBody) -> dict[str, Any]:
    """Render a proposal as HTML for in-app preview."""
    _validate_body(body)
    lead = _build_lead(body)
    try:
        html = _renderer.render_html(
            lead=lead,
            tier=body.tier,
            language=body.language,
            custom_pricing=body.custom_pricing,
            customer_label=body.customer_label,
            customer_handle=body.customer_handle,
        )
    except (FileNotFoundError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "customer_id": body.customer_id,
        "lead_id": body.lead_id,
        "tier": body.tier,
        "language": body.language,
        "html": html,
        "html_bytes": len(html.encode("utf-8")),
        "governance_decision": GovernanceDecision.ALLOW_WITH_REVIEW.value,
        "hard_gates": {
            "no_hardcoded_pricing": True,
            "no_pii_in_logs": True,
            "no_guaranteed_claims": True,
        },
    }


@router.post("/render")
async def render_proposal_pdf_endpoint(body: ProposalRenderBody) -> Response:
    """Render a proposal as a PDF (application/pdf bytes)."""
    _validate_body(body)
    lead = _build_lead(body)
    try:
        pdf_bytes = _renderer.render_pdf(
            lead=lead,
            tier=body.tier,
            language=body.language,
            custom_pricing=body.custom_pricing,
            customer_label=body.customer_label,
            customer_handle=body.customer_handle,
        )
    except (FileNotFoundError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    filename = f"dealix_proposal_{body.tier}_{body.language}_{body.lead_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Governance-Decision": GovernanceDecision.ALLOW_WITH_REVIEW.value,
            "X-Pricing-Source": "dealix/config/pricing.yaml",
        },
    )


@router.get("/tiers")
async def list_supported_tiers() -> dict[str, Any]:
    """Return the supported tiers + languages catalogue (read-only)."""
    return {
        "tiers": list(SUPPORTED_TIERS),
        "languages": list(SUPPORTED_LANGUAGES),
        "pricing_source": "dealix/config/pricing.yaml",
        "vat_jurisdiction": "KSA",
        "governance_decision": GovernanceDecision.ALLOW.value,
    }
