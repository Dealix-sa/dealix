"""Sales endpoints — scripts, proposals, proposal artifacts."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from api.dependencies import get_proposal_agent
from api.schemas import (
    ProposalRequest,
    ProposalResponse,
    SalesScriptRequest,
    SalesScriptResponse,
)
from auto_client_acquisition.agents.intake import Lead, LeadSource
from auto_client_acquisition.agents.proposal import ProposalAgent
from auto_client_acquisition.runtime_paths import resolve_proposals_dir
from auto_client_acquisition.sales_os.proposal_artifact import (
    build_proposal_artifact,
    proposal_artifact_filename,
)
from core.logging import get_logger
from core.prompts.sales_scripts import get_sales_script
from core.utils import generate_id

router = APIRouter(prefix="/api/v1/sales", tags=["sales"])
log = get_logger(__name__)


def _write_proposal_artifact(
    *, engagement_id: str, body_markdown: str, company_name: str
) -> tuple[str | None, str]:
    """Render and persist a shareable HTML proposal artifact.

    Returns (artifact_url, status). Degrades gracefully: a write failure
    never breaks proposal generation — the markdown is still returned.
    """
    try:
        html_doc = build_proposal_artifact(
            body_markdown=body_markdown,
            engagement_id=engagement_id,
            customer_name=company_name,
        )
        out_dir = resolve_proposals_dir()
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / proposal_artifact_filename(engagement_id)
        path.write_text(html_doc, encoding="utf-8")
        return f"/api/v1/sales/proposal/{engagement_id}/artifact", "generated"
    except Exception as exc:  # never fail proposal generation on artifact I/O
        log.warning("proposal_artifact_write_failed", error=str(exc))
        return None, "generation_failed"


@router.post("/script", response_model=SalesScriptResponse)
async def build_script(request: SalesScriptRequest) -> SalesScriptResponse:
    """Return a bilingual sales script for a given sector + type."""
    try:
        script = get_sales_script(
            request.script_type,
            locale=request.locale,
            name=request.name or "",
            sector=request.sector,
            company=request.company or "",
            date="",
            time="",
            link="",
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return SalesScriptResponse(
        script=script,
        locale=request.locale,
        script_type=request.script_type,
    )


@router.post("/proposal", response_model=ProposalResponse)
async def generate_proposal(
    request: ProposalRequest,
    agent: ProposalAgent = Depends(get_proposal_agent),
) -> ProposalResponse:
    """Generate a proposal on demand (outside the pipeline)."""
    lead = Lead(
        id=request.lead_id or generate_id("lead"),
        source=LeadSource.MANUAL,
        company_name=request.company_name,
        contact_name="",
        sector=request.sector,
        region=request.region,
        budget=request.budget_hint,
        pain_points=request.pain_points,
        locale=request.locale,
    )
    proposal = await agent.run(lead=lead, outcomes=request.outcomes or None)
    artifact_url, artifact_status = _write_proposal_artifact(
        engagement_id=proposal.id,
        body_markdown=proposal.body_markdown,
        company_name=proposal.company_name,
    )
    return ProposalResponse(
        id=proposal.id,
        lead_id=proposal.lead_id,
        company_name=proposal.company_name,
        body_markdown=proposal.body_markdown,
        budget_min=proposal.budget_min,
        budget_max=proposal.budget_max,
        currency=proposal.currency,
        valid_until=proposal.valid_until,
        created_at=proposal.created_at,
        artifact_url=artifact_url,
        artifact_status=artifact_status,
    )


@router.get("/proposal/{engagement_id}/artifact")
async def get_proposal_artifact(engagement_id: str) -> Response:
    """Serve a generated proposal artifact as a self-contained HTML page.

    Read-only: this serves a draft for founder review. Delivery to the
    customer routes through the Approval Command Center, not this route.
    """
    path = resolve_proposals_dir() / proposal_artifact_filename(engagement_id)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="proposal artifact not found")
    return Response(content=path.read_text(encoding="utf-8"), media_type="text/html")
