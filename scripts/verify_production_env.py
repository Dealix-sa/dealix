"""Verify production env vars without printing any secret value.

Pass APP_ENV=production for strict production checks. In CI without
production env, runs in CI-safe mode and reports WARN for unset
production-only variables (the railway-readiness gate enforces them).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    VerifierReport,
    env_present,
    env_truthy,
    main_cli,
)

# Vars that must be PRESENT in production (no value is ever printed).
PROD_REQUIRED = [
    "APP_ENV",
    "DEALIX_INTERNAL_TOKEN",
    "JWT_SECRET_KEY",
    "DEALIX_PRIVATE_OPS",
    "DATABASE_URL",
]

PROD_RECOMMENDED = [
    "GROQ_API_KEY",
    "GOOGLE_SEARCH_API_KEY",
    "GOOGLE_SEARCH_CX",
    "GREEN_API_INSTANCE_ID",
    "GREEN_API_TOKEN",
    "HUBSPOT_ACCESS_TOKEN",
    "MOYASAR_SECRET_KEY",
    "POSTHOG_HOST",
    "SMTP_USER",
    "SMTP_PASSWORD",
]

# Safety toggles — value semantics matter, but we still never print values.
SAFETY_TOGGLES = {
    "WHATSAPP_MOCK_MODE": True,        # MUST be true (or unset) until safety gate passes
    "WHATSAPP_ALLOW_LIVE_SEND": False, # MUST be false until safety gate passes
}


def run() -> VerifierReport:
    r = VerifierReport(verifier="Production Env")
    app_env = os.environ.get("APP_ENV", "").lower()
    production = app_env == "production"
    r.pass_("app_env", f"APP_ENV={'production' if production else 'non-production'}")

    # Required
    for name in PROD_REQUIRED:
        if env_present(name):
            r.pass_(name, "set")
        elif production:
            r.fail(name, "unset in production",
                   hint=f"set {name} in Railway → Variables")
        else:
            r.warn(name, "unset (CI-safe; required in production)")

    # Recommended
    for name in PROD_RECOMMENDED:
        if env_present(name):
            r.pass_(name, "set")
        elif production:
            r.warn(name, "unset; integration disabled in production")
        else:
            r.warn(name, "unset (CI)")

    # Safety toggles — refuse the dangerous combo
    live_send = env_truthy("WHATSAPP_ALLOW_LIVE_SEND", default=False)
    mock_mode = env_truthy("WHATSAPP_MOCK_MODE", default=True)
    if live_send and not _safety_cert_passed():
        r.fail("WHATSAPP_ALLOW_LIVE_SEND",
               "live send enabled but live-send safety certification has not passed",
               hint="run: make live-send-safety  → must PASS  → then flip the flag")
    elif live_send and mock_mode:
        r.fail("WHATSAPP_MOCK_VS_LIVE",
               "WHATSAPP_ALLOW_LIVE_SEND=true while WHATSAPP_MOCK_MODE=true (contradictory)")
    else:
        r.pass_("whatsapp_safety_toggles",
                f"live_send={'on' if live_send else 'off'}, mock={'on' if mock_mode else 'off'}")

    # Frontend exposure: NEXT_PUBLIC_* must never include any secret name
    leaked = [
        k for k in os.environ
        if k.startswith("NEXT_PUBLIC_") and any(s in k for s in (
            "TOKEN", "SECRET", "KEY", "PASSWORD"
        ))
    ]
    if leaked:
        r.fail("NEXT_PUBLIC_no_secret_names",
               f"{len(leaked)} NEXT_PUBLIC_* vars look like secrets",
               hint="rename or strip — anything NEXT_PUBLIC_* ships to the browser")
    else:
        r.pass_("NEXT_PUBLIC_no_secret_names", "no NEXT_PUBLIC_* secret-named vars")

    return r


def _safety_cert_passed() -> bool:
    """Look for a freshly green safety certification marker."""
    marker = Path("/tmp/dealix_live_send_safety.PASS")
    return marker.exists()


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_production_env"))
