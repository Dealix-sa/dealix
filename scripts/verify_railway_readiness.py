#!/usr/bin/env python3
"""Verify Railway deployment readiness — repo-only static checks.

Runs the following non-network checks:

  1. ``railway.toml`` + ``railway.json`` exist and agree on:
       - ``builder = DOCKERFILE``
       - ``healthcheckPath = /healthz``
       - ``preDeployCommand`` points at ``scripts/railway_predeploy.sh``
  2. ``Dockerfile`` exists and uses a non-root user.
  3. ``scripts/railway_predeploy.sh`` exists and respects
     ``RUN_RAILWAY_PRE_DEPLOY_MIGRATE``.
  4. ``api/routers/health.py`` defines ``/healthz``.
  5. App listens on ``$PORT`` (string check in Dockerfile/Procfile).
  6. ``Procfile`` vs ``railway.toml`` migration commands overlap → WARN.
  7. Frontend secret leak scan — fails if ``frontend/src/**`` references a
     ``NEXT_PUBLIC_*`` env that looks like a server secret (TOKEN/API_KEY/SECRET),
     excluding the allow-list in
     ``docs/security/FRONTEND_PUBLIC_ENV_POLICY.md``.
  8. ``docs/ops/RAILWAY_PRODUCTION_DEPLOYMENT.md`` exists.

Exit codes: 0 PASS or WARN only; 1 if any FAIL.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# Standard SaaS frontend env names that are *designed* to be public — these
# are never flagged. Anything else matching the secret-looking patterns is
# flagged as FAIL unless explicitly allow-listed in
# docs/security/FRONTEND_PUBLIC_ENV_POLICY.md.
PUBLIC_FRONTEND_NAMES_OK = {
    "NEXT_PUBLIC_POSTHOG_KEY",
    "NEXT_PUBLIC_POSTHOG_HOST",
    "NEXT_PUBLIC_MOYASAR_PUBLISHABLE_KEY",
    "NEXT_PUBLIC_BASE_URL",
    "NEXT_PUBLIC_API_BASE_URL",
    "NEXT_PUBLIC_DEALIX_PUBLIC_KEY",
    "NEXT_PUBLIC_APP_ENV",
    "NEXT_PUBLIC_SENTRY_DSN",
}

# Words that signal a server secret. Any NEXT_PUBLIC_* containing these
# (case-insensitive) is fail-on-detect unless allow-listed.
SECRET_HINTS = ("TOKEN", "SECRET", "API_KEY", "ADMIN_KEY", "PASSWORD")


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _check_railway_files(fails: list[str], warns: list[str]) -> None:
    toml = ROOT / "railway.toml"
    js = ROOT / "railway.json"
    if not toml.exists():
        fails.append("railway.toml: missing")
    if not js.exists():
        fails.append("railway.json: missing")
    if not toml.exists() or not js.exists():
        return
    toml_text = _read(toml)
    js_text = _read(js)
    for name, text in (("railway.toml", toml_text), ("railway.json", js_text)):
        if "DOCKERFILE" not in text:
            fails.append(f"{name}: builder is not DOCKERFILE")
        if "/healthz" not in text:
            fails.append(f"{name}: healthcheckPath is not /healthz")
        if "scripts/railway_predeploy.sh" not in text:
            fails.append(f"{name}: preDeployCommand does not reference scripts/railway_predeploy.sh")


def _check_dockerfile(fails: list[str], warns: list[str]) -> None:
    df = ROOT / "Dockerfile"
    if not df.exists():
        fails.append("Dockerfile: missing")
        return
    text = _read(df)
    # Non-root user — look for either `USER app` style or any non-root USER directive.
    has_user = bool(re.search(r"^\s*USER\s+\S+", text, re.MULTILINE))
    if not has_user:
        fails.append("Dockerfile: no USER directive — runs as root")
    # PORT awareness
    if "$PORT" not in text and "${PORT" not in text:
        warns.append("Dockerfile: no $PORT reference — verify Railway PORT is honoured")


def _check_predeploy(fails: list[str], warns: list[str]) -> None:
    sh = ROOT / "scripts" / "railway_predeploy.sh"
    if not sh.exists():
        fails.append("scripts/railway_predeploy.sh: missing")
        return
    text = _read(sh)
    if "RUN_RAILWAY_PRE_DEPLOY_MIGRATE" not in text:
        fails.append("railway_predeploy.sh: missing RUN_RAILWAY_PRE_DEPLOY_MIGRATE gating")


def _check_healthz(fails: list[str], warns: list[str]) -> None:
    health = ROOT / "api" / "routers" / "health.py"
    if not health.exists():
        fails.append("api/routers/health.py: missing")
        return
    text = _read(health)
    if "/healthz" not in text:
        fails.append("api/routers/health.py: does not register /healthz")


def _check_procfile_overlap(fails: list[str], warns: list[str]) -> None:
    procfile = ROOT / "Procfile"
    railway_toml = ROOT / "railway.toml"
    if not (procfile.exists() and railway_toml.exists()):
        return
    proc = _read(procfile).lower()
    toml = _read(railway_toml).lower()
    if "alembic upgrade head" in proc and "predeploycommand" in toml and "railway_predeploy" in toml:
        warns.append(
            "Procfile 'release: alembic upgrade head' overlaps with railway.toml preDeployCommand "
            "(railway_predeploy.sh already runs alembic). Consider removing release: from Procfile."
        )


def _load_frontend_allowlist() -> set[Path]:
    """Allow-list of frontend files known to reference admin-like NEXT_PUBLIC_*."""
    doc = ROOT / "docs" / "security" / "FRONTEND_PUBLIC_ENV_POLICY.md"
    if not doc.exists():
        return set()
    text = _read(doc)
    # Extract paths from any line that looks like ` - frontend/src/... ` (markdown bullets).
    pattern = re.compile(r"^\s*[-*]\s+(`?)(frontend/src/[^\s`]+)\1", re.MULTILINE)
    return {ROOT / m.group(2) for m in pattern.finditer(text)}


def _check_frontend_secret_leak(fails: list[str], warns: list[str]) -> None:
    frontend_src = ROOT / "frontend" / "src"
    if not frontend_src.exists():
        warns.append("frontend/src: missing — skipping frontend scan")
        return
    allowlist = _load_frontend_allowlist()
    # Match NEXT_PUBLIC_* identifiers.
    next_public_re = re.compile(r"NEXT_PUBLIC_[A-Z0-9_]+")
    violations: list[tuple[Path, set[str]]] = []
    for path in frontend_src.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        names = set(next_public_re.findall(text))
        bad: set[str] = set()
        for name in names:
            if name in PUBLIC_FRONTEND_NAMES_OK:
                continue
            if any(h in name for h in SECRET_HINTS):
                bad.add(name)
        if bad:
            violations.append((path, bad))

    if not violations:
        return

    new_violations: list[tuple[Path, set[str]]] = []
    for path, bad in violations:
        if path in allowlist:
            warns.append(
                f"frontend secret allow-listed (tech debt): {path.relative_to(ROOT)} — {sorted(bad)}"
            )
        else:
            new_violations.append((path, bad))
    for path, bad in new_violations:
        fails.append(
            f"frontend secret leak: {path.relative_to(ROOT)} references {sorted(bad)} — "
            "use a backend proxy or add to docs/security/FRONTEND_PUBLIC_ENV_POLICY.md "
            "(only if intentional)."
        )


def _check_runbook(fails: list[str], warns: list[str]) -> None:
    doc = ROOT / "docs" / "ops" / "RAILWAY_PRODUCTION_DEPLOYMENT.md"
    if not doc.exists():
        fails.append("docs/ops/RAILWAY_PRODUCTION_DEPLOYMENT.md: missing")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.parse_args()

    fails: list[str] = []
    warns: list[str] = []

    _check_railway_files(fails, warns)
    _check_dockerfile(fails, warns)
    _check_predeploy(fails, warns)
    _check_healthz(fails, warns)
    _check_procfile_overlap(fails, warns)
    _check_frontend_secret_leak(fails, warns)
    _check_runbook(fails, warns)

    print("== verify_railway_readiness ==")
    for w in warns:
        print(f"  WARN: {w}")
    for f in fails:
        print(f"  FAIL: {f}")
    if not fails and not warns:
        print("  ok: all railway readiness checks passed")

    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    print(f"RAILWAY_READINESS_VERDICT={verdict}")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
