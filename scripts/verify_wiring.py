#!/usr/bin/env python3
"""
verify_wiring.py — checks that promised surfaces are actually wired.

Reality, not vibes:
  - api/main.py mounts routers
  - api/routers/health.py exposes /healthz
  - Makefile defines audit/everything/production-certification
  - frontend/ has a build script
  - .github/workflows/ has CI + dealix-everything + dealix-production-certification

Exits 1 on any wiring gap.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""


def main() -> int:
    failures: list[str] = []
    ok: list[str] = []

    # 1) /healthz is reachable through the FastAPI app
    health = read(ROOT / "api/routers/health.py")
    if "/healthz" not in health:
        failures.append("api/routers/health.py does not expose /healthz")
    else:
        ok.append("api/routers/health.py exposes /healthz")

    # 2) FastAPI app mounts routers (smoke check)
    main_py = read(ROOT / "api/main.py")
    if "FastAPI(" not in main_py:
        failures.append("api/main.py does not instantiate FastAPI(...)")
    elif "include_router" not in main_py and "from api.routers" not in main_py:
        failures.append("api/main.py does not appear to mount any routers")
    else:
        ok.append("api/main.py instantiates FastAPI and mounts routers")

    # 3) Makefile defines the audit/everything/production-certification commands
    mk = read(ROOT / "Makefile")
    required_targets = [
        "audit:",
        "everything:",
        "production-certification:",
        "repo-completeness:",
        "non-empty-files:",
        "wiring-check:",
        "business-os:",
        "policy-check:",
        "agent-registry:",
        "eval-gate:",
        "live-send-safety:",
        "railway-readiness:",
    ]
    missing_targets = [t for t in required_targets if t not in mk]
    if missing_targets:
        failures.append(f"Makefile missing targets: {', '.join(missing_targets)}")
    else:
        ok.append(f"Makefile defines all {len(required_targets)} audit targets")

    # 4) Frontend build is wired
    fe_pkg = ROOT / "frontend/package.json"
    if fe_pkg.exists():
        try:
            data = json.loads(read(fe_pkg))
            scripts = data.get("scripts", {})
            if "build" not in scripts:
                failures.append("frontend/package.json missing 'build' script")
            else:
                ok.append(f"frontend/package.json has build: {scripts['build'][:60]}")
        except json.JSONDecodeError as exc:
            failures.append(f"frontend/package.json invalid JSON: {exc}")
    else:
        failures.append("frontend/package.json is missing")

    # 5) Required CI workflows
    wf_dir = ROOT / ".github/workflows"
    required_workflows = [
        "ci.yml",
        "dealix-everything.yml",
        "dealix-production-certification.yml",
    ]
    for wf in required_workflows:
        if not (wf_dir / wf).exists():
            failures.append(f".github/workflows/{wf} is missing")
        else:
            ok.append(f".github/workflows/{wf} exists")

    # 6) Workflows reference the verifiers they claim to run
    everything_wf = read(wf_dir / "dealix-everything.yml")
    if everything_wf and "verify_everything.py" not in everything_wf:
        failures.append("dealix-everything.yml does not run verify_everything.py")
    elif everything_wf:
        ok.append("dealix-everything.yml runs verify_everything.py")

    cert_wf = read(wf_dir / "dealix-production-certification.yml")
    if cert_wf and "production-certification" not in cert_wf and "verify_everything.py" not in cert_wf:
        failures.append(
            "dealix-production-certification.yml does not invoke production-certification or verify_everything.py"
        )
    elif cert_wf:
        ok.append("dealix-production-certification.yml invokes certification path")

    # 7) Dockerfile must contain start.sh HEREDOC (start.sh is generated at build time, not on disk)
    df = read(ROOT / "Dockerfile")
    if "/app/start.sh" not in df:
        failures.append("Dockerfile does not reference /app/start.sh")
    elif not re.search(r"COPY[^\n]*<<['\"]?EOF['\"]?\s+/app/start\.sh", df):
        failures.append("Dockerfile does not create /app/start.sh via HEREDOC")
    else:
        ok.append("Dockerfile generates /app/start.sh via HEREDOC")

    # Report
    print(f"WIRING: {len(ok)} ok, {len(failures)} failures")
    for line in ok:
        print(f"  ok   {line}")
    for line in failures:
        print(f"  FAIL {line}")

    if failures:
        print("WIRING: FAIL")
        return 1
    print("WIRING: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
