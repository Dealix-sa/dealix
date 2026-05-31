"""Public platform metadata — version + GTM surface registry."""

from __future__ import annotations

from fastapi import APIRouter

from core.config.settings import get_settings
from dealix.commercial_ops.gtm_public_surfaces import build_gtm_public_surfaces_snapshot

router = APIRouter(tags=["platform"])


@router.get("/version")
async def version() -> dict[str, object]:
    """Deploy identity for probes, partners, and status pages."""
    settings = get_settings()
    return {
        "service": "dealix-api",
        "status": "ok",
        "version": settings.app_version,
        "env": settings.app_env,
        "git_sha": settings.git_sha,
        "health": "/healthz",
        "docs": "/docs",
        "meta": "/api/v1/meta",
    }


@router.get("/api/v1/meta")
async def platform_meta() -> dict[str, object]:
    """GTM trust layer: surfaces registry + canonical links."""
    settings = get_settings()
    surfaces = build_gtm_public_surfaces_snapshot()
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "env": settings.app_env,
        "git_sha": settings.git_sha,
        "surfaces": surfaces,
        "canonical_links": {
            "healthz": "/healthz",
            "health": "/health",
            "openapi": "/openapi.json",
            "commercial_map": "/api/v1/commercial-map",
            "revenue_os_catalog": "/api/v1/revenue-os/catalog",
        },
    }
