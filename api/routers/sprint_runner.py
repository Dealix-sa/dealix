"""Sprint runner router — exposes the 10-step orchestrator from
auto_client_acquisition.delivery_factory.delivery_sprint.

POST /api/v1/sprint/run         →  full orchestrated 10-step result
POST /api/v1/sprint/render/*    →  render an existing Proof Pack (no re-run)
GET  /api/v1/sprint/sample      → run on demo CSV + accounts (smoke / demo)

Checklist tracker (lightweight JSONL — no migration):
  POST /api/v1/sprint/start                    → start a tracked sprint
  GET  /api/v1/sprint/{run_id}/checklist       → 10-step status
  POST /api/v1/sprint/{run_id}/step/{n}/mark   → mark step done

The ``/render/*`` routes are pure formatting: they take the Proof Pack from
a prior ``/run`` response and never execute the Sprint again — re-running
would duplicate ledger and capital-asset side effects.
"""
from __future__ import annotations

import json
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, Field

_REPO = Path(__file__).resolve().parents[2]
SPRINT_TRACKER_DIR = _REPO / "data" / "sprint_runs"

SPRINT_STEPS: tuple[str, ...] = (
    "kickoff",                  # 1: source-passport + customer agreement
    "data_intake",              # 2: CSV/CRM data received
    "data_quality_report",      # 3: DQ scoring complete
    "icp_match_scoring",        # 4: top-N accounts ranked
    "intelligence_loop",        # 5: enrichment + competitor brief
    "draft_assembly",           # 6: outreach + proposals drafted
    "founder_approval_pass_1",  # 7: founder approves day-3 preview
    "proof_pack_v1",            # 8: bilingual proof pack drafted
    "founder_approval_pass_2",  # 9: founder signs off final deliverable
    "handoff_delivery",         # 10: customer receives proof pack
)

router = APIRouter(prefix="/api/v1/sprint", tags=["sprint"])

# ---------------------------------------------------------------------------
# Admin auth dependency
# ---------------------------------------------------------------------------

_ADMIN_KEY_HEADER = "X-Admin-API-Key"


def _require_admin(x_admin_api_key: str | None = Header(default=None, alias=_ADMIN_KEY_HEADER)) -> str:
    """FastAPI dependency — validates the X-Admin-API-Key header."""
    if not x_admin_api_key:
        raise HTTPException(status_code=401, detail="X-Admin-API-Key header is required.")
    from core.config.settings import get_settings
    settings = get_settings()
    allowed_keys = settings.admin_api_key_list
    # When no keys are configured (dev / test), any non-empty key is accepted.
    if allowed_keys and x_admin_api_key not in allowed_keys:
        raise HTTPException(status_code=403, detail="Invalid admin API key.")
    return x_admin_api_key


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
    except Exception as e:
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


@router.post("/render/email-body", response_class=PlainTextResponse)
async def render_proof_pack_email_body(body: _ProofPackRenderBody) -> str:
    """Render a short bilingual cover note from an existing Proof Pack — the
    founder copies it into their own mailbox. Render-only — never auto-sent,
    never runs the Sprint."""
    from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
        proof_pack_email_body,
    )

    return proof_pack_email_body(body.pack(), customer_handle=body.customer_handle)


# ── Lightweight checklist tracker (JSONL-backed, no DB) ────────────────


def _tracker_path(run_id: str) -> Path:
    if not re.fullmatch(r"[a-zA-Z0-9_-]{6,64}", run_id):
        raise HTTPException(status_code=400, detail="invalid_run_id")
    SPRINT_TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    return SPRINT_TRACKER_DIR / f"{run_id}.json"


def _read_tracker(run_id: str) -> dict[str, Any]:
    path = _tracker_path(run_id)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="sprint_run_not_found")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"tracker_read_error: {exc}") from exc


def _write_tracker(run_id: str, data: dict[str, Any]) -> None:
    path = _tracker_path(run_id)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


class SprintStartBody(BaseModel):
    customer_handle: str = Field(min_length=2, max_length=64)
    plan_id: str = Field(default="pilot_managed")
    source_passport: str = Field(default="manual_entry", max_length=120)
    notes: str = Field(default="", max_length=500)


