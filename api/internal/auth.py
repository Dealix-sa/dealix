"""Internal API authentication gate.

If ``DEALIX_INTERNAL_TOKEN`` is set in the environment, every internal
endpoint requires the ``X-Dealix-Internal-Token`` header to match. If
the env var is unset (typical local dev) requests are allowed.

In production the token MUST be set. See docs/security/INTERNAL_API_AUTH_GATE.md.
"""

from __future__ import annotations

import os

from fastapi import Header, HTTPException, status

INTERNAL_TOKEN_ENV = "DEALIX_INTERNAL_TOKEN"
INTERNAL_TOKEN_HEADER = "X-Dealix-Internal-Token"


def require_internal_token(
    x_dealix_internal_token: str | None = Header(default=None, alias=INTERNAL_TOKEN_HEADER),
) -> None:
    """FastAPI dependency that enforces the internal token gate."""

    expected = os.environ.get(INTERNAL_TOKEN_ENV)
    if not expected:
        return None
    if x_dealix_internal_token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="internal_token_required_or_invalid",
        )
    return None
