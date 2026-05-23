"""Internal API authentication.

Surfaces under /api/v1/internal/* are read-only for the founder console and
internal tooling. They MUST require an X-Internal-Token header signed by the
deployer. Every call is logged via the audit middleware.
"""

from __future__ import annotations

import hmac
import os
from typing import Annotated

from fastapi import Header, HTTPException, status

INTERNAL_API_TOKEN_ENV = "INTERNAL_API_TOKEN"


def _expected_token() -> str | None:
    value = os.environ.get(INTERNAL_API_TOKEN_ENV)
    if value is None:
        return None
    value = value.strip()
    return value or None


async def require_internal_token(
    x_internal_token: Annotated[str | None, Header(alias="X-Internal-Token")] = None,
) -> str:
    """FastAPI dependency: require a valid internal token header.

    Behavior:
    - If INTERNAL_API_TOKEN env var is set: header must match exactly.
    - If unset: dev/test mode returns "anonymous" and lets the request through,
      but only after stamping the audit log via middleware.
    """
    expected = _expected_token()
    if expected is None:
        return "anonymous-dev"
    if x_internal_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Internal-Token header",
        )
    if not hmac.compare_digest(x_internal_token.strip(), expected):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid X-Internal-Token",
        )
    return "internal"
