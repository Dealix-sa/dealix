"""Internal API authentication gate.

Production must set DEALIX_INTERNAL_TOKEN. In local dev, when the env var
is unset, requests are allowed but the system refuses to call itself
production-ready (see docs/security/INTERNAL_API_AUTH_GATE.md).
"""

from __future__ import annotations

import logging
import os

from fastapi import Header, HTTPException, status

logger = logging.getLogger(__name__)

INTERNAL_TOKEN_ENV = "DEALIX_INTERNAL_TOKEN"
INTERNAL_TOKEN_HEADER = "X-Dealix-Internal-Token"


def _env_token() -> str | None:
    raw = os.environ.get(INTERNAL_TOKEN_ENV, "").strip()
    return raw or None


def require_internal_token(
    x_dealix_internal_token: str | None = Header(default=None),
) -> dict[str, str]:
    """FastAPI dependency: gate internal endpoints with a shared token.

    Returns a small context dict so handlers can record who-ish made the call.
    """

    configured = _env_token()
    if configured is None:
        logger.warning(
            "DEALIX_INTERNAL_TOKEN unset — running open in dev. "
            "Set the env var before promoting to production."
        )
        return {"actor": "founder_dev", "auth_mode": "open_dev"}

    presented = (x_dealix_internal_token or "").strip()
    if not presented or presented != configured:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_internal_token",
        )
    return {"actor": "founder", "auth_mode": "token"}


def is_production_token_set() -> bool:
    return _env_token() is not None
