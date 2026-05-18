"""Sprint runner router — exposes the 10-step orchestrator from
auto_client_acquisition.delivery_factory.delivery_sprint.

POST /api/v1/sprint/run         →  full orchestrated 10-step result
POST /api/v1/sprint/render/*    →  render an existing Proof Pack (no re-run)
GET  /api/v1/sprint/sample      → run on demo CSV + accounts (smoke / demo)

The ``/render/*`` routes are pure formatting: they take the Proof Pack from
a prior ``/run`` response and never execute the Sprint again — re-running
would duplicate ledger and capital-asset side effects.
"""
from __future__ import annotations

import re
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/sprint", tags=["sprint"])


class _SprintRunBody(BaseModel):
    engagement_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    source_passport: dict[str, Any] | None = None
    raw_csv: str = ""
    accounts: list[dict[str, Any]] | None = None
    problem_summary: str = ""
    workflow_owner_present: bool = True


class _ProofPackRenderBody(BaseModel):
    """Render input — the Proof Pack from a prior ``/run`` response.

    ``proof_pack`` is the ``proof_pack`` object of a SprintRun. ``run`` is
    accepted as a convenience: the whole ``/run`` response can be posted back
    and the Proof Pack is extracted from it.
    """

    customer_handle: str = Field(..., min_length=1)
    engagement_id: str = "proof_pack"
    proof_pack: dict[str, Any] | None = None
    run: dict[str, Any] | None = None
    # Optional payment->delivery audit link inputs. The rung 1 Proof Pack
    # is a paid deliverable, so a real payment reference is required to
    # record the audit link in the existing capital ledger.
    customer_id: str | None = Field(default=None, max_length=120)
    payment_id: str | None = Field(default=None, max_length=200)

    def pack(self) -> dict[str, Any] | None:
        if self.proof_pack is not None:
            return self.proof_pack
        if self.run is not None:
            return self.run.get("proof_pack")
        return None


@router.post("/run")
async def run_sprint_endpoint(body: _SprintRunBody) -> dict[str, Any]:
    """Run the 10-step Sprint orchestrator. Returns the full run record
    including each step's output, the Proof Pack, capital assets, and
    retainer eligibility."""
    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    try:
        run = run_sprint(
            engagement_id=body.engagement_id,
            customer_id=body.customer_id,
            source_passport=body.source_passport,
            raw_csv=body.raw_csv,
            accounts=body.accounts,
            problem_summary=body.problem_summary,
            workflow_owner_present=body.workflow_owner_present,
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"sprint_run_failed: {e}") from e
    return run.to_dict()


@router.post("/render/markdown", response_class=PlainTextResponse)
async def render_proof_pack_markdown(body: _ProofPackRenderBody) -> str:
    """Render an existing Proof Pack as a customer-facing bilingual markdown
    report. Does not run the Sprint."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_to_markdown,
    )

    return proof_pack_to_markdown(body.pack(), customer_handle=body.customer_handle)


@router.post("/render/pdf")
async def render_proof_pack_pdf(body: _ProofPackRenderBody):
    """Render an existing Proof Pack as PDF. Falls back to markdown with an
    ``X-PDF-Renderer`` header when no PDF renderer is installed. Does not run
    the Sprint."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_to_markdown,
        proof_pack_to_pdf,
    )

    pack = body.pack()
    pdf = proof_pack_to_pdf(pack, customer_handle=body.customer_handle)
    if pdf is None:
        return PlainTextResponse(
            content=proof_pack_to_markdown(
                pack, customer_handle=body.customer_handle
            ),
            headers={"X-PDF-Renderer": "unavailable; markdown returned as fallback"},
        )
    # Sanitize the client-supplied id before it reaches a response header —
    # strip anything outside [A-Za-z0-9._-] to prevent CR/LF header injection.
    safe_id = re.sub(r"[^A-Za-z0-9._-]", "_", body.engagement_id)[:64] or "proof_pack"
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="proof_pack_{safe_id}.pdf"'
        },
    )


@router.post("/render/html", response_class=HTMLResponse)
async def render_proof_pack_html(body: _ProofPackRenderBody) -> str:
    """Render an existing Proof Pack as a self-contained bilingual HTML
    deliverable. Does not run the Sprint.

    If ``customer_id`` and ``payment_id`` are both supplied, the
    payment->delivery audit link is recorded in the capital ledger and
    embedded in the rendered footer for traceability to the paid pilot.
    """
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_to_html,
    )
    from auto_client_acquisition.proof_to_market.delivery_audit import (
        PAYMENT_REF,
        RUNG1_PROOF_PACK,
        DeliveryAuditError,
        record_delivery_audit_link,
    )

    audit_link = None
    if body.customer_id and body.payment_id:
        try:
            audit_link = record_delivery_audit_link(
                customer_id=body.customer_id,
                engagement_id=body.engagement_id,
                deliverable_kind=RUNG1_PROOF_PACK,
                reference_kind=PAYMENT_REF,
                reference_id=body.payment_id,
            )
        except DeliveryAuditError as exc:
            raise HTTPException(
                status_code=422,
                detail={"en": str(exc), "ar": "تعذّر تسجيل رابط التدقيق"},
            ) from exc

    return proof_pack_to_html(
        body.pack(),
        customer_handle=body.customer_handle,
        audit_link=audit_link,
    )


@router.post("/render/email-body", response_class=PlainTextResponse)
async def render_proof_pack_email_body(body: _ProofPackRenderBody) -> str:
    """Render a short bilingual cover note from an existing Proof Pack — the
    founder copies it into their own mailbox. Render-only — never auto-sent,
    never runs the Sprint."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_email_body,
    )

    return proof_pack_email_body(body.pack(), customer_handle=body.customer_handle)


@router.get("/sample")
async def sample_sprint() -> dict[str, Any]:
    """Run the sprint on the synthetic Saudi B2B demo CSV bundled in
    data/demo/saudi_b2b_demo.csv. Used by the landing page + smoke tests.
    """
    import csv
    from pathlib import Path
    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    demo_path = Path(__file__).resolve().parent.parent.parent / "data" / "demo" / "saudi_b2b_demo.csv"
    raw = demo_path.read_text(encoding="utf-8") if demo_path.exists() else ""
    accounts: list[dict[str, Any]] = []
    if raw:
        reader = csv.DictReader(raw.splitlines())
        accounts = list(reader)

    passport = {
        "source_id": "DEMO-SAUDI-B2B-001",
        "source_type": "client_upload",
        "owner": "dealix",
        "allowed_use": ["internal_analysis", "scoring"],
        "contains_pii": False,
        "sensitivity": "low",
        "ai_access_allowed": True,
        "external_use_allowed": False,
        "retention_policy": "project_duration",
    }
    run = run_sprint(
        engagement_id="demo_sprint_001",
        customer_id="dealix_internal_demo",
        source_passport=passport,
        raw_csv=raw,
        accounts=accounts,
        problem_summary="Demo: rank Saudi B2B accounts by relationship + sector.",
        workflow_owner_present=True,
    )
    return run.to_dict()
