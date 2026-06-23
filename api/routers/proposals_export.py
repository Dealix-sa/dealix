"""
Proposals Export Router — website export, lead capture, daily drafts.

Endpoints:
    POST /api/v1/proposals/render          — render bilingual proposal via Jinja2
    GET  /api/v1/proposals/pitch-pdf       — download pitch PDF
    GET  /api/v1/leads/daily-export        — export daily drafts as CSV
    POST /api/v1/leads/website-inquiry     — capture website lead inquiry

All generated content is DRAFT_ONLY. Nothing is sent automatically.
Governance decision is included in every response.
"""

from __future__ import annotations

import io
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["proposals-export"])

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = REPO_ROOT / "templates"
PDF_PATH = REPO_ROOT / "landing" / "assets" / "dealix_proposal_v2.pdf"
DAILY_DRAFTS_DIR = REPO_ROOT / "data" / "daily_drafts"
LEADS_DIR = REPO_ROOT / "data" / "leads"
WEBSITE_INQUIRIES_PATH = LEADS_DIR / "website_inquiries.jsonl"

CALENDLY_URL = "https://calendly.com/sami-assiri11/dealix-demo"

# ---------------------------------------------------------------------------
# Lazy Jinja2 environment — initialised only when first needed so the module
# can be imported safely even when Jinja2 is not installed.
# ---------------------------------------------------------------------------

_jinja_env = None


def _get_jinja_env():  # type: ignore[return]
    global _jinja_env
    if _jinja_env is not None:
        return _jinja_env
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape

        _jinja_env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(["html"]),
            keep_trailing_newline=True,
        )
        return _jinja_env
    except Exception as exc:
        raise RuntimeError(f"Jinja2 unavailable: {exc}") from exc


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------


class ProposalRequest(BaseModel):
    company_name: str
    sector: str
    contact_name: str = "فريق"
    pain_points: list[str] = []
    language: str = "ar"  # ar | en | both


class InquiryRequest(BaseModel):
    company: str
    sector: str
    email: str
    name: str = ""
    message: str = ""
    language_pref: str = "ar"


# ---------------------------------------------------------------------------
# Endpoint 1: Render custom proposal
# ---------------------------------------------------------------------------


@router.post("/proposals/render")
async def render_proposal(req: ProposalRequest) -> dict:
    """
    Render a bilingual (or single-language) proposal using Jinja2 templates.

    Returns the rendered markdown, word count, and generation timestamp.
    All output is marked DRAFT_ONLY — not for automatic distribution.
    """
    today_str = datetime.now(UTC).strftime("%Y-%m-%d")
    template_vars = {
        "company_name": req.company_name,
        "contact_name": req.contact_name,
        "sector": req.sector,
        "pain_points": req.pain_points or [
            "فرص ضائعة بسبب بطء الاستجابة" if req.language in ("ar", "both")
            else "Slow response to inbound leads"
        ],
        "date": today_str,
    }

    results: dict[str, str] = {}
    errors: dict[str, str] = {}

    langs_to_render: list[str]
    if req.language == "both":
        langs_to_render = ["ar", "en"]
    elif req.language in ("ar", "en"):
        langs_to_render = [req.language]
    else:
        raise HTTPException(status_code=422, detail="language must be 'ar', 'en', or 'both'")

    template_map = {
        "ar": "PROPOSAL_SPRINT_ARABIC_FULL.md.j2",
        "en": "PROPOSAL_SPRINT_ENGLISH_FULL.md.j2",
    }

    try:
        env = _get_jinja_env()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    for lang in langs_to_render:
        tmpl_name = template_map[lang]
        tmpl_path = TEMPLATES_DIR / tmpl_name
        if not tmpl_path.exists():
            errors[lang] = f"Template not found: {tmpl_name}"
            continue
        try:
            tmpl = env.get_template(tmpl_name)
            rendered = tmpl.render(**template_vars)
            results[f"proposal_{lang}"] = rendered
        except Exception as exc:
            errors[lang] = str(exc)

    if not results and errors:
        raise HTTPException(status_code=500, detail={"render_errors": errors})

    total_words = sum(len(text.split()) for text in results.values())

    return {
        "governance_decision": "DRAFT_ONLY",
        "approval_required": True,
        **results,
        "word_count": total_words,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "template_errors": errors or None,
    }


