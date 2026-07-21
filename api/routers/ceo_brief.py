"""
CEO Daily Brief API

Returns the latest generated daily brief or generates one on demand.
The brief is email-ready and can be sent via the email integration.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from scripts.daily_intelligence_scheduler import run_daily_intelligence

router = APIRouter(prefix="/api/v1/ceo-brief", tags=["CEO Daily Brief"])

BRIEF_DIR = Path("reports/daily_intelligence")


class CEODailyBriefResponse(BaseModel):
    generated_at: str
    markdown: str
    json_data: dict[str, Any]


@router.get("/latest", response_model=CEODailyBriefResponse)
async def get_latest_brief() -> CEODailyBriefResponse:
    """Return the latest generated CEO daily brief."""
    latest = _find_latest_brief()
    if not latest:
        # Generate one if none exists
        brief = run_daily_intelligence()
        md_path = BRIEF_DIR / f"daily_brief_{datetime.utcnow().strftime('%Y-%m-%d')}.md"
        return CEODailyBriefResponse(
            generated_at=brief["generated_at"],
            markdown=md_path.read_text(encoding="utf-8"),
            json_data=brief,
        )

    json_data = json.loads(latest["json"].read_text(encoding="utf-8"))
    markdown = latest["md"].read_text(encoding="utf-8")
    return CEODailyBriefResponse(
        generated_at=json_data["generated_at"],
        markdown=markdown,
        json_data=json_data,
    )


@router.post("/generate", response_model=CEODailyBriefResponse)
async def generate_brief() -> CEODailyBriefResponse:
    """Generate a fresh CEO daily brief now."""
    brief = run_daily_intelligence()
    md_path = BRIEF_DIR / f"daily_brief_{datetime.utcnow().strftime('%Y-%m-%d')}.md"
    return CEODailyBriefResponse(
        generated_at=brief["generated_at"],
        markdown=md_path.read_text(encoding="utf-8"),
        json_data=brief,
    )


@router.get("/email", response_model=dict[str, str])
async def get_brief_email() -> dict[str, str]:
    """Return CEO brief formatted as email subject + body."""
    latest = _find_latest_brief()
    if not latest:
        raise HTTPException(status_code=404, detail="No brief found. Generate one first.")

    json_data = json.loads(latest["json"].read_text(encoding="utf-8"))
    pipeline = json_data["pipeline"]

    subject = (
        f"Dealix Daily Brief — Pipeline SAR {pipeline['total_pipeline_sar']:,.0f} "
        f"| Health {pipeline['health']:.0f}/100"
    )
    body = latest["md"].read_text(encoding="utf-8")

    return {"subject": subject, "body": body, "to": "founder@dealix.me"}


def _find_latest_brief() -> dict[str, Path] | None:
    if not BRIEF_DIR.exists():
        return None
    json_files = sorted(BRIEF_DIR.glob("daily_brief_*.json"), reverse=True)
    if not json_files:
        return None
    json_path = json_files[0]
    md_path = json_path.with_suffix(".md")
    return {"json": json_path, "md": md_path if md_path.exists() else json_path}
