"""Internal CEO summary endpoint.

A minimal, read-only aggregate intended for founder/CEO automation. The
route is guarded by ``api.middleware.internal_token.InternalTokenMiddleware``
on the ``/api/v1/internal/`` prefix; this router only assembles the payload
and never mutates state.

Payload structure is deliberately conservative — every field is derived
from existing settings and on-disk markers, with safe defaults. No new
data sources are introduced here; richer surfaces should add fields to
this response over time rather than spawning new endpoints.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from core.config.settings import get_settings


router = APIRouter(prefix="/api/v1/internal/ceo", tags=["Admin"])


def _safe_path_marker(path_str: str) -> dict[str, Any]:
    """Return existence + child count for a ledger path (no content read)."""
    p = Path(path_str)
    return {
        "path": str(p),
        "exists": p.exists(),
        "is_dir": p.is_dir() if p.exists() else False,
    }


def _agent_registry_summary() -> dict[str, Any]:
    """Best-effort count of registered agents — never raises."""
    try:
        from auto_client_acquisition.agent_governance.agent_registry import (
            AGENT_REGISTRY,
        )

        agents = list(AGENT_REGISTRY)
        return {
            "count": len(agents),
            "available": True,
        }
    except Exception:  # noqa: BLE001 — defensive; never break /summary
        return {"count": 0, "available": False}


@router.get("/summary")
async def ceo_summary() -> dict[str, Any]:
    """Aggregate CEO snapshot — production-safe, read-only.

    Returns environment posture, kill-switch state, and registry counts.
    Never returns secret values. Safe to log.
    """
    settings = get_settings()

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "app": {
            "name": settings.app_name,
            "version": settings.app_version,
            "env": settings.app_env,
            "git_sha": settings.git_sha,
            "is_production": settings.is_production,
        },
        "kill_switches": {
            "whatsapp_mock_mode": settings.whatsapp_mock_mode,
            "whatsapp_allow_live_send": settings.whatsapp_allow_live_send,
            "is_live_send_allowed": settings.is_live_send_allowed,
            "whatsapp_daily_limit": settings.whatsapp_daily_limit,
        },
        "control_plane": {
            "internal_token_configured": settings.internal_token_value is not None,
            "admin_api_keys_configured": len(settings.admin_api_key_list) > 0,
            "private_ops": _safe_path_marker(settings.dealix_private_ops),
            "public_base_url": settings.public_base_url,
        },
        "registry": {
            "agents": _agent_registry_summary(),
        },
        "next_actions": [
            "Verify make production-certification is green",
            "Confirm WHATSAPP_MOCK_MODE remains true until live-send certification",
            "Review docs/ops/DEALIX_FINAL_READINESS_REPORT.md",
        ],
    }
