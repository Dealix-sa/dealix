"""Internal API auth gate.

Behaviour:

* If ``DEALIX_INTERNAL_TOKEN`` is set in the environment, every request
  to internal endpoints MUST present a matching ``X-Dealix-Internal-Token``
  header. Mismatches are rejected with 401.

* If the env var is **not** set, requests are allowed in
  ``dev_unprotected`` mode. This is intentional for local dev but is
  treated as a production-readiness failure by
  ``docs/security/INTERNAL_API_AUTH_GATE.md``.

Coding agents MUST NOT add new ways to bypass this gate.
"""

from __future__ import annotations

import os
from typing import Final

from fastapi import Header, HTTPException, status

_ENV_VAR: Final[str] = "DEALIX_INTERNAL_TOKEN"
_HEADER: Final[str] = "X-Dealix-Internal-Token"


def auth_mode() -> str:
    """Return the current auth mode label used by health endpoints."""
    return "enforced" if os.environ.get(_ENV_VAR) else "dev_unprotected"


def require_internal_token(
    x_dealix_internal_token: str | None = Header(default=None, alias=_HEADER),
) -> str:
    """FastAPI dependency enforcing the internal token contract.

    Returns the auth mode (``enforced`` or ``dev_unprotected``) on
    success. Raises HTTP 401 if a token is configured but the caller
    omits or mismatches it.
    """
    expected = os.environ.get(_ENV_VAR)
    if not expected:
        # dev mode — explicitly permissive, but health endpoints surface
        # this so the founder can see it in the console.
        return "dev_unprotected"

    if not x_dealix_internal_token or x_dealix_internal_token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_internal_token",
                "hint": (
                    "Set the X-Dealix-Internal-Token header. "
                    "See docs/security/INTERNAL_API_AUTH_GATE.md."
                ),
            },
        )
    return "enforced"
