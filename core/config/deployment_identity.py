"""Resolve the deployed commit identity from platform-managed variables.

The generic ``GIT_SHA`` build fallback is intentionally last. Vercel and
Railway provide runtime-specific commit variables; those values are the
trustworthy source for release evidence when present.
"""

from __future__ import annotations

import os

_PLATFORM_SHA_NAMES = (
    "VERCEL_GIT_COMMIT_SHA",
    "RAILWAY_GIT_COMMIT_SHA",
    "GIT_SHA",
)


def resolve_deployment_git_sha(fallback: str = "unknown") -> str:
    """Return the first non-empty platform deployment SHA.

    Values are stripped but otherwise preserved so callers can compare the
    response with provider deployment metadata without leaking any secret.
    """

    for name in _PLATFORM_SHA_NAMES:
        value = os.getenv(name, "").strip()
        if value:
            return value
    normalized_fallback = str(fallback or "").strip()
    return normalized_fallback or "unknown"
