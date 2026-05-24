"""Founder Console internal auth.

The Founder Console is internal-only. We accept a single shared key via
the `x-internal-key` header. This is intentionally simple — never expose
these routes on the public internet.
"""
from __future__ import annotations

import os

from fastapi import Header, HTTPException, status

INTERNAL_KEY_ENV = "DEALIX_INTERNAL_KEY"


def require_internal_key(x_internal_key: str | None = Header(default=None)) -> str:
    expected = os.environ.get(INTERNAL_KEY_ENV)
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="internal_key_not_configured",
        )
    if not x_internal_key or x_internal_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_internal_key",
        )
    return x_internal_key