@router.post("/start")
async def sprint_start(body: SprintStartBody) -> dict[str, Any]:
    """Create a new tracked Sprint run.

    Persists a JSONL tracker at data/sprint_runs/{run_id}.json. Returns
    the run_id + initial checklist (all 10 steps pending). Doctrine: no
    external send — this is record-keeping for the founder's workflow.
    """
    run_id = f"sprint_{uuid.uuid4().hex[:12]}"
    tracker = {
        "run_id": run_id,
        "customer_handle": body.customer_handle,
        "plan_id": body.plan_id,
        "source_passport": body.source_passport,
        "notes": body.notes,
        "started_at": datetime.now(UTC).isoformat(),
        "current_step": 1,
        "steps": [
            {
                "n": i + 1,
                "name": name,
                "status": "pending",
                "marked_at": None,
                "evidence_link": None,
            }
            for i, name in enumerate(SPRINT_STEPS)
        ],
        "doctrine_note": (
            "Sprint progress is founder-tracked. No autonomous outbound. "
            "Every deliverable passes founder approval before reaching the customer."
        ),
    }
    _write_tracker(run_id, tracker)
    return tracker


@router.get("/{run_id}/checklist")
async def sprint_checklist(run_id: str) -> dict[str, Any]:
    """Return current 10-step checklist for a tracked sprint."""
    return _read_tracker(run_id)


class SprintMarkBody(BaseModel):
    evidence_link: str = Field(default="", max_length=400)
    notes: str = Field(default="", max_length=500)


@router.post("/{run_id}/step/{step_n}/mark")
async def sprint_mark_step(
    run_id: str, step_n: int, body: SprintMarkBody | None = None
) -> dict[str, Any]:
    """Mark a sprint step as done (idempotent).

    Records evidence_link + timestamp. Updates current_step to the
    next pending step. Doctrine: changes are append-only — older
    snapshots are not deleted.
    """
    if not 1 <= step_n <= len(SPRINT_STEPS):
        raise HTTPException(status_code=400, detail="invalid_step_n")
    tracker = _read_tracker(run_id)
    body = body or SprintMarkBody()
    for step in tracker["steps"]:
        if step["n"] == step_n:
            step["status"] = "done"
            step["marked_at"] = datetime.now(UTC).isoformat()
            step["evidence_link"] = body.evidence_link or step.get("evidence_link")
            if body.notes:
                step["notes"] = body.notes
    # advance current_step to first pending
    next_pending = next(
        (s["n"] for s in tracker["steps"] if s["status"] == "pending"),
        len(SPRINT_STEPS) + 1,
    )
    tracker["current_step"] = next_pending
    tracker["last_updated_at"] = datetime.now(UTC).isoformat()
    _write_tracker(run_id, tracker)
    return tracker


@router.get("/sample")
async def sample_sprint() -> dict[str, Any]:
    """Run the sprint on the synthetic Saudi B2B demo CSV bundled in
    data/demo/saudi_b2b_demo.csv. Cached in Redis for 1 hour — demo calls
    return in <100ms after first run.
    """
    import csv
    import json
    from pathlib import Path

    _DEMO_CACHE_KEY = "dealix:demo:sprint:sample:v2"
    _DEMO_CACHE_TTL = 3600  # 1 hour

    # Try Redis cache first — short timeout so a missing Redis never delays demo
    redis_client = None
    try:
        from redis.asyncio import Redis as AsyncRedis
        from core.config.settings import get_settings
        settings = get_settings()
        redis_client = AsyncRedis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=2)
        cached_raw = await redis_client.get(_DEMO_CACHE_KEY)
        if cached_raw:
            return json.loads(cached_raw)
    except Exception:  # Redis unavailable — fall through to live run
        pass

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
    result = run.to_dict()

    # Cache the result for 1 hour — best-effort, never fatal
    try:
        if redis_client:
            await redis_client.setex(_DEMO_CACHE_KEY, _DEMO_CACHE_TTL, json.dumps(result, default=str))
    except Exception:  # Redis write failure is non-fatal; next call will re-run sprint
        pass

    return result
