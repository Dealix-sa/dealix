"""
Feature Gating Middleware.
يربط كل طلب بالـ tenant المُتحقق منه من التوكن فقط.

This middleware publishes an **advisory** tenant hint derived strictly
from a verified access token. It is not the authority for entitlement
decisions — ``dealix.feature_gating.service.FeatureGate`` resolves the
tenant from the authenticated user on every gated route.

Client-supplied headers (``X-Tenant-ID``) are deliberately ignored here:
a browser-controlled value must never become request tenant context.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from api.security.jwt import decode_access_token


class FeatureGatingMiddleware(BaseHTTPMiddleware):
    """
    Injects a verified tenant hint into request.state for downstream use.
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

        tenant_id = self._extract_tenant_id(request)

        request.state.tenant_id = tenant_id
        request.state.tenant_id_source = "verified_jwt" if tenant_id else None
        # Lazy-load features when needed; don't block request here
        request.state.features_loaded = False

        return await call_next(request)

    def _extract_tenant_id(self, request: Request) -> str | None:
        """Return the tenant claim of a verified access token, else None.

        Only the signed ``tid`` claim is trusted. Headers are never read:
        honouring ``X-Tenant-ID`` here would let any caller pick the tenant
        whose entitlements are evaluated.
        """
        auth = request.headers.get("authorization", "")
        scheme, _, token = auth.partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            return None
        try:
            payload = decode_access_token(token.strip())
        except JWTError:
            return None
        tenant_id = payload.get("tid")
        return tenant_id if isinstance(tenant_id, str) and tenant_id else None
