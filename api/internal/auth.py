"""Auth gate for the Dealix internal Founder Console endpoints.

In production, set DEALIX_INTERNAL_TOKEN. Requests must carry it via
`x-dealix-internal-token`. When the token is unset we run in
dev-unprotected mode so the Founder Console can be rendered locally; we
explicitly surface the mode in the response so it is impossible to
miss.
"""
from __future__ import annotations

import os
from typing import Literal

from fastapi import Header, HTTPException, status

AuthMode = Literal["enforced", "dev_unprotected"]


def auth_mode() -> AuthMode:
    return "enforced" if os.getenv("DEALIX_INTERNAL_TOKEN") else "dev_unprotected"


async def require_internal_token(
    x_dealix_internal_token: str | None = Header(default=None, alias="x-dealix-internal-token"),
) -> AuthMode:
    expected = os.getenv("DEALIX_INTERNAL_TOKEN")
    if expected is None:
        # Dev mode: do not raise, but mark the response.
        return "dev_unprotected"
    if not x_dealix_internal_token or x_dealix_internal_token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_or_missing_internal_token",
        )
    return "enforced"
