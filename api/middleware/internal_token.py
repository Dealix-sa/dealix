"""Dual-token guard for /api/v1/internal/* routes.

Production-safe internal control plane access. Accepts EITHER of:

  - ``X-Dealix-Internal-Token: <DEALIX_INTERNAL_TOKEN>``  (preferred for
    founder/CEO automation; lets internal access live in its own secret
    independent of the broader ``ADMIN_API_KEYS`` list).
  - ``X-API-Key: <one of ADMIN_API_KEYS>``  (existing admin channel —
    preserved so this middleware does not break any currently working
    integration).

In production ``app_env == "production"``:
  - At least one of the two credential sources MUST be configured at boot.
  - Requests without a matching header return ``403``.

In development/test/staging:
  - If neither credential source is configured at boot, requests are
    allowed through so local development of the CEO summary endpoint
    remains frictionless.
  - If credentials ARE configured, the rules above still apply.

This module never logs token values. The X-Dealix-Internal-Token alias is
also recognised as ``X-DEALIX-INTERNAL-TOKEN`` (case insensitive — Starlette
normalises). All comparisons use ``hmac.compare_digest`` to prevent timing
attacks on the secret.
"""

from __future__ import annotations

import hmac

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from core.config.settings import get_settings


_INTERNAL_PREFIX = "/api/v1/internal/"
_HEADER_INTERNAL = "x-dealix-internal-token"
_HEADER_API_KEY = "x-api-key"


def _token_matches(presented: str, expected: str | None) -> bool:
    """Constant-time comparison; returns False if either side is empty."""
    if not presented or not expected:
        return False
    return hmac.compare_digest(presented, expected)


def _api_key_matches(presented: str, expected_list: list[str]) -> bool:
    if not presented or not expected_list:
        return False
    return any(hmac.compare_digest(presented, expected) for expected in expected_list)


class InternalTokenMiddleware(BaseHTTPMiddleware):
    """Guard ``/api/v1/internal/*`` routes with dual-token auth."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        path = request.url.path
        if not path.startswith(_INTERNAL_PREFIX):
            return await call_next(request)

        settings = get_settings()
        internal_token = settings.internal_token_value
        admin_keys = settings.admin_api_key_list
        has_credentials_configured = bool(internal_token) or bool(admin_keys)

        # Dev convenience: if no credentials configured and we are NOT in
        # production, allow through. Production with no credentials is
        # blocked at startup validation (see api/main.py:_validate_production_secrets
        # and verify_production_env.py), so by the time a request reaches
        # here in production at least one source is configured.
        if not has_credentials_configured and not settings.is_production:
            return await call_next(request)

        presented_internal = request.headers.get(_HEADER_INTERNAL, "")
        presented_api_key = request.headers.get(_HEADER_API_KEY, "")

        if _token_matches(presented_internal, internal_token) or _api_key_matches(
            presented_api_key, admin_keys
        ):
            return await call_next(request)

        return JSONResponse(
            status_code=403,
            content={
                "error": "internal_token_required",
                "detail": (
                    "Provide X-Dealix-Internal-Token (DEALIX_INTERNAL_TOKEN) or "
                    "X-API-Key (one of ADMIN_API_KEYS)."
                ),
            },
        )