# ---------------------------------------------------------------------------
# Endpoint 2: Download pitch PDF
# ---------------------------------------------------------------------------


@router.get("/proposals/pitch-pdf")
async def download_pitch_pdf() -> FileResponse:
    """
    Download the Dealix company pitch PDF.

    Returns 404 if the PDF has not been placed in landing/assets/.
    """
    if not PDF_PATH.exists():
        raise HTTPException(status_code=404, detail="PDF not found — place file at landing/assets/dealix_proposal_v2.pdf")
    return FileResponse(
        path=str(PDF_PATH),
        media_type="application/pdf",
        filename="Dealix_Company_Proposal_v2.pdf",
        headers={"Content-Disposition": "attachment; filename=Dealix_Company_Proposal_v2.pdf"},
    )


# ---------------------------------------------------------------------------
# Endpoint 3: Export daily drafts as CSV
# ---------------------------------------------------------------------------


@router.get("/leads/daily-export")
async def export_daily_drafts(date: str | None = None) -> StreamingResponse:
    """
    Stream the daily drafts CSV for the requested date (defaults to today).

    Reads data/daily_drafts/{date}/drafts_all.csv.
    Returns 404 if the date directory or CSV file does not exist.
    """
    if date is None:
        date = datetime.now(UTC).strftime("%Y-%m-%d")

    # Sanitise the date parameter to prevent path traversal.
    import re as _re
    if not _re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise HTTPException(status_code=422, detail="date must be YYYY-MM-DD")

    csv_path = DAILY_DRAFTS_DIR / date / "drafts_all.csv"
    if not csv_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No drafts CSV found for {date}. Run generate_daily_mass_drafts.py first.",
        )

    content = csv_path.read_bytes()

    return StreamingResponse(
        io.BytesIO(content),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename=dealix_drafts_{date}.csv"},
    )


# ---------------------------------------------------------------------------
# Endpoint 4: Website lead inquiry capture
# ---------------------------------------------------------------------------


@router.post("/leads/website-inquiry")
async def capture_website_inquiry(req: InquiryRequest) -> dict:
    """
    Capture a website lead inquiry and append it to data/leads/website_inquiries.jsonl.

    Returns the inquiry ID, next-step guidance in both languages, and Calendly URL.
    No automatic outreach is triggered — approval_required is always True.
    """
    LEADS_DIR.mkdir(parents=True, exist_ok=True)

    inquiry_id = f"inq_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.now(UTC).isoformat(timespec="seconds")

    record = {
        "inquiry_id": inquiry_id,
        "company": req.company,
        "sector": req.sector,
        "email": req.email,
        "name": req.name,
        "message": req.message,
        "language_pref": req.language_pref,
        "status": "new",
        "approval_required": True,
        "governance_decision": "DRAFT_ONLY",
        "created_at": now_iso,
    }

    with WEBSITE_INQUIRIES_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    next_step_ar = (
        "شكراً لاهتمامك. سيتواصل معك فريق Dealix خلال يوم عمل واحد. "
        "يمكنك حجز موعد مباشرة عبر الرابط أدناه."
    )
    next_step_en = (
        "Thank you for your interest. The Dealix team will be in touch within one business day. "
        "You can also book a call directly using the link below."
    )

    return {
        "inquiry_id": inquiry_id,
        "governance_decision": "DRAFT_ONLY",
        "approval_required": True,
        "next_step_ar": next_step_ar,
        "next_step_en": next_step_en,
        "calendly_url": CALENDLY_URL,
        "created_at": now_iso,
    }
