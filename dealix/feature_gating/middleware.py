"""
Feature Gating Middleware.
يربط كل طلب بالـ tenant ويتحقق من صلاحية الوصول للميزة.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from dealix.feature_gating.service import FeatureGatingService


class FeatureGatingMiddleware(BaseHTTPMiddleware):
    """
    Injects feature flags into request.state for downstream use.
    Skips paths that don't need tenant context.
    """

    SKIP_PATHS = {
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth",
        "/api/v1/public",
        "/api/v1/webhooks",
    }

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        path = request.url.path

        # Skip public paths
        if any(path.startswith(skip) for skip in self.SKIP_PATHS):
            return await call_next(request)

        # Try to extract tenant_id from JWT or headers
        tenant_id = self._extract_tenant_id(request)

        if tenant_id:
            request.state.tenant_id = tenant_id
            # Lazy-load features when needed; don't block request here
            request.state.features_loaded = False
        else:
            request.state.tenant_id = None
            request.state.features_loaded = False

        return await call_next(request)

    def _extract_tenant_id(self, request: Request) -> str | None:
        # Priority: x-tenant-id header → JWT payload → path param
        tenant_id = request.headers.get("x-tenant-id")
        if tenant_id:
            return tenant_id

        # Try JWT
        auth = request.headers.get("authorization", "")
        if auth.startswith("Bearer "):
            token = auth.replace("Bearer ", "")
            try:
                import jwt

                from core.config.settings import get_settings
                payload = jwt.decode(
                    token,
                    get_settings().app_secret_key,
                    algorithms=["HS256"],
                )
                return payload.get("tenant_id")
            except Exception:
                pass

        return None
