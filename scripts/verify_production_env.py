#!/usr/bin/env python3
"""Verify production environment variable PRESENCE only — never prints values.

Outputs ``set`` or ``missing`` per variable. The verifier never reads the
secret value itself, only checks ``os.environ.get(name)`` is non-empty (and
in ``--ci`` mode, only verifies the variable NAME exists in
``core.config.settings.Settings``).

Required variables in production (``APP_ENV=production``):

  - JWT_SECRET_KEY, APP_SECRET_KEY, API_KEYS, ADMIN_API_KEYS  (existing)
  - APP_ENV  (mapped to pydantic ``app_env``)
  - DEALIX_INTERNAL_TOKEN OR ADMIN_API_KEYS  (one of two — internal auth)
  - DEALIX_PRIVATE_OPS
  - DATABASE_URL, CORS_ORIGINS, PUBLIC_BASE_URL

Optional (WARN if missing):

  GROQ_API_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_CX,
  HUBSPOT_ACCESS_TOKEN, MOYASAR_SECRET_KEY, POSTHOG_HOST,
  SMTP_USER, SMTP_PASSWORD, SMTP_FROM,
  GREEN_API_INSTANCE_ID, GREEN_API_TOKEN, WHATSAPP_DAILY_LIMIT.

Conflict rules (FAIL):

  - WHATSAPP_ALLOW_LIVE_SEND=true AND WHATSAPP_MOCK_MODE=true.
  - APP_ENV=production AND DEALIX_INTERNAL_TOKEN empty AND ADMIN_API_KEYS empty.

Exit codes:
  0 — PASS or WARN only
  1 — at least one FAIL
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


REQUIRED = (
    "JWT_SECRET_KEY",
    "APP_SECRET_KEY",
    "API_KEYS",
    "APP_ENV",
    "DEALIX_PRIVATE_OPS",
    "DATABASE_URL",
    "CORS_ORIGINS",
    "PUBLIC_BASE_URL",
)
# One of these must be set in production (internal control plane auth).
INTERNAL_AUTH_OPTIONS = ("DEALIX_INTERNAL_TOKEN", "ADMIN_API_KEYS")

OPTIONAL = (
    "GROQ_API_KEY",
    "GOOGLE_SEARCH_API_KEY",
    "GOOGLE_SEARCH_CX",
    "HUBSPOT_ACCESS_TOKEN",
    "MOYASAR_SECRET_KEY",
    "POSTHOG_HOST",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "SMTP_FROM",
    "GREEN_API_INSTANCE_ID",
    "GREEN_API_TOKEN",
    "WHATSAPP_DAILY_LIMIT",
)


def _is_truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _settings_names() -> set[str]:
    """Names of Settings fields — used in --ci mode."""
    from core.config.settings import Settings

    return {name.upper() for name in Settings.model_fields.keys()}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--ci",
        action="store_true",
        help=(
            "CI mode: only verify variable names are declared in Settings; "
            "do not require values to be present in the environment."
        ),
    )
    p.add_argument(
        "--strict-production",
        action="store_true",
        help=(
            "Treat the run as production even if APP_ENV is not 'production'. "
            "Useful for pre-deploy smoke tests."
        ),
    )
    args = p.parse_args()

    is_ci_mode = args.ci
    declared_names = _settings_names() if is_ci_mode else set()

    is_production = args.strict_production or os.getenv("APP_ENV", "").strip() == "production"

    fails: list[str] = []
    warns: list[str] = []

    print("== verify_production_env ==")
    print(f"  mode: {'ci' if is_ci_mode else 'live'}")
    print(f"  app_env: {os.getenv('APP_ENV', 'unset')}")
    print(f"  is_production: {is_production}")

    # ── Required ─────────────────────────────────────────────────
    print("  -- required --")
    for name in REQUIRED:
        if is_ci_mode:
            # Verify variable name is recognised by Settings (or known alias).
            ok = name in declared_names or name in {"API_KEYS", "APP_ENV"}
            status = "declared" if ok else "missing"
        else:
            ok = bool(os.getenv(name, "").strip())
            status = "set" if ok else "missing"
        print(f"    {name}: {status}")
        if not ok:
            if is_production or is_ci_mode:
                fails.append(f"required missing: {name}")
            else:
                warns.append(f"required missing (non-prod): {name}")

    # Internal auth — must have ONE of the options in production.
    print("  -- internal auth (need ≥1) --")
    internal_any = False
    for name in INTERNAL_AUTH_OPTIONS:
        if is_ci_mode:
            ok = True  # in CI we only check names — accept declared aliases
            status = "ok (ci)"
        else:
            ok = bool(os.getenv(name, "").strip())
            status = "set" if ok else "missing"
        print(f"    {name}: {status}")
        if ok:
            internal_any = True
    if not internal_any and is_production and not is_ci_mode:
        fails.append(
            "no internal auth configured: set DEALIX_INTERNAL_TOKEN or ADMIN_API_KEYS"
        )

    # ── Optional ─────────────────────────────────────────────────
    print("  -- optional (warn if missing) --")
    for name in OPTIONAL:
        if is_ci_mode:
            print(f"    {name}: ci-skip")
            continue
        ok = bool(os.getenv(name, "").strip())
        print(f"    {name}: {'set' if ok else 'missing'}")
        if not ok:
            warns.append(f"optional missing: {name}")

    # ── Conflict rules (FAIL) ────────────────────────────────────
    print("  -- conflict rules --")
    if not is_ci_mode:
        allow_live = _is_truthy(os.getenv("WHATSAPP_ALLOW_LIVE_SEND"))
        mock = _is_truthy(os.getenv("WHATSAPP_MOCK_MODE"))
        print(f"    WHATSAPP_ALLOW_LIVE_SEND: {allow_live}")
        print(f"    WHATSAPP_MOCK_MODE: {mock}")
        if allow_live and mock:
            fails.append(
                "contradictory flags: WHATSAPP_ALLOW_LIVE_SEND=true AND "
                "WHATSAPP_MOCK_MODE=true — pick one (mock wins if both)."
            )
    else:
        print("    skipped (ci)")

    # ── Summary ─────────────────────────────────────────────────
    print()
    for w in warns:
        print(f"  WARN: {w}")
    for f in fails:
        print(f"  FAIL: {f}")

    if fails:
        verdict = "FAIL"
    elif warns:
        verdict = "WARN"
    else:
        verdict = "PASS"
    print(f"PRODUCTION_ENV_VERDICT={verdict}")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
