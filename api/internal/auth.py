"""Internal-API authentication gate.

Production policy:
    * APP_ENV=production       → DEALIX_INTERNAL_TOKEN MUST be set, and
                                  every request MUST present the matching
                                  X-Dealix-Internal-Token header.
    * Non-production           → bypass allowed for local dev only.

Never log the token. Never echo it in errors. Constant-time compare.
"""
from __future__ import annotations

import hmac
import os
from typing import Optional

try:
    from fastapi import HTTPException, Request, status
except Exception:  # pragma: no cover - FastAPI may be absent in CI lint runs
    HTTPException = Exception  # type: ignore[assignment]
    Request = object  # type: ignore[assignment]

    class _S:
        HTTP_401_UNAUTHORIZED = 401
        HTTP_403_FORBIDDEN = 403
        HTTP_500_INTERNAL_SERVER_ERROR = 500

    status = _S()  # type: ignore[assignment]

INTERNAL_TOKEN_HEADER = "X-Dealix-Internal-Token"


def _expected_token() -> Optional[str]:
    return os.environ.get("DEALIX_INTERNAL_TOKEN") or None


def _is_production() -> bool:
    return os.environ.get("APP_ENV", "").lower() == "production"


def require_internal_token(request: Request) -> None:
    """FastAPI dependency. Raises 401/403 if the token is missing or wrong.

    Never includes the expected token (or any part of it) in error messages.
    """
    expected = _expected_token()
    presented = getattr(request, "headers", {}).get(INTERNAL_TOKEN_HEADER) if request else None
    production = _is_production()

    if production and not expected:
        # Misconfiguration: production must have a token configured.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal token not configured",
        )
    if not production and not expected:
        # Local dev convenience: allow if APP_ENV != production and no token set.
        return

    if not presented:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing internal token",
        )
    # constant-time compare to avoid timing oracles
    if not hmac.compare_digest(presented, expected or ""):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid internal token",
        )
