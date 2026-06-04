"""Commercial Launch OS — read-only endpoints.

Exposes the launch configuration (verticals, offers, readiness, channel policy,
metrics schema, media-social calendar schema) as READ-ONLY GET endpoints.

Doctrine: these endpoints never send anything. There are no POST/PUT/PATCH/DELETE
routes here, no email/WhatsApp/LinkedIn send, no CRM push-send, no form submit.
AI drafts, ranks, and recommends; the founder reviews, approves, and sends
manually; the system never sends externally.

Self-contained: depends only on FastAPI + stdlib and reads the repo `config/`
JSON files. Safe to include additively.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

_CONFIG = Path(__file__).resolve().parents[2] / "config"

router = APIRouter(prefix="/api/v1/commercial", tags=["Sales"])

# Separate router (different prefix); registered alongside `router` in api.main.
media_router = APIRouter(prefix="/api/v1/media-social", tags=["Sales"])


def _load(name: str) -> dict[str, Any]:
    path = _CONFIG / name
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"config not found: {name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - config is committed
        raise HTTPException(status_code=500, detail=f"invalid config: {name}") from exc


@router.get("/verticals")
def get_verticals() -> dict[str, Any]:
    """Read-only: the first-5 verticals and their ICP metadata."""
    return _load("commercial_verticals.json")


@router.get("/offers")
def get_offers() -> dict[str, Any]:
    """Read-only: the SAR offer ladder."""
    return _load("commercial_offers.json")


@router.get("/readiness")
def get_readiness() -> dict[str, Any]:
    """Read-only: launch governing rule + mandatory safety flags."""
    cfg = _load("commercial_launch.json")
    return {
        "governing_rule": cfg.get("governing_rule"),
        "mandatory_safety_flags": cfg.get("mandatory_safety_flags"),
        "external_send_enabled": cfg.get("external_send_enabled", False),
        "daily_draft_target": cfg.get("daily_draft_target"),
        "first_5_verticals": cfg.get("first_5_verticals", []),
    }


@router.get("/channel-policy")
def get_channel_policy() -> dict[str, Any]:
    """Read-only: manual-only channel policy."""
    return _load("commercial_channels.json")


@router.get("/metrics-schema")
def get_metrics_schema() -> dict[str, Any]:
    """Read-only: the manual-input metrics schema (no assumed numbers)."""
    return _load("commercial_metrics.json")


@media_router.get("/calendar-schema")
def get_calendar_schema() -> dict[str, Any]:
    """Read-only: media/social calendar schema (manual posting only)."""
    return _load("media_social_calendar.json")
