"""
API key authentication middleware and dependency.
وسيط مصادقة مفتاح API.

Policy:
  * Requests to /health* and /docs*, /openapi.json, / are public.
  * Webhook endpoints use webhook signatures (see webhook_signatures.py).
  * All other /api/* endpoints require a valid X-API-Key header
    that matches one of the secrets in settings.api_keys (comma separated).
  * Admin endpoints (/api/v1/admin/*) additionally require a valid
    X-Admin-API-Key header from the ADMIN_API_KEYS env var.
    مسارات الإدارة تتطلب مفتاح X-Admin-API-Key منفصل.
"""

from __future__ import annotations

import hmac
import json
import os
import re
from collections.abc import Awaitable, Callable, Iterable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from core.logging import get_logger

logger = get_logger(__name__)

# Paths that are always public — no API key required
PUBLIC_PATHS: set[str] = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/healthz",
    "/readyz",
    "/livez",
    "/health/live",
    "/health/ready",
    "/health/deep",
    "/ready",
    "/live",
    "/version",
    "/api/status",
    "/api/v1/meta",
    # Public pricing list — prospects need to see plans without an API key.
    # Checkout + plan-specific tampering protection stays on /api/v1/checkout.
    "/api/v1/pricing/plans",
}
PUBLIC_PREFIXES: tuple[str, ...] = (
    "/docs",
    "/redoc",
    "/static",
    "/api/outbound",
    "/api/v1/webhooks/",  # webhooks use signatures instead
    "/api/v1/public/",   # public landing endpoints (demo-request, health)
    "/api/v1/auth/",     # auth endpoints use JWT — no API key required
)

# FastAPI security scheme header (for OpenAPI schema generation)
_admin_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


def _split_key_bundle(raw: str) -> list[str]:
    """Parse common secret shapes without logging or exposing key values.

    Production and CI have both used single keys, comma-separated strings,
    whitespace/newline-separated values, and JSON secret bundles. The smoke
    runner already accepts these shapes; the middleware should accept the same
    configured values so protected-route smoke tests verify the real edge path.
    """
    raw = raw.strip()
    if not raw:
        return []

    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]

    if raw.startswith("{"):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            values: list[str] = []
            for key in ("API_KEYS", "api_keys", "keys", "values", "value"):
                value = parsed.get(key)
                if isinstance(value, list):
                    values.extend(str(item).strip() for item in value)
                elif isinstance(value, str):
                    values.extend(_split_key_bundle(value))
            return [value for value in values if value]

    return [part.strip() for part in re.split(r"[,;\n\r\t ]+", raw) if part.strip()]


def _dedupe_keys(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _configured_keys() -> list[str]:
    values: list[str] = []
    for env_name in (
        "API_KEYS",
        "DEALIX_API_KEYS",
        "DEALIX_API_KEY",
        "DEALIX_PRODUCTION_API_KEY",
        "DEALIX_SMOKE_API_KEY",
    ):
        values.extend(_split_key_bundle(os.getenv(env_name, "")))
    return _dedupe_keys(values)


def _configured_admin_keys() -> list[str]:
    """Return the list of valid admin API keys from ADMIN_API_KEYS env var."""
    raw = os.getenv("ADMIN_API_KEYS", "")
    return _split_key_bundle(raw)


def verify_api_key(key: str | None, allowed: Iterable[str] | None = None) -> bool:
    if not key:
        return False
    allowed_keys = list(allowed) if allowed is not None else _configured_keys()
    if not allowed_keys:
        # No keys configured → allow (dev mode). Production MUST set API_KEYS.
        return True
    return any(hmac.compare_digest(k, key) for k in allowed_keys)


def verify_admin_key(key: str | None) -> bool:
    """Constant-time comparison against ADMIN_API_KEYS.
    Returns True in dev mode (no admin keys configured).
    تحقق ثابت الوقت من مفتاح الإدارة.
    """
    if not key:
        return False
    admin_keys = _configured_admin_keys()
    if not admin_keys:
        # No admin keys configured → allow (dev mode).
        return True
    return any(hmac.compare_digest(k, key) for k in admin_keys)


async def require_admin_key(
    request: Request,
    admin_key: str | None = Depends(_admin_key_header),
) -> None:
    """
    FastAPI dependency — enforce X-Admin-API-Key on admin routes.
    Raises HTTP 403 if the key is invalid or missing in production.
    تبعية FastAPI: تفرض مفتاح X-Admin-API-Key على مسارات الإدارة.
    """
    if not verify_admin_key(admin_key):
        logger.warning(
            "admin_key_invalid",
            path=request.url.path,
            has_key=bool(admin_key),
        )
        # 401 when no credential was supplied (authentication required); 403
        # when a key was supplied but is not a valid admin key (authenticated
        # actor, forbidden). This matches standard HTTP semantics.
        if not admin_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-Admin-API-Key",
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid X-Admin-API-Key",
        )


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path
        if path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES):
            return await call_next(request)

        allowed = _configured_keys()
        if not allowed:
            # No keys configured. In production this is a hard fail — an
            # unconfigured production deployment must NOT silently accept
            # every request. In dev/test, allow through for convenience.
            if os.getenv("APP_ENV", "").lower() == "production":
                logger.warning("api_keys_unconfigured_production", path=path)
                return JSONResponse(
                    {"detail": "API authentication is not configured"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            return await call_next(request)

        # Accept the key from the X-API-Key header or the ?api_key= query param.
        provided = request.headers.get("X-API-Key") or request.query_params.get("api_key")
        if not verify_api_key(provided, allowed):
            logger.warning("api_key_invalid", path=path, has_key=bool(provided))
            # Return a proper JSONResponse instead of raising HTTPException —
            # BaseHTTPMiddleware does not route exceptions through FastAPI's
            # exception handlers, so raising here produces a bare 500 at the
            # edge. Returning a Response gives clients a clean 401.
            return JSONResponse(
                {"detail": "Invalid or missing X-API-Key"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return await call_next(request)
