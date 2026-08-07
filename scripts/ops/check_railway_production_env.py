#!/usr/bin/env python3
"""Railway production environment checker for Dealix.

This script intentionally prints only variable names, never secret values.
It is safe to run in CI, Railway predeploy logs, and local shells.
"""

from __future__ import annotations

import os
import sys
from urllib.parse import urlparse

REQUIRED_FOR_PRODUCTION = (
    "APP_ENV",
    "ENVIRONMENT",
    "DATABASE_URL",
    "APP_SECRET_KEY",
    "JWT_SECRET_KEY",
    "API_KEYS",
    "ADMIN_API_KEYS",
)

SAFE_REQUIRED_DEFAULTS = {
    "EXTERNAL_SEND_ENABLED": "false",
    "EMAIL_SEND_ENABLED": "false",
    "WHATSAPP_SEND_ENABLED": "false",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "SMS_SEND_ENABLED": "false",
    "OUTBOUND_MODE": "draft_only",
}

PLACEHOLDER_FRAGMENTS = (
    "change-me",
    "changeme",
    "CHANGE_ME",
    "placeholder",
    "dummy",
    "example",
    "test-secret",
)


def is_missing(name: str) -> bool:
    return not os.getenv(name, "").strip()


def looks_placeholder(name: str) -> bool:
    value = os.getenv(name, "")
    lowered = value.lower()
    return any(fragment.lower() in lowered for fragment in PLACEHOLDER_FRAGMENTS)


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    app_env = os.getenv("APP_ENV", "").strip().lower()
    environment = os.getenv("ENVIRONMENT", "").strip().lower()

    if app_env != "production":
        warnings.append(f"APP_ENV is {app_env or '<unset>'}; Railway production should use APP_ENV=production")
    if environment != "production":
        warnings.append(
            f"ENVIRONMENT is {environment or '<unset>'}; Railway production should use ENVIRONMENT=production"
        )

    for name in REQUIRED_FOR_PRODUCTION:
        if is_missing(name):
            failures.append(f"Missing required Railway variable: {name}")
        elif name in {"APP_SECRET_KEY", "JWT_SECRET_KEY", "API_KEYS", "ADMIN_API_KEYS"} and looks_placeholder(name):
            failures.append(f"Railway variable must not be a placeholder: {name}")

    app_secret = os.getenv("APP_SECRET_KEY", "")
    jwt_secret = os.getenv("JWT_SECRET_KEY", "")
    if app_secret and len(app_secret) < 32:
        failures.append("APP_SECRET_KEY must be at least 32 characters")
    if jwt_secret and len(jwt_secret) < 32:
        failures.append("JWT_SECRET_KEY must be at least 32 characters")

    database_url = os.getenv("DATABASE_URL", "")
    if database_url:
        parsed = urlparse(database_url.replace("postgresql+asyncpg://", "postgresql://"))
        if parsed.scheme not in {"postgres", "postgresql"}:
            failures.append("DATABASE_URL must be a Postgres URL")
        if not parsed.hostname:
            failures.append("DATABASE_URL must include a hostname")

    for name, expected in SAFE_REQUIRED_DEFAULTS.items():
        actual = os.getenv(name, expected).strip().lower()
        if name == "OUTBOUND_MODE":
            if actual not in {"draft_only", "disabled", "controlled_live"}:
                failures.append(f"OUTBOUND_MODE has unsupported value: {actual}")
            if actual == "controlled_live" and os.getenv("EXTERNAL_SEND_ENABLED", "false").lower() != "true":
                failures.append("OUTBOUND_MODE=controlled_live requires EXTERNAL_SEND_ENABLED=true")
        else:
            if actual not in {"true", "false", "1", "0", "yes", "no", "on", "off"}:
                failures.append(f"{name} must be boolean-like")

    if failures:
        print("RAILWAY_PRODUCTION_ENV=FAIL")
        for failure in failures:
            print(f"FAIL: {failure}")
        for warning in warnings:
            print(f"WARN: {warning}")
        print("NEXT_ACTION: set the missing Railway service variables, then redeploy.")
        return 1

    print("RAILWAY_PRODUCTION_ENV=READY")
    print("Required production variables are present and non-placeholder.")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
