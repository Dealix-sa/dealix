#!/usr/bin/env python3
"""
Phase 6 — Railway Production Environment Contract Check

Verifies all required environment variables are present and valid before
any Railway deployment proceeds. Exits 1 with a clear error list if any
required vars are missing or misconfigured.

Usage:
    python scripts/railway/check_env_contract.py
    python scripts/railway/check_env_contract.py --strict   # also checks optional vars

Outputs:
    RAILWAY_ENV_CONTRACT=PASS  (exit 0) — all required vars present
    RAILWAY_ENV_CONTRACT=FAIL  (exit 1) — one or more required vars missing
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass


@dataclass
class EnvSpec:
    key: str
    required: bool
    description: str
    example: str
    check: str = "present"  # "present" | "nonempty" | "boolean" | "url"


REQUIRED: list[EnvSpec] = [
    EnvSpec("APP_ENV",            True,  "Application environment",          "production",             "nonempty"),
    EnvSpec("APP_SECRET_KEY",     True,  "App secret key (32+ chars)",       "change-me-32-chars-min", "nonempty"),
    EnvSpec("DATABASE_URL",       True,  "PostgreSQL connection URL",         "postgresql://...",       "url"),
    EnvSpec("EXTERNAL_SEND_ENABLED",    True,  "Must be false in production",  "false",  "boolean"),
    EnvSpec("OUTBOUND_MODE",            True,  "Must be draft_only by default","draft_only", "nonempty"),
    EnvSpec("EMAIL_SEND_ENABLED",       True,  "Email send gate",              "false",  "boolean"),
    EnvSpec("WHATSAPP_SEND_ENABLED",    True,  "WhatsApp send gate",           "false",  "boolean"),
    EnvSpec("WHATSAPP_ALLOW_LIVE_SEND", True,  "WhatsApp live send gate",      "false",  "boolean"),
    EnvSpec("SMS_SEND_ENABLED",         True,  "SMS send gate",                "false",  "boolean"),
]

OPTIONAL: list[EnvSpec] = [
    EnvSpec("OPENAI_API_KEY",       False, "OpenAI API key",         "sk-...",    "present"),
    EnvSpec("DEEPSEEK_API_KEY",     False, "DeepSeek API key",       "sk-...",    "present"),
    EnvSpec("OPENROUTER_API_KEY",   False, "OpenRouter API key",     "sk-...",    "present"),
    EnvSpec("GROQ_API_KEY",         False, "Groq API key",           "gsk_...",   "present"),
    EnvSpec("MINIMAX_API_KEY",      False, "MiniMax API key",        "...",        "present"),
    EnvSpec("KIMI_API_KEY",         False, "Kimi/Moonshot API key",  "sk-...",    "present"),
    EnvSpec("AI_DAILY_BUDGET_USD",  False, "Daily AI spend cap",     "5.0",       "present"),
    EnvSpec("CORS_ORIGINS",         False, "Allowed CORS origins",   "https://...", "present"),
    EnvSpec("ADMIN_API_KEYS",       False, "Admin API keys",         "key1,key2", "present"),
    EnvSpec("LOG_LEVEL",            False, "Logging level",          "INFO",      "present"),
]

SAFETY_DEFAULTS = {
    "EXTERNAL_SEND_ENABLED": "false",
    "OUTBOUND_MODE": "draft_only",
    "EMAIL_SEND_ENABLED": "false",
    "WHATSAPP_SEND_ENABLED": "false",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "SMS_SEND_ENABLED": "false",
}


def _check_spec(spec: EnvSpec) -> str | None:
    val = os.environ.get(spec.key)
    if val is None:
        return f"MISSING — {spec.description} (example: {spec.example})"
    if spec.check == "nonempty" and not val.strip():
        return f"EMPTY — {spec.description} must not be empty"
    if spec.check == "boolean" and val.strip().lower() not in ("true", "false", "0", "1"):
        return f"INVALID — {spec.description} must be 'true' or 'false', got: {val!r}"
    if spec.check == "url" and not val.strip().startswith(("postgresql://", "postgres://", "sqlite://")):
        return f"INVALID — {spec.description} must be a valid database URL"
    return None


def _check_safety_posture() -> list[str]:
    warnings = []
    for key, expected in SAFETY_DEFAULTS.items():
        actual = os.environ.get(key, expected).strip().lower()
        if key == "OUTBOUND_MODE":
            if actual != expected:
                warnings.append(f"SAFETY WARN: {key}={actual!r} — expected {expected!r}")
        else:
            if actual not in ("false", "0"):
                warnings.append(f"SAFETY WARN: {key}={actual!r} — live sending may be enabled")
    return warnings


def check_contract(strict: bool = False) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for spec in REQUIRED:
        err = _check_spec(spec)
        if err:
            errors.append(f"  ✗ {spec.key}: {err}")

    if strict:
        for spec in OPTIONAL:
            err = _check_spec(spec)
            if err:
                warnings.append(f"  ⚠ {spec.key}: {err}")

    warnings.extend(_check_safety_posture())

    return len(errors) == 0, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Railway production env contract check")
    parser.add_argument("--strict", action="store_true", help="Also check optional variables")
    args = parser.parse_args()

    print("Railway Environment Contract Check")
    print("=" * 50)

    passed, errors, warnings = check_contract(strict=args.strict)

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(w)

    if errors:
        print("\nErrors:")
        for e in errors:
            print(e)
        print(f"\nRAILWAY_ENV_CONTRACT=FAIL ({len(errors)} error(s))")
        return 1

    print(f"\nAll {len(REQUIRED)} required variables present and valid.")
    if args.strict:
        print(f"{len(OPTIONAL) - len(warnings)} of {len(OPTIONAL)} optional variables configured.")
    print("\nRAILWAY_ENV_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
