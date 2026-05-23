"""
Internal-API auth dependency.

Behaviour:
    - If the DEALIX_INTERNAL_TOKEN env var is set, the request must include
      the matching value in the X-Dealix-Internal-Token header. Missing or
      mismatched tokens return 401.
    - If the env var is unset, requests are allowed but the response carries
      auth_mode='dev_unprotected' so the UI / audit log can flag it.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from fastapi import Header, HTTPException, status


@dataclass(frozen=True)
class InternalAuthContext:
    """Resolved auth context for an internal request."""

    auth_mode: str  # "token" | "dev_unprotected"
    token_present: bool


def _env_token() -> str:
    return os.getenv("DEALIX_INTERNAL_TOKEN", "").strip()


async def require_internal_token(
    x_dealix_internal_token: str | None = Header(default=None, alias="X-Dealix-Internal-Token"),
) -> InternalAuthContext:
    """FastAPI dependency — returns the auth context or raises 401."""
    expected = _env_token()
    if not expected:
        return InternalAuthContext(auth_mode="dev_unprotected", token_present=False)
    if not x_dealix_internal_token or x_dealix_internal_token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_internal_token",
        )
    return InternalAuthContext(auth_mode="token", token_present=True)
