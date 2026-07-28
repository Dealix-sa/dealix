#!/usr/bin/env python3
"""Validate .env.railway.*.generated — no secrets printed, only missing placeholders."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(
    r"CHANGE_ME|REPLACE_|REPLACE$|<paste|<your_|sk_live_CHANGE|phc_CHANGE",
    re.I,
)

REQUIRED_API = (
    "DATABASE_URL",
    "APP_SECRET_KEY",
    "ENVIRONMENT",
    "CORS_ORIGINS",
    "API_KEYS",
    "DEALIX_API_KEY",
    "ADMIN_API_KEYS",
    # The single-key alias the founder scripts and the ops proxy export to
    # *call* the admin surface (scripts/run_founder_commercial_day.sh,
    # verify_commercial_launch_ready.py). The server-side gate accepts it as
    # well as ADMIN_API_KEYS, so requiring it here keeps the two in step —
    # an environment that omits it leaves those tools with no credential.
    "DEALIX_ADMIN_API_KEY",
    "MOYASAR_SECRET_KEY",
    "MOYASAR_WEBHOOK_SECRET",
    "POSTHOG_API_KEY",
    "CALENDLY_URL",
)
REQUIRED_FE = (
    "NEXT_PUBLIC_API_URL",
    "NEXT_PUBLIC_SITE_URL",
    "NEXT_PUBLIC_USE_DEALIX_OPS_PROXY",
    "DEALIX_ADMIN_API_KEY",
    "DEALIX_API_KEY",
)


def _load_dotenv(path: Path) -> int:
    if not path.is_file():
        return 0
    loaded = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if not key or key in os.environ:
            continue
        os.environ[key] = val.strip().strip('"').strip("'")
        loaded += 1
    return loaded


def _parse(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        out[key.strip()] = val.strip()
    return out


def _env_snapshot(keys: tuple[str, ...]) -> dict[str, str]:
    return {k: (os.getenv(k) or "").strip() for k in keys}


def _check_env(keys: tuple[str, ...], *, label: str) -> list[str]:
    issues: list[str] = []
    for key in keys:
        val = (os.getenv(key) or "").strip()
        if not val:
            issues.append(f"{label}: missing {key}")
        elif PLACEHOLDER.search(val):
            issues.append(f"{label}: placeholder {key}")
    cal = os.getenv("CALENDLY_WEBHOOK_SECRET") or os.getenv("CALENDLY_WEBHOOK_SIGNING_KEY", "")
    if "CALENDLY" in label or keys == REQUIRED_API:
        if not cal:
            issues.append(f"{label}: missing CALENDLY_WEBHOOK_SECRET or SIGNING_KEY")
        elif PLACEHOLDER.search(cal):
            issues.append(f"{label}: placeholder Calendly webhook")
    return issues


def _check_file(path: Path, required: tuple[str, ...]) -> list[str]:
    issues: list[str] = []
    env = _parse(path)
    if not env:
        return [f"missing file: {path.name}"]
    for key in required:
        val = env.get(key, "")
        if not val:
            issues.append(f"{path.name}: missing {key}")
        elif PLACEHOLDER.search(val):
            issues.append(f"{path.name}: placeholder {key}")
    if path.name.startswith(".env.railway.generated"):
        cal = env.get("CALENDLY_WEBHOOK_SECRET") or env.get("CALENDLY_WEBHOOK_SIGNING_KEY", "")
        if not cal:
            issues.append(f"{path.name}: missing CALENDLY_WEBHOOK_SECRET or SIGNING_KEY")
        elif PLACEHOLDER.search(cal):
            issues.append(f"{path.name}: placeholder Calendly webhook")
    return issues


def _credential_overlap(api_env: dict[str, str]) -> set[str]:
    service = {
        item.strip()
        for item in api_env.get("API_KEYS", "").split(",")
        if item.strip()
    }
    admin = {
        item.strip()
        for item in api_env.get("ADMIN_API_KEYS", "").split(",")
        if item.strip()
    }
    if api_env.get("DEALIX_API_KEY"):
        service.add(api_env["DEALIX_API_KEY"].strip())
    if api_env.get("DEALIX_ADMIN_API_KEY"):
        admin.add(api_env["DEALIX_ADMIN_API_KEY"].strip())
    return service & admin


def _alias_membership_issues(
    api_env: dict[str, str],
    frontend_env: dict[str, str],
) -> list[str]:
    issues: list[str] = []
    service = {
        item.strip()
        for item in api_env.get("API_KEYS", "").split(",")
        if item.strip()
    }
    admin = {
        item.strip()
        for item in api_env.get("ADMIN_API_KEYS", "").split(",")
        if item.strip()
    }
    for label, env in (("api", api_env), ("frontend", frontend_env)):
        service_alias = env.get("DEALIX_API_KEY", "").strip()
        admin_alias = env.get("DEALIX_ADMIN_API_KEY", "").strip()
        # An absent alias must be an issue, not a skipped check: backend
        # admin guards fail open on an empty value, so silence here would
        # report OK for an environment that has no admin boundary at all.
        if not service_alias:
            issues.append(f"{label}: DEALIX_API_KEY is missing")
        elif service_alias not in service:
            issues.append(f"{label}: DEALIX_API_KEY is not in API_KEYS")
        if not admin_alias:
            issues.append(f"{label}: DEALIX_ADMIN_API_KEY is missing")
        elif admin_alias not in admin:
            issues.append(
                f"{label}: DEALIX_ADMIN_API_KEY is not in ADMIN_API_KEYS"
            )
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--from-railway-env",
        action="store_true",
        help="Load generated env into process before validating (uses exported + file values)",
    )
    args = p.parse_args()

    api = ROOT / ".env.railway.generated"
    fe = ROOT / ".env.railway.frontend.generated"

    # Generated deployment files are separate trust boundaries. Validate each
    # file directly even in compatibility mode so backend values cannot satisfy
    # missing frontend requirements through the process environment.
    issues = _check_file(api, REQUIRED_API)
    issues.extend(_check_file(fe, REQUIRED_FE))
    api_env = _parse(api)
    frontend_env = _parse(fe)
    overlap = _credential_overlap(api_env)
    if overlap:
        issues.append(
            f"{api.name}: service and admin credential sets overlap"
        )
    issues.extend(_alias_membership_issues(api_env, frontend_env))

    print("== validate_railway_generated_env ==")
    if issues:
        for i in issues:
            print(f"  FAIL: {i}")
        print("RAILWAY_GENERATED_ENV=INCOMPLETE")
        return 1
    print("  ok: API + Frontend generated env complete (no placeholders)")
    print("RAILWAY_GENERATED_ENV=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
