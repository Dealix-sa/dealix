"""
api.internal.auth — bearer-token dependency for the Founder Console.

Honors the existing convention: a comma-separated list of admin keys in
the DEALIX_ADMIN_API_KEY (or ADMIN_API_KEYS) env var. Rejects with 401
when missing or mismatched.

This is intentionally minimal: production traffic still goes through
the global APIKeyMiddleware. This dependency adds the Founder-Console
bearer token requirement on top.
"""
from __future__ import annotations

import hmac
import os

from fastapi import Header, HTTPException, status


def _allowed_keys() -> set[str]:
    """Read the admin key list from env (lazy, every request)."""
    raw = os.environ.get("DEALIX_ADMIN_API_KEY", "") or os.environ.get("ADMIN_API_KEYS", "")
    return {k.strip() for k in raw.split(",") if k.strip()}


def require_admin_bearer(authorization: str | None = Header(default=None)) -> str:
    """
    Dependency: require `Authorization: Bearer <token>` matching an admin key.

    Returns the matched token. Raises 401 otherwise.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing_bearer_token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split(" ", 1)[1].strip()
    allowed = _allowed_keys()
    if not allowed:
        # In dev with no key set, refuse rather than silently allow.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin_key_not_configured",
        )
    for k in allowed:
        if hmac.compare_digest(token, k):
            return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="bearer_token_mismatch",
        headers={"WWW-Authenticate": "Bearer"},
    )
