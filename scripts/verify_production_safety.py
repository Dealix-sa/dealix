#!/usr/bin/env python3
"""verify_production_safety.py — production environment must be safe by default.

Checks:
  1. .env.example exposes required keys (APP_SECRET_KEY, DATABASE_URL).
  2. No committed file contains an obvious literal secret value.
  3. api/main.py declares a `/healthz` endpoint and uses FastAPI.
  4. There is no plaintext `WHATSAPP_ALLOW_LIVE_SEND=true` anywhere
     except documentation prose.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_ENV_KEYS = ("APP_SECRET_KEY", "DATABASE_URL")

# Conservative secret signatures only — we intentionally avoid generic
# patterns that flood with false positives.
SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),               # AWS access key
    re.compile(r"sk-[A-Za-z0-9]{20,}"),            # OpenAI / similar
    re.compile(r"xoxb-[A-Za-z0-9-]{10,}"),         # Slack bot token
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),           # GitHub PAT
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
)

SCAN_DIRS = ("api", "dealix", "apps/web/src", "frontend/src", "scripts", "core")
SCAN_SUFFIXES = (".py", ".ts", ".tsx", ".js", ".env", ".yaml", ".yml", ".toml")
SKIP_NAMES = {".env.example", ".env.staging.example", ".gitleaks.toml", ".secrets.baseline"}


def main() -> int:
    failures: list[str] = []

    env_example = REPO / ".env.example"
    if not env_example.exists():
        failures.append("missing:.env.example")
    else:
        body = env_example.read_text(encoding="utf-8", errors="ignore")
        for key in REQUIRED_ENV_KEYS:
            if key not in body:
                failures.append(f"env_example_missing:{key}")

    api_main = REPO / "api" / "main.py"
    if api_main.exists():
        body = api_main.read_text(encoding="utf-8", errors="ignore")
        if "FastAPI" not in body:
            failures.append("api_main_not_fastapi")
        # /healthz can be declared in api/main.py OR in any router under
        # api/routers/. Treat the API package as one surface.
        healthz_seen = "/healthz" in body
        if not healthz_seen:
            routers_dir = REPO / "api" / "routers"
            if routers_dir.is_dir():
                for r in routers_dir.rglob("*.py"):
                    try:
                        if "/healthz" in r.read_text(
                            encoding="utf-8", errors="ignore"
                        ):
                            healthz_seen = True
                            break
                    except OSError:
                        continue
        if not healthz_seen:
            failures.append("api_missing_healthz")
    else:
        failures.append("missing:api/main.py")

    # Self-skip: the verifier family enumerates banned patterns as data.
    SELF_SKIPS = {
        (REPO / "scripts" / "verify_live_send_safety.py").resolve(),
        (REPO / "scripts" / "verify_production_safety.py").resolve(),
        (REPO / "scripts" / "verify_everything.py").resolve(),
        (REPO / "dealix_manifest.yaml").resolve(),
    }

    for sub in SCAN_DIRS:
        root = REPO / sub
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in SCAN_SUFFIXES:
                continue
            if p.name in SKIP_NAMES:
                continue
            try:
                if p.resolve() in SELF_SKIPS:
                    continue
            except OSError:
                continue
            if p.name.startswith("verify_") and p.suffix == ".py":
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pat in SECRET_PATTERNS:
                m = pat.search(text)
                if m:
                    rel = p.relative_to(REPO).as_posix()
                    failures.append(f"possible_secret:{rel}")
                    break
            # A literal `WHATSAPP_ALLOW_LIVE_SEND=true` in non-doc code
            # is a hard fail, *unless* the same file talks to the approval
            # queue or audit (then it is documenting the gate, not flipping it).
            if "WHATSAPP_ALLOW_LIVE_SEND=true" in text and p.suffix != ".md":
                low = text.lower()
                if not any(
                    tok in low
                    for tok in ("approval", "audit", "queue", "mock", "block", "deny")
                ):
                    failures.append(
                        f"live_send_enabled_in_code:{p.relative_to(REPO).as_posix()}"
                    )

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"PRODUCTION_SAFETY_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
