"""
System 26 — Enterprise Control Plane router.

Surfaces the `dealix.control_plane.ControlPlane` facade as read-only
snapshots. Mutating endpoints are intentionally not exposed: the
sovereign Control Plane is mutated *inside* the platform via Python
APIs, not over HTTP, until an S4 launch gate has been approved.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from dealix.control_plane import (
    ControlPlane,
    build_default_control_plane,
)

router = APIRouter(prefix="/api/v1/control-plane", tags=["control-plane"])

_PLANE: ControlPlane | None = None


def _plane() -> ControlPlane:
    global _PLANE
    if _PLANE is None:
        _PLANE = build_default_control_plane()
    return _PLANE


@router.get("/health")
async def control_plane_health() -> dict[str, str]:
    """Lightweight liveness probe for the Control Plane."""
    return {"system": "26_control_plane", "status": "ok"}


@router.get("/snapshot")
async def control_plane_snapshot() -> dict[str, Any]:
    """Read-only snapshot of every Level Max layer."""
    return _plane().snapshot()


@router.get("/sovereignty")
async def sovereignty_order() -> dict[str, list[str]]:
    snap = _plane().snapshot()
    return {"sovereignty_order": snap["sovereignty_order"]}


@router.get("/security-mode")
async def security_mode() -> dict[str, str]:
    return {"security_mode": _plane().security_mode_manager.mode.value}


@router.get("/commercial-packaging")
async def commercial_packaging() -> dict[str, Any]:
    return _plane().commercial.to_dict()


@router.get("/health-flags")
async def health_flags() -> dict[str, Any]:
    flags = _plane().refresh_health_flags()
    return {
        "flags": [f.value for f in flags],
        "metrics": _plane().health.metrics.to_dict(),
    }


@router.get("/scale-kill-board")
async def scale_kill_board() -> dict[str, Any]:
    return _plane().scale_kill.render()


@router.get("/money-snapshot")
async def money_snapshot() -> dict[str, Any]:
    return _plane().money.snapshot().to_dict()


@router.get("/intelligence-graph/summary")
async def intelligence_graph_summary() -> dict[str, Any]:
    return _plane().graph.summary()


@router.get("/public-api-readiness")
async def public_api_readiness() -> dict[str, Any]:
    return _plane().public_api.status()


@router.get("/marketplace-readiness")
async def marketplace_readiness() -> dict[str, Any]:
    return _plane().marketplace.status()
