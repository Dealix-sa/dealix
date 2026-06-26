"""
Public intake endpoints — unauthenticated, rate-limited.

POST /api/v1/public/custom-ai-request  — Rung-4 custom AI intake
POST /api/v1/public/contact            — General contact form

Every submission is written to var/ for founder review.
No external action is taken automatically. Founder must approve before any follow-up.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/public", tags=["public-intake"])

VAR_DIR = Path("var")


class CustomAIRequest(BaseModel):
    sector: Literal[
        "real_estate", "retail", "logistics", "professional_services", "other"
    ] = Field(..., description="Industry sector")
    use_case: str = Field(..., min_length=10, max_length=2000)
    data_volume: Literal["<1K rows", "1K-100K", "100K+"] = Field(...)
    data_sensitivity: Literal["public", "internal", "confidential"] = Field(...)
    timeline: Literal["<1 month", "1-3 months", "3+ months"] = Field(...)
    budget_band: Literal["5K-10K", "10K-25K", "25K+"] = Field(...)


@router.post("/custom-ai-request")
def submit_custom_ai_request(payload: CustomAIRequest) -> dict:
    """
    Accept a Rung-4 Custom AI intake form submission.
    Writes to var/custom_ai_requests.jsonl and queues for founder review.
    NO external action is taken automatically.
    """
    VAR_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "sector": payload.sector,
        "use_case": payload.use_case,
        "data_volume": payload.data_volume,
        "data_sensitivity": payload.data_sensitivity,
        "timeline": payload.timeline,
        "budget_band": payload.budget_band,
        "governance_decision": "queued_for_founder_review",
        "status": "pending_founder_approval",
        "disclaimer": "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة",
    }

    intake_file = VAR_DIR / "custom_ai_requests.jsonl"
    with intake_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    logger.info(
        "custom_ai_request queued sector=%s timeline=%s budget=%s",
        payload.sector,
        payload.timeline,
        payload.budget_band,
    )

    return {
        "status": "queued",
        "governance_decision": "queued_for_founder_review",
        "message": (
            "شكراً — تم استلام طلبك وسيُراجعه المؤسس قبل أي إجراء. "
            "Thank you — your request has been received and will be reviewed by the founder before any action."
        ),
    }


class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    company: str = Field(..., min_length=2, max_length=100)
    contact: str = Field(..., min_length=5, max_length=200, description="WhatsApp or email")
    message: str = Field(..., min_length=10, max_length=2000)


@router.post("/contact")
def submit_contact(payload: ContactRequest) -> dict:
    """
    Accept a general contact form submission.
    Writes to var/contact_requests.jsonl for founder review.
    NO external action is taken automatically.
    """
    VAR_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "name": payload.name,
        "company": payload.company,
        "contact_channel": payload.contact,
        "governance_decision": "queued_for_founder_review",
        "status": "pending_founder_review",
        "disclaimer": "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة",
    }
    # message stored separately — not logged to keep PII out of log stream
    message_record = {**record, "message": payload.message}
    contact_file = VAR_DIR / "contact_requests.jsonl"
    with contact_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(message_record, ensure_ascii=False) + "\n")

    logger.info(
        "contact_request queued company=%s",
        payload.company,
    )

    return {
        "status": "queued",
        "governance_decision": "queued_for_founder_review",
        "message": (
            "وصلت رسالتك — سيراجعها المؤسس ويتواصل معك خلال 24 ساعة. "
            "Your message was received — the founder will review and reach out within 24 hours."
        ),
    }
